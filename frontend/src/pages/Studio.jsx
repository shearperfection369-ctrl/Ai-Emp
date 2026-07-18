import { useEffect, useState } from "react";
import api, { apiErr } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { toast } from "sonner";
import {
  Image as ImageIcon, PenLine, Search, Sparkles, Loader2, Download, Zap, Coins, Bot, Brain,
} from "lucide-react";

const TABS = [
  { id: "image", label: "Image Studio", icon: ImageIcon, costKey: "image", accent: "#00f0ff" },
  { id: "text", label: "Writer & Coder", icon: PenLine, costKey: "text", accent: "#00f0ff" },
  { id: "research", label: "Research", icon: Search, costKey: "research", accent: "#ffb000" },
];

export default function Studio() {
  const { refreshUser } = useAuth();
  const [tab, setTab] = useState("image");
  const [credits, setCredits] = useState(null);
  const [costs, setCosts] = useState({ text: 2, research: 4, image: 15 });
  const [packs, setPacks] = useState([]);

  // shared io
  const [input, setInput] = useState("");
  const [mode, setMode] = useState("chatgpt");
  const [busy, setBusy] = useState(false);
  const [textOut, setTextOut] = useState("");
  const [imgOut, setImgOut] = useState("");
  const [engine, setEngine] = useState("");

  const loadCredits = () => api.get("/studio/credits").then(({ data }) => { setCredits(data.credits); setCosts(data.costs); });

  useEffect(() => {
    loadCredits();
    api.get("/credit-packs").then(({ data }) => setPacks(data));
  }, []);

  const switchTab = (id) => { setTab(id); setInput(""); setTextOut(""); setImgOut(""); setEngine(""); };

  const run = async () => {
    if (!input.trim()) { toast.error("Enter something first"); return; }
    setBusy(true); setTextOut(""); setImgOut("");
    try {
      if (tab === "image") {
        const { data } = await api.post("/studio/image", { prompt: input });
        setImgOut(data.image_base64); setCredits(data.credits);
      } else if (tab === "text") {
        const { data } = await api.post("/studio/text", { mode, prompt: input });
        setTextOut(data.output); setEngine(data.engine); setCredits(data.credits);
      } else {
        const { data } = await api.post("/studio/research", { query: input });
        setTextOut(data.output); setCredits(data.credits);
      }
      refreshUser();
    } catch (e) {
      const status = e?.response?.status;
      toast.error(apiErr(e));
      if (status === 402) document.getElementById("credit-packs")?.scrollIntoView({ behavior: "smooth" });
    } finally {
      setBusy(false);
    }
  };

  const buyPack = async (pack) => {
    try {
      const { data } = await api.post("/payments/checkout", {
        items: [{ lookup_key: pack.lookup_key, quantity: 1 }],
        origin_url: window.location.origin,
      });
      window.location.href = data.checkout_url;
    } catch (e) {
      toast.error(apiErr(e));
    }
  };

  const activeCost = costs[TABS.find((t) => t.id === tab).costKey];

  return (
    <div className="max-w-[1200px] mx-auto px-5 py-12" data-testid="studio-page">
      <div className="flex flex-wrap items-end justify-between gap-4 mb-8">
        <div>
          <div className="font-code text-[11px] tracking-[0.3em] text-[#00f0ff] uppercase mb-1">// LIVE AI CONSOLE</div>
          <h1 className="font-display font-bold text-3xl md:text-5xl text-white flex items-center gap-3">
            <Sparkles className="w-8 h-8 text-[#00f0ff]" /> AI Studio
          </h1>
          <p className="font-code text-[#8b9bb4] mt-2">Real, working AI — generate images, writing, code & research. Powered by frontier models.</p>
        </div>
        <div className="glass clip-hud-sm px-5 py-3 flex items-center gap-3" data-testid="studio-credits">
          <Coins className="w-5 h-5 text-[#ffb000]" />
          <div>
            <div className="font-code text-[10px] tracking-widest uppercase text-[#8b9bb4]">Credits</div>
            <div className="font-orbit font-bold text-2xl text-[#ffb000]">{credits ?? "—"}</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {TABS.map((t) => (
          <button key={t.id} onClick={() => switchTab(t.id)} data-testid={`studio-tab-${t.id}`}
            className={`px-4 py-2.5 clip-hud-sm font-display font-bold text-sm tracking-wide transition-colors border flex items-center gap-2 ${
              tab === t.id ? "bg-[#00f0ff] text-black border-[#00f0ff]" : "glass border-[#00f0ff]/20 text-[#8b9bb4] hover:text-white"}`}>
            <t.icon className="w-4 h-4" /> {t.label}
            <span className={`font-code text-[10px] ${tab === t.id ? "text-black/70" : "text-[#00f0ff]"}`}>{costs[t.costKey]}cr</span>
          </button>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Input */}
        <div className="glass clip-hud p-6">
          {tab === "text" && (
            <div className="flex gap-2 mb-4">
              {[{ id: "chatgpt", label: "ChatGPT", icon: Bot }, { id: "claude", label: "Claude", icon: Brain }].map((m) => (
                <button key={m.id} onClick={() => setMode(m.id)} data-testid={`engine-${m.id}`}
                  className={`px-3 py-1.5 clip-hud-sm font-code text-xs tracking-wide border flex items-center gap-1.5 transition-colors ${
                    mode === m.id ? "bg-[#00f0ff]/15 border-[#00f0ff]/50 text-[#00f0ff]" : "border-[#00f0ff]/15 text-[#8b9bb4] hover:text-white"}`}>
                  <m.icon className="w-3.5 h-3.5" /> {m.label}
                </button>
              ))}
            </div>
          )}
          <label className="font-code text-xs tracking-widest text-[#8b9bb4] uppercase">
            {tab === "image" ? "Describe your image" : tab === "research" ? "What do you want to research?" : "Your prompt"}
          </label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={tab === "image" ? 4 : 8}
            data-testid="studio-input"
            placeholder={tab === "image"
              ? "e.g. A neon cyberpunk fox mascot, futuristic HUD style, dark background"
              : tab === "research"
                ? "e.g. Compare electric vs hydrogen for long-haul freight"
                : "e.g. Write a punchy launch tweet for an AI logistics startup"}
            className="w-full mt-2 bg-[#050a10] border border-[#00f0ff]/25 clip-hud-sm p-3 font-code text-sm text-[#e6f6ff] outline-none focus:border-[#00f0ff] placeholder:text-[#8b9bb4]/50 resize-none"
          />
          <button onClick={run} disabled={busy} data-testid="studio-run"
            className="mt-4 w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 clip-hud bg-[#00f0ff] text-black font-display font-bold tracking-wide hover:glow-cyan-strong transition-shadow disabled:opacity-60">
            {busy ? <><Loader2 className="w-4 h-4 animate-spin" /> {tab === "image" ? "RENDERING… (~30s)" : "GENERATING…"}</>
              : <><Zap className="w-4 h-4" /> GENERATE · {activeCost} CREDITS</>}
          </button>
          <p className="font-code text-[11px] text-[#8b9bb4] mt-2 text-center">Each generation deducts {activeCost} credits from your balance.</p>
        </div>

        {/* Output */}
        <div className="glass clip-hud p-6 min-h-[320px]" data-testid="studio-output">
          <div className="font-code text-[11px] tracking-widest uppercase text-[#00f0ff] mb-3 flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-[#00f0ff] animate-blink" /> OUTPUT {engine && `· ${engine}`}
          </div>
          {busy && (
            <div className="flex flex-col items-center justify-center h-56 gap-3">
              <Loader2 className="w-8 h-8 text-[#00f0ff] animate-spin" />
              <span className="font-code text-sm text-[#8b9bb4]">{tab === "image" ? "Painting pixels…" : "Thinking…"}</span>
            </div>
          )}
          {!busy && imgOut && (
            <div className="space-y-3">
              <img src={`data:image/png;base64,${imgOut}`} alt="Generated" className="w-full clip-hud-sm border border-[#00f0ff]/30" data-testid="studio-image-output" />
              <a href={`data:image/png;base64,${imgOut}`} download="ai-tool-emporium.png"
                className="inline-flex items-center gap-2 px-4 py-2 clip-hud-sm glass border border-[#00f0ff]/40 text-white font-display font-bold text-sm hover:border-[#00f0ff]">
                <Download className="w-4 h-4" /> DOWNLOAD
              </a>
            </div>
          )}
          {!busy && textOut && (
            <div className="font-code text-sm text-[#e6f6ff] whitespace-pre-wrap leading-relaxed" data-testid="studio-text-output">{textOut}</div>
          )}
          {!busy && !imgOut && !textOut && (
            <div className="flex items-center justify-center h-56 font-code text-sm text-[#8b9bb4]/70 text-center px-6">
              Your generated output will materialize here.
            </div>
          )}
        </div>
      </div>

      {/* Credit packs */}
      <div id="credit-packs" className="mt-14" data-testid="credit-packs">
        <div className="flex items-center gap-2 mb-2">
          <Coins className="w-5 h-5 text-[#ffb000]" />
          <h2 className="font-display font-bold text-2xl text-white">Top Up Credits</h2>
        </div>
        <p className="font-code text-sm text-[#8b9bb4] mb-6">Fuel your Studio. Credits never expire. Bigger packs = better value.</p>
        <div className="grid sm:grid-cols-3 gap-5">
          {packs.map((p, i) => (
            <div key={p.slug} className="glass clip-hud p-6 flex flex-col hover:border-[#ffb000]/50 transition-colors animate-hud-in" style={{ animationDelay: `${i * 70}ms` }} data-testid={`pack-${p.slug}`}>
              {p.badge && <span className="self-start font-code text-[10px] font-bold tracking-widest uppercase px-2 py-1 clip-hud-sm bg-[#ffb000]/15 text-[#ffb000] border border-[#ffb000]/40 mb-3">{p.badge}</span>}
              <div className="font-display font-bold text-xl text-white">{p.name}</div>
              <div className="font-orbit font-bold text-4xl text-[#ffb000] text-glow-amber mt-2">{p.credits}<span className="font-code text-sm text-[#8b9bb4] font-normal"> credits</span></div>
              <div className="font-code text-xs text-[#8b9bb4] mt-1">≈ {Math.floor(p.credits / costs.image)} images · {Math.floor(p.credits / costs.text)} writings</div>
              <div className="flex items-center justify-between mt-5 pt-4 border-t border-[#ffb000]/15">
                <div className="font-display font-bold text-2xl text-white">${p.price.toFixed(0)}</div>
                <button onClick={() => buyPack(p)} data-testid={`buy-${p.slug}`}
                  className="px-5 py-2.5 clip-hud-sm bg-[#ffb000]/10 border border-[#ffb000]/40 text-[#ffb000] font-display font-bold text-sm hover:bg-[#ffb000] hover:text-black transition-colors">
                  BUY
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
