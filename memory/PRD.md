# AI Tool Emporium — PRD & Roadmap

## Original Problem Statement
Build "AI Tool Emporium" — an online marketplace that sells packaged AI assistance tools across all major industries (a "Harbor Freight for AI tools"). One-stop shop, interactive & fun, real insight/usage for buyers, full marketing/branding package, and sales tracking. Aesthetic: high-tech, cyber, futuristic, JARVIS / Call of Duty Advanced Warfare — the AI should sell the AI products in the most futuristic way.

## User Choices
- Payments: Stripe (claimable sandbox, tax mode = full/SMP — Stripe manages tax).
- Auth: JWT email/password + Emergent-managed Google OAuth (unified session_token cookie).
- Live interactive AI demos on tool pages.
- Admin sales dashboard.
- Branding: JARVIS / COD Advanced Warfare — cyber, interstellar, HUD. Official logo provided by user (3D metallic "AI" monogram) — used site-wide.

## Architecture
- Frontend: React 19 + CRACO + Tailwind, framer-motion, recharts, lucide-react. HUD/glassmorphism theme (Rajdhani/Orbitron/JetBrains Mono).
- Backend: FastAPI + Motor (MongoDB). All routes under /api.
- AI: Emergent LLM key, Claude Sonnet 4.6 (claude-sonnet-4-6) for ARIA assistant (streaming) + live tool demos (single-shot).
- Payments: Stripe claimable sandbox; catalog synced via setup_stripe.py (tools + bundles), lookup_key based.

## User Personas
- Solopreneurs, small agencies, indie builders who need an AI tool *today* — value-priced, low friction, try-before-buy.
- Owner/Admin — tracks revenue, orders, top tools via Command Center.

## Core Requirements (static)
- Browse/search/filter AI tools across 12 industries; tool detail with live AI demo.
- ARIA JARVIS-style AI concierge that recommends & sells tools.
- Cart + Stripe checkout; library of owned tools.
- Admin dashboard (revenue, orders, AOV, top tools, transactions).
- Full brand kit page.

## Implemented (2026-06-18)
- **AI Studio (live, credit-metered)** — real working AI on the Emergent Universal Key: Image generation (gpt-image-1), Text (ChatGPT gpt-5.4 / Claude Sonnet 4.6 toggle), Research (LLM synthesis). Glowing HUD studio at /studio (auth-gated).
- **Credits system + profit-safe economics**: 30 free credits on signup; per-generation costs text=2/research=4/image=15; atomic guarded deduction (never negative). Stripe **credit packs** (Spark 120/$9, Pro 350/$19, Studio 800/$29) — priced so even the cheapest bulk credit ($0.036) keeps ~3.4x+ markup over worst-case key cost. Credits auto-fulfilled on paid (idempotent).
- **Glowing holographic tool icons** (rotating light-sweep ring + drop-shadow glow) site-wide; navbar credits chip + AI Studio nav + home CTA.
- Verified: testing agent 74/74 backend + all frontend Studio/credits/regression flows.
- **65 AI tools across 31 industries** (seeded) incl. logistics/freight, healthcare, HR, software, finance, legal, cybersecurity, manufacturing, construction, insurance, media, audio, gaming, agriculture, energy, automotive, real estate, e-commerce, research, accounting, productivity + **Everyday Life** (8 affordable $9–$29 personal daily-use tools). Categories with live counts.
- Homepage **"Everyday AI" marketing band** stressing AI for everyday people/daily efficiency; hero stats 65+/30+.
- Site-wide **dark-background logo** (hero lockup + navbar/footer/auth mark tile) — replaced stark-white version.
- Home (hero + logo, stats, features, categories, featured), Marketplace (search/sort/filter), Tool Detail (capabilities + live AI simulation).
- ARIA streaming assistant (recommends tools).
- Auth: register/login (JWT session), Google OAuth callback, admin seed. Unified session_token cookie.
- Cart + Stripe checkout (multi-line-item), payment success polling, library.
- Admin Command Center (recharts area + bar + orders table); role-gated.
- Brand Kit page (official logo lockup + mark, palette, typography, voice, taglines).
- Site-wide official logo (navbar, footer, auth, hero, brand kit, favicon).
- **Quality Tiers (Bronze/Silver/Gold)** + speed/quality + "Why pick this one?" per tool.
- **Value Bundles / starter packs** (4 bundles, discounted, Stripe priced; library grants included tools).
- **Ratings & Reviews** (verified-owner badge, seeded sample reviews, average shown on cards/detail).

## Backlog / Roadmap (from owner's business strategy)
### P1 — Monetization depth (next phase)
- Subscription passes via Stripe: Free (50 credits/mo), Pro $19/mo (10x credits + priority), Studio $79/mo (team seats, API keys).
- Credits system + usage meter (cost-per-task shown upfront); choose credit-metered vs one-time (owner to decide: likely BOTH).
- User dashboard: credit balance, usage history, billing/invoices.
### P2 — Growth & moat
- Affiliate/reseller routing (OpenAI/Anthropic/RunwayML/Midjourney) with 20–35% margin — REQUIRES vendor API keys/accounts (documented, not built).
- Unified API gateway (route to correct vendor, auth, meter usage).
- White-label / API licensing for embedding the catalog.
- SEO landing pages ("best cheap ChatGPT alternative", etc.), affiliate codes for creators.
- Community: user tips, richer review moderation, "Consumer Reports of AI" editorial comparisons.
### Positioning (guiding principle)
- Sell *access & curation*, not features. Price 10–40% below native SaaS. Bundle aggressively. Be obsessively honest about which tool wins for which job. Become the Amazon/Consumer-Reports of AI tools.
- Y1 targets (owner): 5k active users, ~$800 LTV, ~$4M gross, 60–70% margin.

## Next Action Items
- Phase 2: subscriptions + credits + usage meters + user billing dashboard.
- Wire affiliate/vendor routing once vendor keys are available.
