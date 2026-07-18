from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import os
import uuid
import base64
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Optional

import bcrypt
import httpx
import stripe
from fastapi import FastAPI, APIRouter, Request, Response, HTTPException, Depends
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field

from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone
from emergentintegrations.llm.openai.image_generation import OpenAIImageGeneration

from catalog import (CATALOG, CATEGORIES, BUNDLES, SAMPLE_REVIEWS, CREDIT_PACKS, get_tool,
                     get_tool_by_lookup, get_bundle, get_bundle_by_lookup, get_credit_pack_by_lookup)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("emporium")

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY", "")
LLM_MODEL = ("anthropic", "claude-sonnet-4-6")

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY") or "sk_test_emergent"
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

app = FastAPI()
api = APIRouter(prefix="/api")

SESSION_DAYS = 7
FREE_CREDITS = 30
# Credit costs per generation. Priced so even the cheapest bulk pack ($0.036/credit)
# keeps a ~3.4x+ markup over worst-case Universal Key cost (text $0.02, research $0.04, image $0.16).
STUDIO_COST = {"text": 2, "research": 4, "image": 15}


# ----------------------------- Models -----------------------------
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CheckoutItem(BaseModel):
    lookup_key: str
    quantity: int = Field(1, ge=1, le=50)


class CheckoutRequest(BaseModel):
    items: List[CheckoutItem]
    origin_url: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class DemoRequest(BaseModel):
    input: str


class ReviewRequest(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = ""


# ----------------------------- Auth helpers -----------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def public_user(u: dict) -> dict:
    return {
        "user_id": u["user_id"],
        "email": u["email"],
        "name": u.get("name", ""),
        "role": u.get("role", "user"),
        "picture": u.get("picture"),
        "auth_provider": u.get("auth_provider", "password"),
        "credits": u.get("credits", FREE_CREDITS),
    }


async def create_session(user_id: str) -> str:
    token = uuid.uuid4().hex + uuid.uuid4().hex
    await db.user_sessions.insert_one({
        "session_token": token,
        "user_id": user_id,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS),
        "created_at": datetime.now(timezone.utc),
    })
    return token


def set_session_cookie(response: Response, token: str):
    response.set_cookie(
        key="session_token", value=token, httponly=True, secure=True,
        samesite="none", max_age=SESSION_DAYS * 24 * 3600, path="/",
    )


def _extract_token(request: Request) -> Optional[str]:
    token = request.cookies.get("session_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    return token


async def _user_from_token(token: Optional[str]) -> Optional[dict]:
    if not token:
        return None
    session = await db.user_sessions.find_one({"session_token": token}, {"_id": 0})
    if not session:
        return None
    expires_at = session["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        return None
    user = await db.users.find_one({"user_id": session["user_id"]}, {"_id": 0})
    return user


async def get_current_user(request: Request) -> dict:
    user = await _user_from_token(_extract_token(request))
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


async def get_optional_user(request: Request) -> Optional[dict]:
    return await _user_from_token(_extract_token(request))


async def require_admin(request: Request) -> dict:
    user = await get_current_user(request)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ----------------------------- Auth routes -----------------------------
@api.post("/auth/register")
async def register(body: RegisterRequest, response: Response):
    email = body.email.lower()
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="An account with this email already exists")
    user_id = f"user_{uuid.uuid4().hex[:12]}"
    await db.users.insert_one({
        "user_id": user_id, "email": email, "name": body.name,
        "password_hash": hash_password(body.password), "role": "user",
        "auth_provider": "password", "credits": FREE_CREDITS,
        "created_at": datetime.now(timezone.utc),
    })
    token = await create_session(user_id)
    set_session_cookie(response, token)
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    return {"user": public_user(user), "session_token": token}


@api.post("/auth/login")
async def login(body: LoginRequest, response: Response):
    email = body.email.lower()
    user = await db.users.find_one({"email": email}, {"_id": 0})
    if not user or not user.get("password_hash") or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = await create_session(user["user_id"])
    set_session_cookie(response, token)
    return {"user": public_user(user), "session_token": token}


@api.post("/auth/session")
async def google_session(request: Request, response: Response):
    session_id = request.headers.get("X-Session-ID")
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session id")
    async with httpx.AsyncClient() as http:
        r = await http.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers={"X-Session-ID": session_id},
        )
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid session")
    data = r.json()
    email = data["email"].lower()
    existing = await db.users.find_one({"email": email}, {"_id": 0})
    if existing:
        user_id = existing["user_id"]
        await db.users.update_one({"user_id": user_id}, {"$set": {"picture": data.get("picture")}})
    else:
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        await db.users.insert_one({
            "user_id": user_id, "email": email, "name": data.get("name", ""),
            "picture": data.get("picture"), "role": "user", "auth_provider": "google",
            "credits": FREE_CREDITS, "created_at": datetime.now(timezone.utc),
        })
    token = data.get("session_token") or (uuid.uuid4().hex + uuid.uuid4().hex)
    await db.user_sessions.insert_one({
        "session_token": token, "user_id": user_id,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS),
        "created_at": datetime.now(timezone.utc),
    })
    set_session_cookie(response, token)
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    return {"user": public_user(user), "session_token": token}


@api.get("/auth/me")
async def me(user: dict = Depends(get_current_user)):
    return public_user(user)


@api.post("/auth/logout")
async def logout(request: Request, response: Response):
    token = _extract_token(request)
    if token:
        await db.user_sessions.delete_one({"session_token": token})
    response.delete_cookie("session_token", path="/")
    return {"status": "ok"}


# ----------------------------- Catalog routes -----------------------------
@api.get("/categories")
async def list_categories():
    counts = {}
    async for t in db.tools.find({}, {"_id": 0, "category": 1}):
        counts[t["category"]] = counts.get(t["category"], 0) + 1
    return [{**c, "count": counts.get(c["id"], 0)} for c in CATEGORIES]


@api.get("/tools")
async def list_tools(category: Optional[str] = None, search: Optional[str] = None, sort: Optional[str] = None):
    query = {}
    if category and category != "all":
        query["category"] = category
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"tagline": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}},
        ]
    tools = await db.tools.find(query, {"_id": 0, "demo_system": 0}).to_list(200)
    if sort == "price_asc":
        tools.sort(key=lambda t: t["price"])
    elif sort == "price_desc":
        tools.sort(key=lambda t: -t["price"])
    elif sort == "rating":
        tools.sort(key=lambda t: -t.get("rating", 0))
    else:
        tools.sort(key=lambda t: -t.get("users", 0))
    return tools


@api.get("/tools/{slug}")
async def get_tool_detail(slug: str):
    tool = await db.tools.find_one({"slug": slug}, {"_id": 0, "demo_system": 0})
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


@api.get("/bundles")
async def list_bundles():
    out = []
    for b in BUNDLES:
        tools = []
        for s in b["tool_slugs"]:
            t = get_tool(s)
            if t:
                tools.append({"slug": t["slug"], "name": t["name"], "icon": t["icon"], "price": t["price"]})
        out.append({**b, "tools": tools})
    return out


@api.get("/bundles/{slug}")
async def get_bundle_detail(slug: str):
    b = get_bundle(slug)
    if not b:
        raise HTTPException(status_code=404, detail="Bundle not found")
    tools = [get_tool(s) for s in b["tool_slugs"] if get_tool(s)]
    tools = [{"slug": t["slug"], "name": t["name"], "icon": t["icon"], "tagline": t["tagline"], "price": t["price"]} for t in tools]
    return {**b, "tools": tools}


@api.get("/tools/{slug}/reviews")
async def get_reviews(slug: str):
    revs = await db.reviews.find({"tool_slug": slug}, {"_id": 0}).sort("created_at", -1).to_list(200)
    count = len(revs)
    avg = round(sum(r["rating"] for r in revs) / count, 1) if count else 0
    return {"reviews": revs, "average": avg, "count": count}


@api.post("/tools/{slug}/reviews")
async def add_review(slug: str, body: ReviewRequest, user: dict = Depends(get_current_user)):
    if not get_tool(slug):
        raise HTTPException(status_code=404, detail="Tool not found")
    verified = False
    txns = await db.payment_transactions.find(
        {"user_id": user["user_id"], "payment_status": "paid"}, {"_id": 0}).to_list(500)
    for tx in txns:
        for item in tx.get("items", []):
            slugs = item.get("included_slugs") or [item.get("slug")]
            if slug in slugs:
                verified = True
    doc = {
        "tool_slug": slug, "user_id": user["user_id"],
        "user_name": user.get("name") or user["email"].split("@")[0],
        "rating": body.rating, "comment": body.comment.strip(), "verified": verified,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.reviews.update_one({"tool_slug": slug, "user_id": user["user_id"]}, {"$set": doc}, upsert=True)
    return doc


# ----------------------------- AI Studio (credit-metered) -----------------------------
class StudioTextRequest(BaseModel):
    mode: str = "chatgpt"
    prompt: str


class StudioImageRequest(BaseModel):
    prompt: str


class StudioResearchRequest(BaseModel):
    query: str


async def ensure_credits(user: dict) -> int:
    if user.get("credits") is None:
        await db.users.update_one({"user_id": user["user_id"]}, {"$set": {"credits": FREE_CREDITS}})
        return FREE_CREDITS
    return user["credits"]


async def require_credits(user: dict, cost: int):
    bal = await ensure_credits(user)
    if bal < cost:
        raise HTTPException(status_code=402, detail=f"Not enough credits — this needs {cost}, you have {bal}. Top up in the Studio.")


async def spend_credits(user: dict, cost: int) -> int:
    bal = await ensure_credits(user)
    await db.users.update_one({"user_id": user["user_id"]}, {"$inc": {"credits": -cost}})
    return bal - cost


@api.get("/studio/credits")
async def studio_credits(user: dict = Depends(get_current_user)):
    return {"credits": await ensure_credits(user), "costs": STUDIO_COST}


@api.get("/credit-packs")
async def credit_packs():
    return [{"slug": p["slug"], "name": p["name"], "credits": p["credits"], "price": p["price"],
             "lookup_key": p["lookup_key"], "badge": p["badge"]} for p in CREDIT_PACKS]


@api.post("/studio/text")
async def studio_text(body: StudioTextRequest, user: dict = Depends(get_current_user)):
    if not body.prompt.strip():
        raise HTTPException(status_code=400, detail="Enter a prompt")
    cost = STUDIO_COST["text"]
    await require_credits(user, cost)
    provider, model = ("openai", "gpt-5.4") if body.mode == "chatgpt" else ("anthropic", "claude-sonnet-4-6")
    label = "ChatGPT (GPT-5.4)" if body.mode == "chatgpt" else "Claude Sonnet 4.6"
    chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=f"studio_text_{uuid.uuid4().hex[:8]}",
                   system_message="You are a world-class writing, brainstorming and coding assistant. Be helpful, clear and well-structured.").with_model(provider, model)
    try:
        result = await chat.send_message(UserMessage(text=body.prompt.strip()))
    except Exception:
        logger.exception("studio text failed")
        raise HTTPException(status_code=502, detail="AI engine unavailable, please retry")
    remaining = await spend_credits(user, cost)
    return {"output": result, "engine": label, "credits": remaining}


@api.post("/studio/research")
async def studio_research(body: StudioResearchRequest, user: dict = Depends(get_current_user)):
    if not body.query.strip():
        raise HTTPException(status_code=400, detail="Enter a research question")
    cost = STUDIO_COST["research"]
    await require_credits(user, cost)
    chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=f"studio_research_{uuid.uuid4().hex[:8]}",
                   system_message=("You are a research analyst. Produce a structured synthesis: a concise TL;DR, "
                                   "3-6 key points with brief explanations, and a short 'Consider this' section. "
                                   "Be balanced and cite the type of source where relevant. Note that answers are "
                                   "based on model knowledge and may not include the very latest events.")).with_model("openai", "gpt-5.4")
    try:
        result = await chat.send_message(UserMessage(text=body.query.strip()))
    except Exception:
        logger.exception("studio research failed")
        raise HTTPException(status_code=502, detail="AI engine unavailable, please retry")
    remaining = await spend_credits(user, cost)
    return {"output": result, "credits": remaining}


@api.post("/studio/image")
async def studio_image(body: StudioImageRequest, user: dict = Depends(get_current_user)):
    if not body.prompt.strip():
        raise HTTPException(status_code=400, detail="Describe the image you want")
    cost = STUDIO_COST["image"]
    await require_credits(user, cost)
    gen = OpenAIImageGeneration(api_key=EMERGENT_LLM_KEY)
    try:
        images = await gen.generate_images(prompt=body.prompt.strip(), model="gpt-image-1", number_of_images=1)
    except Exception:
        logger.exception("studio image failed")
        raise HTTPException(status_code=502, detail="Image engine unavailable, please retry")
    if not images:
        raise HTTPException(status_code=502, detail="No image was generated, please retry")
    b64 = base64.b64encode(images[0]).decode("utf-8")
    remaining = await spend_credits(user, cost)
    return {"image_base64": b64, "credits": remaining}


# ----------------------------- AI: live demo (single-shot) -----------------------------
@api.post("/tools/{slug}/demo")
async def run_demo(slug: str, body: DemoRequest):
    tool = get_tool(slug)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    if not body.input.strip():
        raise HTTPException(status_code=400, detail="Please enter a prompt to try the tool")
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"demo_{slug}_{uuid.uuid4().hex[:8]}",
        system_message=tool["demo_system"] + "\n\nKeep the demo output focused and under 250 words.",
    ).with_model(*LLM_MODEL)
    try:
        result = await chat.send_message(UserMessage(text=body.input.strip()))
    except Exception as e:
        logger.exception("demo failed")
        raise HTTPException(status_code=502, detail="AI engine unavailable, please retry")
    return {"tool": tool["name"], "output": result}


# ----------------------------- AI: JARVIS assistant (streaming) -----------------------------
def _assistant_system(tools_summary: str) -> str:
    return (
        "You are ARIA, the AI concierge of AI Tool Emporium — a futuristic, high-tech marketplace for AI tools. "
        "Speak like a confident, sleek JARVIS-style assistant: crisp, futuristic, helpful, never robotic-boring. "
        "Your job is to understand what the buyer wants to accomplish and recommend the perfect tool(s) from the "
        "catalog below, explaining WHY it fits and its price. Always recommend by exact tool name. Be concise "
        "(under 130 words), persuasive but honest. If nothing fits, say so.\n\nCATALOG:\n" + tools_summary
    )


@api.post("/assistant/chat")
async def assistant_chat(body: ChatRequest, request: Request):
    user = await get_optional_user(request)
    tools_summary = "\n".join(
        f"- {t['name']} (${t['price']:.0f}, {t['category']}): {t['tagline']}" for t in CATALOG
    )
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"aria_{body.session_id}",
        system_message=_assistant_system(tools_summary),
    ).with_model(*LLM_MODEL)

    await db.chat_messages.insert_one({
        "session_id": body.session_id, "user_id": user["user_id"] if user else None,
        "role": "user", "content": body.message, "created_at": datetime.now(timezone.utc),
    })

    async def gen():
        full = ""
        try:
            async for event in chat.stream_message(UserMessage(text=body.message)):
                if isinstance(event, TextDelta):
                    full += event.content
                    yield event.content
                elif isinstance(event, StreamDone):
                    break
        except Exception:
            logger.exception("assistant stream failed")
            yield "\n[Signal lost — please try again.]"
        await db.chat_messages.insert_one({
            "session_id": body.session_id, "user_id": user["user_id"] if user else None,
            "role": "assistant", "content": full, "created_at": datetime.now(timezone.utc),
        })

    return StreamingResponse(gen(), media_type="text/plain",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ----------------------------- Payments -----------------------------
@api.post("/payments/checkout")
async def create_checkout(body: CheckoutRequest, request: Request):
    if not body.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    user = await get_optional_user(request)
    line_items = []
    resolved = []
    total_cents = 0
    for it in body.items:
        prices = stripe.Price.list(lookup_keys=[it.lookup_key], active=True, limit=1).data
        if not prices:
            raise HTTPException(status_code=400, detail=f"Product unavailable: {it.lookup_key}")
        price = prices[0]
        line_items.append({"price": price.id, "quantity": it.quantity})
        tool = get_tool_by_lookup(it.lookup_key)
        bundle = get_bundle_by_lookup(it.lookup_key)
        pack = get_credit_pack_by_lookup(it.lookup_key)
        total_cents += (price.unit_amount or 0) * it.quantity
        if pack:
            resolved.append({
                "slug": pack["slug"], "name": pack["name"], "lookup_key": it.lookup_key,
                "price": (price.unit_amount or 0) / 100, "quantity": it.quantity,
                "is_credit_pack": True, "credits": pack["credits"],
            })
        elif bundle:
            resolved.append({
                "slug": bundle["slug"], "name": bundle["name"], "lookup_key": it.lookup_key,
                "price": (price.unit_amount or 0) / 100, "quantity": it.quantity,
                "is_bundle": True, "included_slugs": bundle["tool_slugs"],
            })
        else:
            resolved.append({
                "slug": tool["slug"] if tool else it.lookup_key,
                "name": tool["name"] if tool else it.lookup_key,
                "lookup_key": it.lookup_key,
                "price": (price.unit_amount or 0) / 100, "quantity": it.quantity,
                "is_bundle": False, "included_slugs": [tool["slug"]] if tool else [],
            })

    kwargs = dict(
        line_items=line_items,
        mode="payment",
        success_url=f"{body.origin_url}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{body.origin_url}/payment/cancel",
        metadata={"user_id": user["user_id"] if user else ""},
    )
    try:
        session = stripe.checkout.Session.create(**kwargs, managed_payments={"enabled": True})
    except stripe.error.InvalidRequestError as e:
        msg = (getattr(e, "user_message", "") or "").lower()
        if "managed payments" in msg or "ineligible" in msg:
            session = stripe.checkout.Session.create(
                **kwargs, automatic_tax={"enabled": True}, billing_address_collection="required")
        else:
            raise

    await db.payment_transactions.insert_one({
        "session_id": session.id,
        "user_id": user["user_id"] if user else None,
        "user_email": user["email"] if user else None,
        "items": resolved,
        "amount": total_cents / 100,
        "currency": "usd",
        "status": "initiated",
        "payment_status": "pending",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    })
    return {"checkout_url": session.url, "session_id": session.id}


async def fulfill_transaction(session_id: str):
    tx = await db.payment_transactions.find_one({"session_id": session_id})
    if not tx or tx.get("fulfilled"):
        return
    total_credits = 0
    for item in tx.get("items", []):
        if item.get("is_credit_pack"):
            total_credits += item.get("credits", 0) * item.get("quantity", 1)
    if total_credits and tx.get("user_id"):
        await db.users.update_one({"user_id": tx["user_id"]}, {"$inc": {"credits": total_credits}})
    await db.payment_transactions.update_one({"session_id": session_id}, {"$set": {"fulfilled": True}})


@api.get("/payments/status/{session_id}")
async def payment_status(session_id: str):
    record = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
    if not record:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if record.get("payment_status") != "paid":
        try:
            s = stripe.checkout.Session.retrieve(session_id)
            if s.payment_status == "paid" or s.status == "complete":
                await db.payment_transactions.update_one(
                    {"session_id": session_id, "payment_status": {"$ne": "paid"}},
                    {"$set": {"status": "completed", "payment_status": "paid",
                              "stripe_payment_intent_id": s.payment_intent,
                              "updated_at": datetime.now(timezone.utc)}})
                await fulfill_transaction(session_id)
                record = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
        except stripe.error.StripeError:
            pass
    return {"session_id": record["session_id"], "status": record["status"],
            "payment_status": record["payment_status"], "items": record.get("items", []),
            "amount": record.get("amount")}


@api.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")
    obj, t = event["data"]["object"], event["type"]
    if t == "checkout.session.completed":
        await db.payment_transactions.update_one(
            {"session_id": obj["id"], "payment_status": {"$ne": "paid"}},
            {"$set": {"status": "completed", "payment_status": obj.get("payment_status", "paid"),
                      "stripe_payment_intent_id": obj.get("payment_intent"),
                      "updated_at": datetime.now(timezone.utc)}})
        await fulfill_transaction(obj["id"])
    elif t == "checkout.session.expired":
        await db.payment_transactions.update_one(
            {"session_id": obj["id"]},
            {"$set": {"status": "expired", "payment_status": "expired",
                      "updated_at": datetime.now(timezone.utc)}})
    return {"status": "ok"}


# ----------------------------- Library -----------------------------
@api.get("/library")
async def library(user: dict = Depends(get_current_user)):
    txns = await db.payment_transactions.find(
        {"user_id": user["user_id"], "payment_status": "paid"}, {"_id": 0}).to_list(500)
    owned = {}
    for tx in txns:
        for item in tx.get("items", []):
            slugs = item.get("included_slugs") or [item.get("slug")]
            for s in slugs:
                tool = get_tool(s)
                if tool:
                    owned[s] = {
                        "slug": tool["slug"], "name": tool["name"], "tagline": tool["tagline"],
                        "category": tool["category"], "icon": tool["icon"], "price": tool["price"],
                        "purchased_at": tx.get("updated_at"),
                    }
    return list(owned.values())


# ----------------------------- Admin -----------------------------
@api.get("/admin/stats")
async def admin_stats(admin: dict = Depends(require_admin)):
    paid = await db.payment_transactions.find({"payment_status": "paid"}, {"_id": 0}).to_list(2000)
    total_revenue = sum(tx.get("amount", 0) for tx in paid)
    total_orders = len(paid)
    total_users = await db.users.count_documents({})
    total_tools = await db.tools.count_documents({})
    aov = (total_revenue / total_orders) if total_orders else 0

    by_day = {}
    tool_sales = {}
    for tx in paid:
        d = tx.get("updated_at") or tx.get("created_at")
        if isinstance(d, str):
            d = datetime.fromisoformat(d)
        key = d.strftime("%Y-%m-%d") if d else "n/a"
        by_day[key] = by_day.get(key, 0) + tx.get("amount", 0)
        for item in tx.get("items", []):
            ts = tool_sales.setdefault(item["name"], {"name": item["name"], "units": 0, "revenue": 0})
            ts["units"] += item.get("quantity", 1)
            ts["revenue"] += item.get("price", 0) * item.get("quantity", 1)

    revenue_series = [{"date": k, "revenue": round(v, 2)} for k, v in sorted(by_day.items())][-14:]
    top_tools = sorted(tool_sales.values(), key=lambda x: -x["revenue"])[:6]
    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "total_users": total_users,
        "total_tools": total_tools,
        "aov": round(aov, 2),
        "revenue_series": revenue_series,
        "top_tools": top_tools,
    }


@api.get("/admin/orders")
async def admin_orders(admin: dict = Depends(require_admin)):
    txns = await db.payment_transactions.find({}, {"_id": 0}).sort("created_at", -1).to_list(200)
    return txns


# ----------------------------- Startup -----------------------------
async def seed_tools():
    for t in CATALOG:
        await db.tools.update_one({"slug": t["slug"]}, {"$set": t}, upsert=True)


async def seed_admin():
    email = os.environ.get("ADMIN_EMAIL", "admin@example.com").lower()
    password = os.environ.get("ADMIN_PASSWORD", "admin123")
    existing = await db.users.find_one({"email": email})
    if not existing:
        await db.users.insert_one({
            "user_id": f"user_{uuid.uuid4().hex[:12]}", "email": email, "name": "Emporium Admin",
            "password_hash": hash_password(password), "role": "admin",
            "auth_provider": "password", "created_at": datetime.now(timezone.utc),
        })
    else:
        updates = {}
        if not existing.get("password_hash") or not verify_password(password, existing["password_hash"]):
            updates["password_hash"] = hash_password(password)
        if existing.get("role") != "admin":
            updates["role"] = "admin"
        if updates:
            await db.users.update_one({"email": email}, {"$set": updates})


async def seed_reviews():
    if await db.reviews.count_documents({}) > 0:
        return
    for slug, revs in SAMPLE_REVIEWS.items():
        for name, rating, comment in revs:
            await db.reviews.insert_one({
                "tool_slug": slug, "user_id": f"seed_{uuid.uuid4().hex[:8]}",
                "user_name": name, "rating": rating, "comment": comment, "verified": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })


@app.on_event("startup")
async def startup():
    await db.users.create_index("email", unique=True)
    await db.users.create_index("user_id", unique=True)
    await db.user_sessions.create_index("session_token")
    await db.tools.create_index("slug", unique=True)
    await db.payment_transactions.create_index("session_id")
    await seed_tools()
    await seed_admin()
    await seed_reviews()
    logger.info("Emporium startup complete: seeded %d tools", len(CATALOG))


app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown():
    client.close()
