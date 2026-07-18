"""Shared AI tool catalog. Used by server.py (Mongo seed) and setup_stripe.py (Stripe prices)."""

CATEGORIES = [
    {"id": "marketing", "name": "Marketing", "icon": "Megaphone"},
    {"id": "sales", "name": "Sales", "icon": "TrendingUp"},
    {"id": "content", "name": "Content", "icon": "PenTool"},
    {"id": "software", "name": "Software", "icon": "Code2"},
    {"id": "finance", "name": "Finance", "icon": "LineChart"},
    {"id": "healthcare", "name": "Healthcare", "icon": "HeartPulse"},
    {"id": "legal", "name": "Legal", "icon": "Scale"},
    {"id": "education", "name": "Education", "icon": "GraduationCap"},
    {"id": "hr", "name": "Human Resources", "icon": "Users"},
    {"id": "support", "name": "Customer Support", "icon": "Headset"},
    {"id": "data", "name": "Data & Analytics", "icon": "Database"},
    {"id": "design", "name": "Branding & Design", "icon": "Sparkles"},
]


def _tool(slug, name, tagline, category, price, icon, badge, rating, users, features,
          demo_label, demo_placeholder, demo_system):
    return {
        "slug": slug,
        "name": name,
        "tagline": tagline,
        "category": category,
        "price": float(price),
        "amount_cents": int(round(price * 100)),
        "lookup_key": f"tool_{slug}",
        "icon": icon,
        "badge": badge,
        "rating": rating,
        "users": users,
        "features": features,
        "demo_label": demo_label,
        "demo_placeholder": demo_placeholder,
        "demo_system": demo_system,
    }


CATALOG = [
    _tool("neurocopy", "NeuroCopy", "High-converting ad copy in seconds", "marketing", 49,
          "Megaphone", "Bestseller", 4.9, 18420,
          ["Facebook / Google / TikTok ad variants", "Tone & audience targeting", "A/B headline generator", "Unlimited regenerations"],
          "Describe your product & audience",
          "e.g. A sleep supplement for busy professionals aged 30-45",
          "You are NeuroCopy, an elite direct-response advertising AI. Given a product description, generate 3 punchy ad variants (headline + primary text + CTA) optimized for conversion. Be bold, benefit-driven and concise. Format cleanly with labels."),
    _tool("leadhawk", "LeadHawk", "Cold outreach that actually gets replies", "sales", 59,
          "TrendingUp", "Hot", 4.8, 9310,
          ["Personalized cold emails", "Follow-up sequences", "Objection handling", "LinkedIn DM scripts"],
          "Describe your prospect & offer",
          "e.g. Selling HR software to Series A startup founders",
          "You are LeadHawk, a B2B sales outreach specialist. Given a prospect and offer, write a concise, personalized cold email (subject + body) plus one follow-up. Focus on the prospect's pain, keep it under 120 words, human and non-salesy."),
    _tool("storyforge", "StoryForge", "Long-form articles that rank & read", "content", 49,
          "PenTool", None, 4.7, 12750,
          ["SEO-optimized blog posts", "Custom tone of voice", "Auto outline & sections", "Plagiarism-safe originality"],
          "What should the article be about?",
          "e.g. The future of remote work in 2026",
          "You are StoryForge, a professional long-form content writer. Given a topic, produce a well-structured article excerpt with an H1, a compelling intro, and 2-3 subheadings with rich paragraphs. Engaging, authoritative, SEO-aware."),
    _tool("codepilot-x", "CodePilot X", "Your AI pair programmer & debugger", "software", 79,
          "Code2", "Pro", 4.9, 22100,
          ["Multi-language code generation", "Bug detection & fixes", "Refactor suggestions", "Test generation"],
          "Paste code or describe what you need",
          "e.g. Write a Python function to debounce API calls",
          "You are CodePilot X, an expert senior software engineer. Given a coding request or a snippet, return clean, production-ready code in a fenced block plus a short explanation. If given buggy code, identify the bug and fix it."),
    _tool("ledgermind", "LedgerMind", "Turn raw numbers into clear insight", "finance", 99,
          "LineChart", None, 4.6, 5400,
          ["Financial statement analysis", "Cashflow summaries", "Plain-English reporting", "Risk flagging"],
          "Paste financials or ask a question",
          "e.g. Revenue up 12% but margin fell 4% — what's happening?",
          "You are LedgerMind, a CFA-level financial analyst. Given financial data or a question, provide a crisp analysis with key metrics, trends, and 2-3 actionable insights. Use plain English an executive can act on."),
    _tool("mediscribe", "MediScribe", "Clinical notes, summarized instantly", "healthcare", 149,
          "HeartPulse", "Enterprise", 4.8, 3120,
          ["SOAP note generation", "Patient summary drafting", "Medical terminology aware", "HIPAA-minded outputs"],
          "Paste consultation notes",
          "e.g. Patient presents with persistent cough for 2 weeks...",
          "You are MediScribe, a clinical documentation assistant. Given consultation notes, produce a structured SOAP note (Subjective, Objective, Assessment, Plan). Be precise and professional. Add a disclaimer that outputs must be reviewed by a licensed clinician."),
    _tool("lexdraft", "LexDraft", "Draft & simplify legal clauses", "legal", 129,
          "Scale", None, 4.7, 4210,
          ["Contract clause drafting", "Plain-English translation", "Risk highlighting", "Multi-jurisdiction aware"],
          "Describe the clause you need",
          "e.g. A mutual NDA confidentiality clause for a SaaS deal",
          "You are LexDraft, a legal drafting assistant. Given a request, draft a clear, professional clause and follow it with a plain-English explanation. Add a note that this is not legal advice and should be reviewed by a licensed attorney."),
    _tool("tutorcore", "TutorCore", "Lessons & quizzes on any topic", "education", 39,
          "GraduationCap", None, 4.8, 15600,
          ["Lesson plan generation", "Auto quiz & answer keys", "Grade-level adaptation", "Interactive explanations"],
          "What do you want to teach?",
          "e.g. Explain photosynthesis for 7th graders with a quiz",
          "You are TutorCore, an expert teacher. Given a topic and level, produce a short lesson with a clear explanation, one worked example, and a 3-question quiz with answers. Adapt language to the grade level."),
    _tool("talentsift", "TalentSift", "Screen resumes & write JDs fast", "hr", 69,
          "Users", "Hot", 4.6, 6800,
          ["Resume screening & scoring", "Job description writer", "Bias-aware language", "Interview question generator"],
          "Paste a JD or resume, or describe a role",
          "e.g. Write a JD for a senior React developer, remote",
          "You are TalentSift, an HR & recruiting AI. Depending on the input, either write a compelling, inclusive job description, or screen a resume against a role with a fit score and rationale. Be structured and unbiased."),
    _tool("helpsphere", "HelpSphere", "Perfect support replies, on brand", "support", 49,
          "Headset", None, 4.7, 8900,
          ["Empathetic reply drafting", "Tone & brand matching", "Multi-language support", "Escalation summaries"],
          "Paste the customer message",
          "e.g. Customer is angry their order arrived damaged",
          "You are HelpSphere, a customer support specialist. Given a customer message, draft a warm, empathetic, solution-focused reply. Acknowledge feelings, provide a clear next step, and keep the brand professional and friendly."),
    _tool("dataseer", "DataSeer", "Ask your data in plain English", "data", 89,
          "Database", "Pro", 4.8, 7300,
          ["Natural language to SQL", "Chart recommendations", "Insight narratives", "Data cleaning tips"],
          "Describe your data question",
          "e.g. Show total sales by region for last quarter (SQL)",
          "You are DataSeer, a data analyst AI. Given a question about data, produce the SQL query (in a fenced block) and a short explanation of what it returns and how to visualize it. Assume standard table names if none are given."),
    _tool("brandforge", "BrandForge", "Names, taglines & identity kits", "design", 59,
          "Sparkles", "Bestseller", 4.9, 19800,
          ["Brand name generator", "Tagline & mission writer", "Voice & tone guide", "Color palette suggestions"],
          "Describe your brand or business",
          "e.g. A premium coffee subscription for developers",
          "You are BrandForge, a branding strategist. Given a business idea, generate 3 brand name options, a tagline for each, a short brand voice description, and a suggested color palette (with hex codes). Be creative and cohesive."),
    _tool("pitchdeck-ai", "PitchDeck AI", "Investor-ready pitches & proposals", "sales", 99,
          "TrendingUp", None, 4.7, 5100,
          ["Pitch deck outlines", "Proposal drafting", "Value proposition framing", "Objection pre-handling"],
          "Describe your company & ask",
          "e.g. Seed pitch for an AI logistics startup",
          "You are PitchDeck AI, a startup pitch expert. Given a company description, produce a slide-by-slide pitch outline (Problem, Solution, Market, Product, Traction, Ask) with 1-2 punchy lines per slide."),
    _tool("socialpulse", "SocialPulse", "Scroll-stopping social content", "marketing", 39,
          "Megaphone", None, 4.6, 21200,
          ["Captions for every platform", "Trending hashtag sets", "Content calendars", "Hook generator"],
          "What are you posting about?",
          "e.g. Launch of our new fitness app, Instagram",
          "You are SocialPulse, a social media manager. Given a topic and platform, write 3 scroll-stopping caption options with strong hooks, appropriate emojis, and a set of relevant hashtags."),
    _tool("translatewave", "TranslateWave", "Fluent localization, not literal", "content", 49,
          "PenTool", None, 4.8, 9600,
          ["50+ languages", "Tone & context aware", "Idiom-safe translation", "Cultural localization notes"],
          "Paste text + target language",
          "e.g. Translate 'Grand opening this weekend!' to Spanish",
          "You are TranslateWave, an expert localizer. Translate the given text into the requested language naturally (not literally), preserving tone and intent. Add a one-line note on any cultural adaptation you made."),
    _tool("resumerocket", "ResumeRocket", "Land interviews with sharper resumes", "hr", 29,
          "Users", "Popular", 4.7, 24500,
          ["Resume bullet rewriting", "ATS keyword optimization", "Cover letter drafting", "Achievement quantifier"],
          "Paste a bullet or describe your role",
          "e.g. Rewrite: 'Responsible for managing the sales team'",
          "You are ResumeRocket, a career coach. Given resume content or a role, rewrite it into strong, quantified, achievement-focused bullet points optimized for ATS. Punchy and results-driven."),
    _tool("emailgenie", "EmailGenie", "Newsletters your list opens", "marketing", 49,
          "Megaphone", None, 4.6, 11300,
          ["Newsletter drafting", "Subject line optimizer", "Segmented tone control", "CTA optimization"],
          "What's the email about?",
          "e.g. Weekly newsletter announcing a 20% flash sale",
          "You are EmailGenie, an email marketing pro. Given a topic, write a complete email: 3 subject line options, a preview line, and a well-structured body with a strong CTA. Skimmable and persuasive."),
    _tool("seosensei", "SEOSensei", "Rank higher with smarter SEO", "marketing", 69,
          "Megaphone", "Pro", 4.8, 13400,
          ["Keyword clustering", "Meta title & description", "Content gap analysis", "SERP-intent matching"],
          "Enter your topic or target keyword",
          "e.g. best running shoes for flat feet",
          "You are SEOSensei, an SEO strategist. Given a topic or keyword, return: a primary keyword, 5 related long-tail keywords, an optimized meta title (<60 chars) and meta description (<155 chars), and 3 content angle ideas."),
]


def get_tool(slug):
    for t in CATALOG:
        if t["slug"] == slug:
            return t
    return None


def get_tool_by_lookup(lookup_key):
    for t in CATALOG:
        if t["lookup_key"] == lookup_key:
            return t
    return None


# ------------------ Quality tiers + "Why pick this one?" ------------------
# tier, speed, quality, why
TIER_META = {
    "neurocopy": ("Gold", "Fast", "Best-in-class", "The workhorse for ad copy — conversion-tested structures at speed. Pick it when volume AND punch both matter."),
    "leadhawk": ("Silver", "Fast", "High quality", "Best for reply rates, not word count. Choose it when personalization beats mass-blasting."),
    "storyforge": ("Silver", "Deep", "High quality", "Trades a little speed for structure and depth. Pick it for long-form that actually ranks."),
    "codepilot-x": ("Gold", "Fast", "Best-in-class", "Deepest reasoning of the dev tools. Choose it for real debugging, not just autocomplete."),
    "ledgermind": ("Gold", "Deep", "Best-in-class", "Executive-grade analysis over raw speed. Pick it when the numbers need a story, not just a summary."),
    "mediscribe": ("Gold", "Deep", "Enterprise-grade", "Highest precision, clinician-reviewed outputs. Choose it when accuracy is non-negotiable."),
    "lexdraft": ("Gold", "Deep", "Best-in-class", "Draft + plain-English explain in one pass. Pick it when clarity and defensibility both count."),
    "tutorcore": ("Bronze", "Instant", "Good enough", "Fastest, most affordable way to build lessons. Pick it for high volume at low cost."),
    "talentsift": ("Silver", "Fast", "High quality", "Balanced screening + JD writing. Choose it to move fast without bias creeping in."),
    "helpsphere": ("Silver", "Instant", "High quality", "Near-instant, on-brand replies. Pick it for support teams that live in the queue."),
    "dataseer": ("Gold", "Fast", "Best-in-class", "SQL + narrative + viz advice together. Choose it when you need the answer, not just the query."),
    "brandforge": ("Silver", "Fast", "High quality", "Names, voice and palette in one shot. Pick it to go from idea to identity in minutes."),
    "pitchdeck-ai": ("Gold", "Deep", "Best-in-class", "Investor-framed narratives, not just bullet points. Choose it when the raise is on the line."),
    "socialpulse": ("Bronze", "Instant", "Good enough", "Cheapest way to never run out of posts. Pick it for daily volume across platforms."),
    "translatewave": ("Silver", "Fast", "High quality", "Localizes meaning, not words. Choose it when tone and culture must survive translation."),
    "resumerocket": ("Bronze", "Instant", "Good enough", "Lowest price, fastest wins. Pick it to sharpen a resume in one sitting."),
    "emailgenie": ("Silver", "Fast", "High quality", "Subject lines + body + CTA together. Choose it to lift open and click rates."),
    "seosensei": ("Gold", "Fast", "Best-in-class", "Keyword clusters + intent + meta in one pass. Pick it to actually move rankings."),
}

for _t in CATALOG:
    _tier, _speed, _quality, _why = TIER_META.get(_t["slug"], ("Silver", "Fast", "High quality", ""))
    _t["tier"] = _tier
    _t["speed"] = _speed
    _t["quality_tier"] = _quality
    _t["why"] = _why


# ------------------ Value bundles / starter packs ------------------
def _bundle(slug, name, tagline, icon, tool_slugs, price, badge=None):
    original = sum(get_tool(s)["price"] for s in tool_slugs)
    return {
        "slug": slug,
        "name": name,
        "tagline": tagline,
        "icon": icon,
        "tool_slugs": tool_slugs,
        "price": float(price),
        "original_price": round(original, 2),
        "amount_cents": int(round(price * 100)),
        "lookup_key": f"bundle_{slug}",
        "savings_pct": round((1 - price / original) * 100) if original else 0,
        "badge": badge,
        "is_bundle": True,
    }


BUNDLES = [
    _bundle("creator-pack", "Creator Pack", "Everything to plan, write & publish content that performs.",
            "PenTool", ["storyforge", "socialpulse", "emailgenie"], 99, "Most Popular"),
    _bundle("growth-engine", "Growth Engine", "The full-funnel marketing & sales acquisition stack.",
            "TrendingUp", ["neurocopy", "seosensei", "leadhawk"], 129, "Best Value"),
    _bundle("founders-toolkit", "Founder's Toolkit", "Launch-ready: brand it, pitch it, understand the numbers.",
            "Rocket", ["pitchdeck-ai", "brandforge", "ledgermind"], 179),
    _bundle("career-launch", "Career Launch", "Land the role and hire the team — the people stack.",
            "Users", ["resumerocket", "talentsift", "tutorcore"], 89),
]


def get_bundle(slug):
    for b in BUNDLES:
        if b["slug"] == slug:
            return b
    return None


def get_bundle_by_lookup(lookup_key):
    for b in BUNDLES:
        if b["lookup_key"] == lookup_key:
            return b
    return None


# ------------------ Seed reviews (Consumer-Reports trust layer) ------------------
SAMPLE_REVIEWS = {
    "neurocopy": [("Marcus T.", 5, "Cut our ad-writing time by 80%. The variants actually convert."),
                  ("Priya K.", 5, "Bronze/Silver/Gold framing helped me pick fast. Worth every dollar.")],
    "codepilot-x": [("Dev_Nolan", 5, "Caught a race condition I'd been chasing for two days."),
                    ("Sara L.", 4, "Great for boilerplate and tests. Occasionally over-explains.")],
    "brandforge": [("Jenna R.", 5, "Named my whole company in an afternoon. The palette suggestions slap.")],
    "seosensei": [("GrowthGuy", 5, "Ranked page one in 6 weeks using its keyword clusters."),
                  ("Ana M.", 4, "Solid meta output. Wish it exported to CSV.")],
    "resumerocket": [("Tyler B.", 5, "Three interviews in a week after the rewrite. Insane ROI for $29.")],
    "pitchdeck-ai": [("FounderFi", 5, "Used it for our seed deck. Investors said the narrative was tight.")],
}
