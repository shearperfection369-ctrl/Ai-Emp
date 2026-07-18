import { Link } from "react-router-dom";
import { Zap, Copy, Check } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

const PALETTE = [
  { name: "Void Black", hex: "#030508" },
  { name: "Panel", hex: "#0A1118" },
  { name: "Signal Cyan", hex: "#00F0FF" },
  { name: "Alert Amber", hex: "#FFB000" },
  { name: "Threat Red", hex: "#FF2A2A" },
  { name: "Ghost Grey", hex: "#8B9BB4" },
];

const TAGLINES = [
  "The one-stop arsenal for all things AI.",
  "Gear up. Deploy AI. Dominate every industry.",
  "Where operators come to weaponize intelligence.",
  "Battle-ready AI tools. Packaged. Deployed. Yours.",
];

const VOICE = [
  { t: "Confident", d: "We speak like a mission commander — direct, assured, never hesitant." },
  { t: "Futuristic", d: "Interstellar, HUD-driven, JARVIS-grade. Always one step ahead of now." },
  { t: "Empowering", d: "The buyer is the hero. Our tools are their arsenal, not the star." },
  { t: "Precise", d: "No fluff. Every word does a job, like a well-engineered tool." },
];

export default function Branding() {
  const [copied, setCopied] = useState("");
  const copy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(text);
    toast.success("Copied to clipboard");
    setTimeout(() => setCopied(""), 1500);
  };

  return (
    <div className="max-w-[1400px] mx-auto px-5 py-12" data-testid="branding-page">
      <div className="font-code text-[11px] tracking-[0.3em] text-[#00f0ff] uppercase mb-1">// BRAND OPS</div>
      <h1 className="font-display font-bold text-3xl md:text-5xl text-white mb-3">The Emporium Brand Kit</h1>
      <p className="font-code text-[#8b9bb4] max-w-2xl mb-12">
        A full marketing &amp; branding package for AI Tool Emporium — logo system, color arsenal, voice, and ready-to-fire taglines.
      </p>

      {/* Logo */}
      <section className="mb-12">
        <h2 className="font-display font-bold text-xl text-white mb-4">Logo System</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="md:col-span-2 glass clip-hud p-8 flex items-center justify-center glow-cyan">
            <img src="/logo-full.png" alt="AI Tool Emporium official logo" className="max-h-44 object-contain" />
          </div>
          <div className="glass clip-hud p-8 flex items-center justify-center bg-[#00f0ff]/5">
            <img src="/logo-mark.png" alt="AI Tool Emporium mark" className="max-h-36 object-contain drop-shadow-[0_0_18px_rgba(0,240,255,0.5)]" />
          </div>
        </div>
      </section>

      {/* Palette */}
      <section className="mb-12">
        <h2 className="font-display font-bold text-xl text-white mb-4">Color Arsenal</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {PALETTE.map((c) => (
            <button key={c.hex} onClick={() => copy(c.hex)} data-testid={`palette-${c.hex}`}
              className="glass clip-hud-sm p-3 text-left hover:border-[#00f0ff]/50 transition-colors group">
              <div className="h-16 clip-hud-sm mb-3 border border-white/10" style={{ background: c.hex }} />
              <div className="font-display font-semibold text-sm text-white">{c.name}</div>
              <div className="font-code text-xs text-[#8b9bb4] flex items-center gap-1.5">
                {c.hex} {copied === c.hex ? <Check className="w-3 h-3 text-[#00f0ff]" /> : <Copy className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />}
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* Typography */}
      <section className="mb-12 grid md:grid-cols-2 gap-4">
        <div className="glass clip-hud p-6">
          <div className="font-code text-xs text-[#8b9bb4] tracking-widest uppercase mb-2">Display · Rajdhani / Orbitron</div>
          <div className="font-orbit font-bold text-3xl text-white">DEPLOY THE FUTURE</div>
          <div className="font-display text-lg text-[#8b9bb4] mt-2">Headlines, HUD data, mission labels</div>
        </div>
        <div className="glass clip-hud p-6">
          <div className="font-code text-xs text-[#8b9bb4] tracking-widest uppercase mb-2">Body · JetBrains Mono</div>
          <div className="font-code text-white text-lg">01001 // intelligence, weaponized.</div>
          <div className="font-code text-sm text-[#8b9bb4] mt-2">Copy, metrics, terminal output</div>
        </div>
      </section>

      {/* Voice */}
      <section className="mb-12">
        <h2 className="font-display font-bold text-xl text-white mb-4">Brand Voice</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {VOICE.map((v) => (
            <div key={v.t} className="glass clip-hud p-5">
              <div className="font-display font-bold text-lg text-[#00f0ff]">{v.t}</div>
              <p className="font-code text-sm text-[#8b9bb4] mt-1.5 leading-relaxed">{v.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Taglines */}
      <section className="mb-12">
        <h2 className="font-display font-bold text-xl text-white mb-4">Ready-to-Fire Taglines</h2>
        <div className="space-y-3">
          {TAGLINES.map((t) => (
            <button key={t} onClick={() => copy(t)} data-testid="tagline-item"
              className="w-full glass clip-hud-sm p-4 flex items-center justify-between text-left hover:border-[#00f0ff]/50 transition-colors group">
              <span className="font-display font-medium text-white text-lg">"{t}"</span>
              {copied === t ? <Check className="w-4 h-4 text-[#00f0ff]" /> : <Copy className="w-4 h-4 text-[#8b9bb4] opacity-0 group-hover:opacity-100 transition-opacity" />}
            </button>
          ))}
        </div>
      </section>

      <div className="glass clip-hud p-8 text-center scanlines">
        <h2 className="font-display font-bold text-2xl text-white">Ready to arm your workflow?</h2>
        <p className="font-code text-[#8b9bb4] mt-2">Enter the marketplace and deploy your first AI tool in seconds.</p>
        <Link to="/marketplace" className="inline-flex items-center gap-2 px-7 py-3.5 clip-hud bg-[#00f0ff] text-black font-display font-bold tracking-wide mt-6 hover:glow-cyan-strong transition-shadow">
          ENTER THE EMPORIUM
        </Link>
      </div>
    </div>
  );
}
