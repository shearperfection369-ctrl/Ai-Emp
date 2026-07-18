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
    {"id": "logistics", "name": "Logistics & Freight", "icon": "Truck"},
    {"id": "realestate", "name": "Real Estate", "icon": "Building2"},
    {"id": "ecommerce", "name": "E-Commerce & Retail", "icon": "ShoppingBag"},
    {"id": "manufacturing", "name": "Manufacturing", "icon": "Factory"},
    {"id": "construction", "name": "Construction", "icon": "HardHat"},
    {"id": "hospitality", "name": "Hospitality & Travel", "icon": "Plane"},
    {"id": "insurance", "name": "Insurance", "icon": "ShieldCheck"},
    {"id": "cybersecurity", "name": "Cybersecurity", "icon": "ShieldAlert"},
    {"id": "media", "name": "Media & Video", "icon": "Clapperboard"},
    {"id": "audio", "name": "Music & Audio", "icon": "Music"},
    {"id": "gaming", "name": "Gaming", "icon": "Gamepad2"},
    {"id": "agriculture", "name": "Agriculture", "icon": "Sprout"},
    {"id": "energy", "name": "Energy & Utilities", "icon": "Fuel"},
    {"id": "automotive", "name": "Automotive", "icon": "Car"},
    {"id": "fitness", "name": "Fitness & Wellness", "icon": "Dumbbell"},
    {"id": "research", "name": "Research & Science", "icon": "FlaskConical"},
    {"id": "productivity", "name": "Productivity", "icon": "ListChecks"},
    {"id": "accounting", "name": "Accounting & Tax", "icon": "Calculator"},
    {"id": "everyday", "name": "Everyday Life", "icon": "Coffee"},
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

    # ---------------- Logistics & Freight ----------------
    _tool("freightpilot", "FreightPilot", "Instant freight quotes & load optimization", "logistics", 129,
          "Truck", "Enterprise", 4.7, 3400,
          ["Freight rate estimation", "Load consolidation tips", "Carrier selection logic", "Fuel surcharge math"],
          "Describe the shipment", "e.g. 12 pallets, Chicago to Dallas, dry van, this Friday",
          "You are FreightPilot, a freight logistics expert. Given a shipment, estimate a reasonable freight rate range, suggest the best equipment/carrier type, flag consolidation or LTL/FTL options, and note key cost drivers. Add a disclaimer that rates are indicative."),
    _tool("routeforge", "RouteForge", "Optimize routes & fleet efficiency", "logistics", 99,
          "Map", None, 4.6, 2600,
          ["Multi-stop route optimization", "Fleet utilization tips", "ETA & fuel estimates", "Driver-hours awareness"],
          "List your stops or route goal", "e.g. Optimize 8 delivery stops around Atlanta metro",
          "You are RouteForge, a route optimization specialist. Given stops or a routing goal, propose an efficient stop order, estimate distance/time/fuel, and flag constraints (traffic windows, driver hours). Present clearly."),
    _tool("customsclear", "CustomsClear", "Customs docs & trade compliance", "logistics", 149,
          "FileCheck", None, 4.6, 1500,
          ["Commercial invoice drafting", "HS code suggestions", "Incoterms guidance", "Compliance checklist"],
          "Describe the international shipment", "e.g. Exporting electronics from US to Germany",
          "You are CustomsClear, an international trade compliance assistant. Given a shipment, suggest likely HS codes, applicable Incoterms, required documents, and a compliance checklist. Add a disclaimer to verify with a licensed customs broker."),

    # ---------------- Real Estate ----------------
    _tool("listinglift", "ListingLift", "Listings that sell homes faster", "realestate", 39,
          "Building2", "Popular", 4.7, 14200,
          ["MLS-ready descriptions", "Neighborhood highlights", "Feature-to-benefit copy", "Social listing posts"],
          "Describe the property", "e.g. 3bd/2ba craftsman, renovated kitchen, big backyard",
          "You are ListingLift, a real estate copywriter. Given property details, write a compelling MLS listing description plus a short social caption. Highlight lifestyle benefits, stay honest, and follow fair-housing-safe language."),
    _tool("dealscope", "DealScope", "Analyze deals & comps in seconds", "realestate", 99,
          "Home", None, 4.6, 4100,
          ["Comp analysis", "Cap rate & cash flow", "Rehab ROI estimates", "Offer strategy"],
          "Describe the deal", "e.g. Duplex at $320k, rents $1500/unit, needs $20k work",
          "You are DealScope, a real estate investment analyst. Given a deal, estimate cap rate, cash flow, and ROI, and give a clear buy/pass rationale with assumptions stated. Add a disclaimer that this is not financial advice."),

    # ---------------- E-Commerce & Retail ----------------
    _tool("productpitch", "ProductPitch", "Product copy that converts browsers", "ecommerce", 39,
          "ShoppingBag", "Bestseller", 4.8, 20300,
          ["Product descriptions", "SEO bullet points", "Amazon/Shopify formats", "Variant copy at scale"],
          "Describe the product", "e.g. Stainless insulated water bottle, 32oz",
          "You are ProductPitch, an e-commerce copywriter. Given a product, write a persuasive description, 5 benefit-driven bullet points, and an SEO title. Optimized for marketplaces like Shopify and Amazon."),
    _tool("reviewradar", "ReviewRadar", "Turn reviews into insight & replies", "ecommerce", 49,
          "MessagesSquare", None, 4.6, 7600,
          ["Sentiment analysis", "Theme extraction", "On-brand reply drafts", "Product improvement ideas"],
          "Paste customer reviews", "e.g. 'Great product but shipping was slow...'",
          "You are ReviewRadar, a retail insights AI. Given customer reviews, summarize sentiment and key themes, draft an empathetic reply, and suggest 2 product/ops improvements."),
    _tool("priceoptix", "PriceOptix", "Smarter pricing, healthier margins", "ecommerce", 89,
          "Tag", None, 4.5, 3900,
          ["Competitive price analysis", "Bundle & discount strategy", "Margin impact modeling", "Psychological pricing"],
          "Describe your product & goal", "e.g. $45 candle, competitors $38-52, want more volume",
          "You are PriceOptix, a pricing strategist. Given a product and competitive context, recommend a price (or range), a discount/bundle strategy, and explain the margin/volume tradeoff clearly."),

    # ---------------- Manufacturing ----------------
    _tool("shopfloor-ai", "ShopFloor AI", "Production scheduling & OEE insight", "manufacturing", 199,
          "Factory", "Enterprise", 4.7, 1800,
          ["Production scheduling", "OEE analysis", "Bottleneck detection", "Downtime root-cause"],
          "Describe the production issue", "e.g. Line 2 OEE dropped to 68%, frequent changeovers",
          "You are ShopFloor AI, a manufacturing operations expert. Given a production scenario, analyze likely OEE losses (availability/performance/quality), identify bottlenecks, and recommend concrete actions."),
    _tool("maintenancemind", "MaintenanceMind", "Predict failures before they cost you", "manufacturing", 149,
          "Wrench", None, 4.6, 2200,
          ["Predictive maintenance advice", "Failure mode analysis", "PM schedule drafting", "Spare-parts guidance"],
          "Describe the equipment & symptoms", "e.g. Pump vibration rising, bearing temp up 10C",
          "You are MaintenanceMind, a reliability engineer. Given equipment symptoms, suggest likely failure modes, recommended inspections, and a preventive maintenance interval. Add a safety disclaimer."),

    # ---------------- Construction ----------------
    _tool("bidbuilder", "BidBuilder", "Win more jobs with sharper bids", "construction", 99,
          "HardHat", None, 4.6, 3300,
          ["Bid & estimate drafting", "Scope of work writing", "Line-item breakdowns", "Change-order language"],
          "Describe the project", "e.g. Bathroom remodel, 80 sqft, mid-range finishes",
          "You are BidBuilder, a construction estimator. Given a project, draft a clear scope of work and a rough line-item estimate structure with labor/material categories. Add a disclaimer that figures are indicative and require local pricing."),
    _tool("safetyscribe", "SafetyScribe", "Jobsite safety plans in minutes", "construction", 59,
          "TriangleAlert", None, 4.7, 4800,
          ["Toolbox talk generator", "JHA / risk assessments", "OSHA-aware checklists", "Incident report drafting"],
          "Describe the task or hazard", "e.g. Working at heights installing rooftop HVAC",
          "You are SafetyScribe, a construction safety specialist. Given a task, produce a concise toolbox talk and a hazard checklist with controls. Keep it OSHA-minded and add a note to follow site-specific procedures."),

    # ---------------- Hospitality & Travel ----------------
    _tool("itineraryai", "ItineraryAI", "Custom trips your guests will love", "hospitality", 29,
          "Plane", "Popular", 4.8, 18900,
          ["Day-by-day itineraries", "Local recommendations", "Budget tiers", "Group & family options"],
          "Describe the trip", "e.g. 4 days in Kyoto for a couple, food & culture focus",
          "You are ItineraryAI, an expert travel planner. Given a trip request, build a day-by-day itinerary with morning/afternoon/evening suggestions, local tips, and a rough budget note. Engaging and practical."),
    _tool("conciergebot", "ConciergeBot", "Five-star guest replies, instantly", "hospitality", 49,
          "BellRing", None, 4.6, 5200,
          ["Guest inquiry responses", "Upsell messaging", "Multilingual replies", "Review response drafts"],
          "Paste the guest message", "e.g. Guest asks for late checkout and restaurant tips",
          "You are ConciergeBot, a luxury hospitality concierge. Given a guest message, write a warm, professional reply that solves the request and tastefully upsells when appropriate."),

    # ---------------- Insurance ----------------
    _tool("claimclarity", "ClaimClarity", "Triage & summarize claims fast", "insurance", 149,
          "ShieldCheck", "Enterprise", 4.6, 2100,
          ["Claim summarization", "Coverage triage", "Fraud-flag heuristics", "Adjuster note drafting"],
          "Paste claim details", "e.g. Rear-end collision, minor injury, disputed fault",
          "You are ClaimClarity, an insurance claims assistant. Given claim details, produce a structured summary, note coverage/triage considerations, flag anything unusual, and draft an adjuster note. Add a disclaimer to follow policy and legal review."),
    _tool("policypal", "PolicyPal", "Explain policies & draft quotes", "insurance", 79,
          "FileText", None, 4.5, 4300,
          ["Plain-English policy explainer", "Quote drafting", "Coverage comparison", "Renewal messaging"],
          "Paste policy text or ask", "e.g. What does this deductible clause actually mean?",
          "You are PolicyPal, an insurance explainer. Given policy text or a question, explain it in plain English, highlight key coverage/limits, and note what to double-check. Add a disclaimer to confirm with the insurer."),

    # ---------------- Cybersecurity ----------------
    _tool("threatlens", "ThreatLens", "Triage alerts & summarize incidents", "cybersecurity", 199,
          "ShieldAlert", "Pro", 4.8, 6100,
          ["Log & alert triage", "Incident summaries", "MITRE ATT&CK mapping", "Remediation steps"],
          "Paste an alert or log snippet", "e.g. Multiple failed logins then success from new IP",
          "You are ThreatLens, a SOC analyst AI. Given an alert or log, assess likely severity, map to MITRE ATT&CK techniques where relevant, and recommend triage + remediation steps. Concise and actionable."),
    _tool("phishguard", "PhishGuard", "Spot phishing & train your team", "cybersecurity", 89,
          "Lock", None, 4.7, 8800,
          ["Phishing email analysis", "Red-flag explanations", "Simulation email writing", "Awareness tips"],
          "Paste the suspicious email", "e.g. 'Your account is locked, click here to verify'",
          "You are PhishGuard, a phishing-detection expert. Given an email, rate its phishing likelihood, list the specific red flags, and give the user a clear recommended action."),

    # ---------------- Media & Video ----------------
    _tool("scriptforge", "ScriptForge", "Video scripts that hold attention", "media", 49,
          "Clapperboard", "Bestseller", 4.8, 16400,
          ["YouTube & ad scripts", "Hook & retention beats", "Shot list drafting", "CTA optimization"],
          "What's the video about?", "e.g. 60s ad for a productivity app, energetic tone",
          "You are ScriptForge, a video scriptwriter. Given a topic and format, write a tight script with a strong hook, clear beats, and a CTA. Note suggested shots/visuals in brackets."),
    _tool("thumbnailgenius", "ThumbnailGenius", "Thumbnails & titles that get clicks", "media", 39,
          "Image", None, 4.6, 12100,
          ["Thumbnail concepts", "Click-worthy titles", "A/B title variants", "Text overlay ideas"],
          "Describe your video", "e.g. Tutorial: build a PC for gaming under $800",
          "You are ThumbnailGenius, a YouTube growth expert. Given a video, propose 3 thumbnail concepts (composition + overlay text) and 5 high-CTR title options. Punchy, curiosity-driven, honest."),
    _tool("subtitlewave", "SubtitleWave", "Transcripts & subtitles, done", "media", 59,
          "Captions", None, 4.7, 6900,
          ["Transcription cleanup", "Subtitle formatting", "Translation-ready output", "Chapter markers"],
          "Paste a transcript or describe", "e.g. Clean up this raw interview transcript",
          "You are SubtitleWave, a captioning assistant. Given transcript text, clean it into readable, well-punctuated subtitle lines and suggest chapter markers. Keep timing-friendly line lengths."),

    # ---------------- Music & Audio ----------------
    _tool("lyriclab", "LyricLab", "Co-write lyrics in any style", "audio", 29,
          "Music", "Popular", 4.7, 15300,
          ["Lyric writing", "Rhyme & meter help", "Genre matching", "Hook generation"],
          "Describe the song", "e.g. Upbeat pop song about starting over, hopeful",
          "You are LyricLab, a songwriter. Given a theme and style, write a verse and a catchy chorus with consistent meter and rhyme. Evocative and singable."),
    _tool("podpro", "PodPro", "Podcast notes & clips on autopilot", "audio", 49,
          "Mic", None, 4.6, 5700,
          ["Show notes generation", "Timestamped highlights", "Clip suggestions", "Episode titles"],
          "Paste episode transcript or topic", "e.g. Episode on remote-work burnout",
          "You are PodPro, a podcast producer. Given a transcript or topic, write engaging show notes, 3 pull-quote clip ideas, and 3 episode title options."),

    # ---------------- Gaming ----------------
    _tool("questforge", "QuestForge", "Design quests & game narratives", "gaming", 59,
          "Gamepad2", None, 4.7, 7200,
          ["Quest & mission design", "Branching narratives", "Lore & world-building", "Objective balancing"],
          "Describe your game & quest goal", "e.g. Fantasy RPG, a side quest about a cursed village",
          "You are QuestForge, a game narrative designer. Given a game and goal, design a quest with hook, objectives, branching choices, and a reward. Immersive and player-driven."),
    _tool("npcmind", "NPCMind", "Believable NPC dialogue at scale", "gaming", 49,
          "Bot", None, 4.6, 6400,
          ["NPC dialogue trees", "Personality & voice", "Barks & ambient lines", "Faction-aware tone"],
          "Describe the NPC & context", "e.g. Gruff blacksmith in a war-torn town",
          "You are NPCMind, a game dialogue writer. Given an NPC and context, write a short dialogue tree with personality-consistent lines and 3 ambient barks."),

    # ---------------- Agriculture ----------------
    _tool("cropsense", "CropSense", "Data-driven crop planning", "agriculture", 99,
          "Sprout", None, 4.6, 2400,
          ["Crop rotation planning", "Planting windows", "Yield optimization tips", "Input recommendations"],
          "Describe your field & goal", "e.g. 40 acres, corn last year, sandy loam soil",
          "You are CropSense, an agronomy advisor. Given field details, recommend a crop rotation, planting window, and key input considerations, with rationale. Add a note to confirm with local extension services."),
    _tool("agriscout", "AgriScout", "Diagnose pests & plant disease", "agriculture", 79,
          "Leaf", None, 4.5, 3100,
          ["Pest & disease ID guidance", "Treatment options", "Prevention tips", "Severity assessment"],
          "Describe the symptoms", "e.g. Yellow spots spreading on tomato leaves",
          "You are AgriScout, a plant-health specialist. Given symptoms, suggest likely causes (pest/disease/deficiency), treatment options, and prevention. Add a disclaimer to confirm with an agronomist."),

    # ---------------- Energy & Utilities ----------------
    _tool("gridgenius", "GridGenius", "Forecast demand & optimize load", "energy", 199,
          "Fuel", "Enterprise", 4.6, 1400,
          ["Demand forecasting", "Load-balancing insight", "Peak-shaving strategy", "Cost/emissions tradeoffs"],
          "Describe the scenario", "e.g. Commercial site, summer peak demand charges high",
          "You are GridGenius, an energy analyst. Given a scenario, explain demand drivers, suggest load-shifting/peak-shaving strategies, and note cost/emissions tradeoffs."),
    _tool("solarsage", "SolarSage", "Solar sizing & ROI reports", "energy", 89,
          "Sun", None, 4.7, 4600,
          ["System sizing estimates", "ROI & payback math", "Incentive guidance", "Homeowner-ready summaries"],
          "Describe the site & bill", "e.g. Home in Arizona, $220/mo electric, south-facing roof",
          "You are SolarSage, a solar consultant. Given a site and bill, estimate a reasonable system size, rough cost, payback period, and note common incentives. Add a disclaimer to get a certified quote."),

    # ---------------- Automotive ----------------
    _tool("autodiag", "AutoDiag", "Diagnose car issues like a pro", "automotive", 69,
          "Car", "Popular", 4.7, 9900,
          ["Symptom-based diagnosis", "OBD code explanations", "Repair cost ranges", "DIY vs shop guidance"],
          "Describe the car problem", "e.g. 2015 Civic, rough idle and check-engine light",
          "You are AutoDiag, a master mechanic. Given a car and symptoms, list likely causes ranked by probability, explain any codes, give rough repair cost ranges, and advise DIY vs professional. Add a safety disclaimer."),
    _tool("dealerdesk", "DealerDesk", "Sell cars faster with sharp copy", "automotive", 59,
          "Gauge", None, 4.5, 3800,
          ["Vehicle listing copy", "Lead follow-up messages", "Trade-in talking points", "Finance explainers"],
          "Describe the vehicle & buyer", "e.g. Certified 2021 F-150, family shopping for towing",
          "You are DealerDesk, an auto sales assistant. Given a vehicle and buyer, write a compelling listing and a personalized follow-up message focused on the buyer's needs."),

    # ---------------- Fitness & Wellness ----------------
    _tool("fitforge", "FitForge", "Personalized workouts & meal plans", "fitness", 29,
          "Dumbbell", "Bestseller", 4.8, 26800,
          ["Custom workout plans", "Macro & meal planning", "Progression tracking tips", "Injury-aware options"],
          "Describe your goal", "e.g. Build muscle, 4 days/week, gym access, beginner",
          "You are FitForge, a certified fitness coach. Given goals and constraints, build a weekly workout split and a simple meal/macro guideline. Add a disclaimer to consult a professional before starting."),
    _tool("mindfulai", "MindfulAI", "Guided meditation & wellness scripts", "fitness", 19,
          "HeartPulse", None, 4.7, 12400,
          ["Meditation scripts", "Breathwork guides", "Journaling prompts", "Stress-relief routines"],
          "What do you need today?", "e.g. A 5-minute calming meditation for anxiety",
          "You are MindfulAI, a mindfulness guide. Given a need, write a soothing, well-paced script (meditation/breathwork/journaling). Warm, grounding, and safe; note it's not a substitute for professional care."),

    # ---------------- Research & Science ----------------
    _tool("paperpilot", "PaperPilot", "Summarize papers & lit reviews", "research", 99,
          "FlaskConical", "Pro", 4.8, 8700,
          ["Paper summarization", "Literature reviews", "Method critique", "Citation-ready notes"],
          "Paste abstract or topic", "e.g. Summarize key findings on gut microbiome & mood",
          "You are PaperPilot, a research assistant. Given an abstract or topic, produce a structured summary (aim, method, findings, limitations) and note open questions. Precise and academic; flag when claims need source verification."),
    _tool("hypothesisai", "HypothesisAI", "Design rigorous experiments", "research", 129,
          "Microscope", None, 4.6, 3200,
          ["Experiment design", "Variable & control setup", "Sample size intuition", "Bias mitigation"],
          "Describe your research question", "e.g. Does a new UI increase signup conversion?",
          "You are HypothesisAI, a research methodologist. Given a question, propose a clear hypothesis, variables, controls, a suitable design, and sample-size considerations. Rigorous and practical."),

    # ---------------- Productivity ----------------
    _tool("meetingscribe", "MeetingScribe", "Meeting notes & action items, auto", "productivity", 39,
          "ListChecks", "Popular", 4.7, 22100,
          ["Meeting summaries", "Action-item extraction", "Decision logging", "Follow-up email drafts"],
          "Paste meeting notes or transcript", "e.g. Weekly standup transcript with 3 blockers",
          "You are MeetingScribe, a productivity assistant. Given meeting notes, produce a crisp summary, a bulleted action-item list with owners, key decisions, and a follow-up email draft."),
    _tool("inboxzero-ai", "InboxZero AI", "Triage & draft email in seconds", "productivity", 29,
          "Inbox", None, 4.6, 17600,
          ["Email triage & priority", "Reply drafting", "Tone adjustment", "Summarize long threads"],
          "Paste the email or thread", "e.g. Long client thread negotiating a deadline",
          "You are InboxZero AI, an email productivity assistant. Given an email or thread, summarize it, suggest a priority, and draft a clear, professional reply matching the requested tone."),

    # ---------------- Accounting & Tax ----------------
    _tool("bookkeepbot", "BookkeepBot", "Clean books without the headache", "accounting", 79,
          "Calculator", None, 4.6, 6300,
          ["Transaction categorization", "Monthly summaries", "Anomaly flagging", "Cashflow narratives"],
          "Paste transactions or ask", "e.g. Categorize: 'AWS $340, Uber $22, Staples $88'",
          "You are BookkeepBot, a bookkeeping assistant. Given transactions, categorize them into standard accounts, summarize by category, and flag anything unusual. Add a disclaimer to have a CPA review."),
    _tool("taxtactician", "TaxTactician", "Find deductions, explain the rules", "accounting", 99,
          "Receipt", "Pro", 4.7, 7100,
          ["Deduction discovery", "Plain-English tax explainers", "Quarterly estimate help", "Recordkeeping tips"],
          "Describe your situation", "e.g. Freelance designer, home office, US, 1099 income",
          "You are TaxTactician, a tax assistant. Given a situation, suggest likely deductions/credits to explore and explain the reasoning in plain English. Always add a disclaimer to consult a licensed tax professional."),

    # ---------------- Everyday Life (for everyone, every day) ----------------
    _tool("mealmate", "MealMate", "Weekly meal plans & grocery lists", "everyday", 19,
          "Utensils", "Bestseller", 4.9, 34200,
          ["Personalized weekly menus", "Auto grocery lists", "Diet & allergy aware", "Budget-friendly options"],
          "Tell me about your week", "e.g. Healthy dinners for a family of 4, no seafood, $100 budget",
          "You are MealMate, a friendly meal-planning assistant for busy people. Given preferences, create a simple weekly dinner plan with a consolidated grocery list. Practical, tasty, and budget-aware."),
    _tool("budgetbuddy", "BudgetBuddy", "Take control of your money", "everyday", 19,
          "Wallet", "Popular", 4.8, 28700,
          ["Simple monthly budgets", "Savings goal plans", "Spending insights", "Debt payoff strategies"],
          "Describe your money goal", "e.g. Take-home $3,800/mo, want to save for a $6k trip",
          "You are BudgetBuddy, a warm personal-finance coach. Given income and goals, build a simple, realistic budget and a savings plan with clear steps. Encouraging, jargon-free. Note it's general guidance, not financial advice."),
    _tool("studybuddy", "StudyBuddy", "Study smarter, ace every exam", "everyday", 19,
          "BookOpen", "Popular", 4.8, 31500,
          ["Study guides & summaries", "Flashcards & quizzes", "Concept explanations", "Exam prep plans"],
          "What are you studying?", "e.g. Help me prep for a biology midterm on cell division",
          "You are StudyBuddy, a patient tutor for students of any age. Given a topic, create a clear study guide, a few flashcards, and a short practice quiz with answers. Make hard concepts click."),
    _tool("giftgenie", "GiftGenie", "The perfect gift, every time", "everyday", 9,
          "Gift", "Bestseller", 4.9, 41800,
          ["Personalized gift ideas", "Any budget or occasion", "Thoughtful & unique picks", "Last-minute rescues"],
          "Who are you shopping for?", "e.g. My dad's 60th, loves fishing and jazz, budget $80",
          "You are GiftGenie, a thoughtful gift concierge. Given a person, occasion, and budget, suggest 5 specific, creative gift ideas with a one-line reason each. Warm and genuinely helpful."),
    _tool("chefai", "ChefAI", "Recipes from what's in your fridge", "everyday", 19,
          "ChefHat", "Popular", 4.8, 26400,
          ["Use-what-you-have recipes", "Step-by-step instructions", "Dietary swaps", "Cook-time estimates"],
          "What's in your kitchen?", "e.g. Chicken, rice, broccoli, soy sauce, garlic",
          "You are ChefAI, a resourceful home cook. Given available ingredients, suggest 1-2 easy recipes with clear steps and cook times, using mostly what's on hand. Friendly and encouraging."),
    _tool("lingualoop", "LinguaLoop", "Learn any language, conversationally", "everyday", 29,
          "Languages", None, 4.7, 19300,
          ["Conversation practice", "Vocabulary drills", "Grammar made simple", "50+ languages"],
          "What do you want to learn?", "e.g. Practice ordering food in Spanish, beginner level",
          "You are LinguaLoop, an encouraging language tutor. Given a language and level, run a short practice exchange with translations and a couple of key phrases to remember. Supportive and fun."),
    _tool("planmyday", "PlanMyDay", "Plan your day, build better habits", "everyday", 19,
          "CalendarCheck", None, 4.7, 22800,
          ["Daily schedule builder", "Habit & routine coaching", "Priority planning", "Focus-time blocking"],
          "What's on your plate today?", "e.g. Work, gym, groceries, call mom, finish a report",
          "You are PlanMyDay, a calm productivity coach. Given a person's tasks, build a realistic time-blocked daily plan with priorities and a small habit suggestion. Motivating, not overwhelming."),
    _tool("wordsmith", "WordSmith", "Everyday writing, handled", "everyday", 19,
          "PenLine", "Popular", 4.8, 33100,
          ["Emails, letters & messages", "Tone adjustment", "Grammar & clarity fixes", "Tricky-message help"],
          "What do you need to write?", "e.g. A polite email asking my landlord to fix the heater",
          "You are WordSmith, a helpful everyday writing assistant. Given a writing need, produce a clear, well-toned draft the person can send as-is. Natural and human, never stiff."),
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

def _auto_meta(t):
    p = t["price"]
    if p >= 120:
        return ("Gold", "Deep", "Best-in-class")
    if p >= 90:
        return ("Gold", "Fast", "Best-in-class")
    if p >= 45:
        return ("Silver", "Fast", "High quality")
    return ("Bronze", "Instant", "Good enough")


for _t in CATALOG:
    if _t["slug"] in TIER_META:
        _tier, _speed, _quality, _why = TIER_META[_t["slug"]]
    else:
        _tier, _speed, _quality = _auto_meta(_t)
        _why = (f"{_t['tagline']}. A {_tier}-tier pick — choose it when you want "
                f"{_quality.lower()} results at {_speed.lower()} speed for {_t['category']} work.")
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


# ------------------ AI Studio credit packs ------------------
def _pack(slug, name, credits, price, badge=None):
    return {
        "slug": slug, "name": name, "credits": credits, "price": float(price),
        "amount_cents": int(round(price * 100)), "lookup_key": f"credits_{slug}",
        "tagline": f"{credits} AI Studio credits", "badge": badge, "is_credit_pack": True,
    }


CREDIT_PACKS = [
    _pack("spark", "Spark Pack", 120, 9),
    _pack("pro", "Pro Pack", 350, 19, "Best Value"),
    _pack("studio", "Studio Pack", 800, 29, "Power User"),
]


def get_credit_pack_by_lookup(lookup_key):
    for p in CREDIT_PACKS:
        if p["lookup_key"] == lookup_key:
            return p
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
