import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../lib/api";
import { Icon } from "../lib/icons";
import ToolCard from "../components/ToolCard";
import { ArrowRight, Cpu, ShieldCheck, Zap, Rocket, Bot, Coffee, Clock, PiggyBank, Smile } from "lucide-react";

const HERO_BG = "https://images.unsplash.com/photo-1768329051020-489b1bc3f507?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHw0fHxzY2klMjBmaSUyMGRlZXAlMjBzcGFjZSUyMHN0YXJzJTIwaW50ZXJzdGVsbGFyfGVufDB8fHx8MTc4NDM5OTA3N3ww&ixlib=rb-4.1.0&q=85";

const STATS = [
  { label: "AI TOOLS DEPLOYED", value: "65+" },
  { label: "INDUSTRIES COVERED", value: "30+" },
  { label: "OPERATORS ARMED", value: "220K+" },
  { label: "UPTIME", value: "99.9%" },
];

const FEATURES = [
  { icon: "Zap", title: "Instant Deployment", desc: "Every tool is packaged and battle-ready. Buy it, own it, run it — zero setup." },
  { icon: "Cpu", title: "Live AI Simulations", desc: "Don't guess. Run any tool live before you buy and watch real output generate." },
  { icon: "Bot", title: "ARIA Concierge", desc: "A JARVIS-grade AI that understands your goal and recommends the perfect tool." },
  { icon: "ShieldCheck", title: "Secure Checkout", desc: "Encrypted Stripe payments. Your arsenal is protected, always." },
];

export default function Home() {
  const [featured, setFeatured] = useState([]);
  const [categories, setCategories] = useState([]);
  const [everyday, setEveryday] = useState([]);

  useEffect(() => {
    api.get("/tools", { params: { sort: "rating" } }).then(({ data }) => setFeatured(data.slice(0, 6)));
    api.get("/categories").then(({ data }) => setCategories(data));
    api.get("/tools", { params: { category: "everyday", sort: "popular" } }).then(({ data }) => setEveryday(data.slice(0, 8)));
  }, []);

  return (
    <div data-testid="home-page">
      {/* HERO */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img src={HERO_BG} alt="" className="w-full h-full object-cover opacity-40" />
          <div className="absolute inset-0 bg-gradient-to-b from-[#030508]/60 via-[#030508]/85 to-[#030508]" />
          <div className="absolute inset-0 scanlines" />
        </div>
        <div className="relative z-10 max-w-[1400px] mx-auto px-5 pt-20 pb-24 md:pt-28 md:pb-32">
          <div className="max-w-3xl animate-hud-in">
            <img src="/logo-full.png" alt="AI Tool Emporium" className="h-24 md:h-32 object-contain mb-6 drop-shadow-[0_0_28px_rgba(0,240,255,0.4)]" data-testid="hero-logo" />
            <div className="inline-flex items-center gap-2 px-3 py-1.5 clip-hud-sm glass border border-[#00f0ff]/30 mb-6">
              <span className="w-2 h-2 rounded-full bg-[#00f0ff] animate-blink" />
              <span className="font-code text-[11px] tracking-[0.3em] text-[#00f0ff] uppercase">System Online · 2026 Build</span>
            </div>
            <h1 className="font-display font-bold text-4xl sm:text-5xl lg:text-6xl leading-[1.05] text-white">
              THE ONE-STOP <span className="text-[#00f0ff] text-glow">ARSENAL</span><br />
              FOR ALL THINGS <span className="text-[#ffb000] text-glow-amber">AI</span>
            </h1>
            <p className="font-code text-base md:text-lg text-[#8b9bb4] mt-6 max-w-xl leading-relaxed">
              Like the hardware store for physical tools — but for artificial intelligence. 65+ packaged AI tools for every industry <span className="text-white">and every day</span>, ready to deploy the moment you land.
            </p>
            <div className="flex flex-wrap gap-4 mt-9">
              <Link to="/marketplace" data-testid="hero-browse"
                className="group inline-flex items-center gap-2 px-7 py-3.5 clip-hud bg-[#00f0ff] text-black font-display font-bold tracking-wide hover:glow-cyan-strong transition-shadow">
                ENTER THE EMPORIUM
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link to="/branding" data-testid="hero-branding"
                className="inline-flex items-center gap-2 px-7 py-3.5 clip-hud glass border border-[#00f0ff]/40 text-white font-display font-bold tracking-wide hover:border-[#00f0ff] transition-colors">
                <Rocket className="w-4 h-4 text-[#00f0ff]" /> BRAND KIT
              </Link>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-14">
              {STATS.map((s) => (
                <div key={s.label} className="glass clip-hud-sm p-4">
                  <div className="font-orbit font-bold text-2xl md:text-3xl text-[#00f0ff] text-glow">{s.value}</div>
                  <div className="font-code text-[10px] tracking-widest text-[#8b9bb4] mt-1">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="relative z-10 max-w-[1400px] mx-auto px-5 py-16">
        <div className="grid md:grid-cols-4 gap-5">
          {FEATURES.map((f, i) => (
            <div key={f.title} className="glass clip-hud p-6 animate-hud-in hover:border-[#00f0ff]/50 transition-colors" style={{ animationDelay: `${i * 80}ms` }} data-testid={`feature-${i}`}>
              <div className="w-11 h-11 clip-hud-sm bg-[#00f0ff]/10 border border-[#00f0ff]/30 flex items-center justify-center mb-4">
                <Icon name={f.icon} className="w-5 h-5 text-[#00f0ff]" />
              </div>
              <h3 className="font-display font-bold text-lg text-white">{f.title}</h3>
              <p className="font-code text-sm text-[#8b9bb4] mt-2 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* EVERYDAY AI */}
      <section className="relative z-10 max-w-[1400px] mx-auto px-5 py-16">
        <div className="glass clip-hud p-8 md:p-10 scanlines relative overflow-hidden">
          <div className="absolute -top-1/2 -right-20 w-96 h-96 rounded-full bg-[#00f0ff]/10 blur-3xl pointer-events-none" />
          <div className="relative">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 clip-hud-sm bg-[#ffb000]/10 border border-[#ffb000]/40 mb-5">
              <Coffee className="w-4 h-4 text-[#ffb000]" />
              <span className="font-code text-[11px] tracking-[0.3em] text-[#ffb000] uppercase">For Everyone · Every Day</span>
            </div>
            <h2 className="font-display font-bold text-3xl md:text-4xl text-white max-w-2xl leading-tight">
              AI Isn't Just for Enterprises. <span className="text-[#00f0ff] text-glow">It's for You.</span>
            </h2>
            <p className="font-code text-[#8b9bb4] mt-4 max-w-2xl leading-relaxed">
              Real tools everyday people use to save time, spend smarter, eat better, learn faster and get more done — starting at just <span className="text-white font-bold">$9</span>. Enrich your daily life, one task at a time.
            </p>
            <div className="flex flex-wrap gap-4 mt-6">
              {[{ icon: Clock, t: "Save hours weekly" }, { icon: PiggyBank, t: "Spend smarter" }, { icon: Smile, t: "Less stress, more done" }].map((b, i) => (
                <div key={i} className="flex items-center gap-2 font-code text-sm text-[#e6f6ff]">
                  <b.icon className="w-4 h-4 text-[#00f0ff]" /> {b.t}
                </div>
              ))}
            </div>

            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
              {everyday.map((t, i) => (
                <Link key={t.slug} to={`/tool/${t.slug}`} data-testid={`everyday-${t.slug}`}
                  className="glass clip-hud-sm p-4 hover:border-[#00f0ff]/50 hover:-translate-y-1 transition-all group animate-hud-in" style={{ animationDelay: `${i * 50}ms` }}>
                  <div className="flex items-center justify-between mb-2">
                    <div className="w-10 h-10 clip-hud-sm bg-[#00f0ff]/10 border border-[#00f0ff]/30 flex items-center justify-center">
                      <Icon name={t.icon} className="w-5 h-5 text-[#00f0ff]" />
                    </div>
                    <span className="font-display font-bold text-lg text-white">${t.price.toFixed(0)}</span>
                  </div>
                  <div className="font-display font-bold text-white group-hover:text-[#00f0ff] transition-colors">{t.name}</div>
                  <div className="font-code text-xs text-[#8b9bb4] mt-1 line-clamp-2">{t.tagline}</div>
                </Link>
              ))}
            </div>

            <Link to="/marketplace?category=everyday" data-testid="everyday-view-all"
              className="inline-flex items-center gap-2 mt-8 px-6 py-3 clip-hud bg-[#00f0ff] text-black font-display font-bold tracking-wide hover:glow-cyan-strong transition-shadow">
              EXPLORE EVERYDAY AI <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* CATEGORIES */}
      <section className="relative z-10 max-w-[1400px] mx-auto px-5 py-8">
        <div className="flex items-end justify-between mb-6">
          <div>
            <div className="font-code text-[11px] tracking-[0.3em] text-[#00f0ff] uppercase mb-1">// SECTORS</div>
            <h2 className="font-display font-bold text-2xl md:text-3xl text-white">Deployed Across Every Industry</h2>
          </div>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {categories.map((c) => (
            <Link key={c.id} to={`/marketplace?category=${c.id}`} data-testid={`category-${c.id}`}
              className="glass clip-hud-sm p-4 flex flex-col items-center text-center gap-2 hover:border-[#00f0ff]/50 hover:-translate-y-0.5 transition-all">
              <Icon name={c.icon} className="w-6 h-6 text-[#00f0ff]" />
              <span className="font-display font-semibold text-sm text-white">{c.name}</span>
              <span className="font-code text-[10px] text-[#8b9bb4]">{c.count} tools</span>
            </Link>
          ))}
        </div>
      </section>

      {/* FEATURED */}
      <section className="relative z-10 max-w-[1400px] mx-auto px-5 py-16">
        <div className="flex items-end justify-between mb-8">
          <div>
            <div className="font-code text-[11px] tracking-[0.3em] text-[#ffb000] uppercase mb-1">// TOP RATED</div>
            <h2 className="font-display font-bold text-2xl md:text-3xl text-white">Featured Firepower</h2>
          </div>
          <Link to="/marketplace" className="hidden sm:flex items-center gap-1.5 font-display font-semibold text-[#00f0ff] hover:gap-3 transition-all" data-testid="view-all">
            VIEW ALL <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {featured.map((t, i) => <ToolCard key={t.slug} tool={t} index={i} />)}
        </div>
      </section>
    </div>
  );
}
