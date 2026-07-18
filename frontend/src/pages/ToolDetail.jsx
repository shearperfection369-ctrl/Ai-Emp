import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api, { apiErr } from "../lib/api";
import { Icon } from "../lib/icons";
import { useCart } from "../context/CartContext";
import { toast } from "sonner";
import { Star, Users, Check, Play, Terminal, ArrowLeft, ShoppingCart, Loader2 } from "lucide-react";

export default function ToolDetail() {
  const { slug } = useParams();
  const { addItem, has } = useCart();
  const [tool, setTool] = useState(null);
  const [notFound, setNotFound] = useState(false);
  const [demoInput, setDemoInput] = useState("");
  const [demoOutput, setDemoOutput] = useState("");
  const [running, setRunning] = useState(false);

  useEffect(() => {
    setTool(null); setDemoOutput(""); setDemoInput("");
    api.get(`/tools/${slug}`).then(({ data }) => setTool(data)).catch(() => setNotFound(true));
  }, [slug]);

  const runDemo = async () => {
    if (!demoInput.trim()) { toast.error("Enter a prompt to run the simulation"); return; }
    setRunning(true); setDemoOutput("");
    try {
      const { data } = await api.post(`/tools/${slug}/demo`, { input: demoInput });
      setDemoOutput(data.output);
    } catch (e) {
      toast.error(apiErr(e));
    } finally {
      setRunning(false);
    }
  };

  if (notFound) return <div className="max-w-3xl mx-auto px-5 py-24 text-center font-code text-[#8b9bb4]">Tool not found. <Link to="/marketplace" className="text-[#00f0ff]">Return to arsenal</Link></div>;
  if (!tool) return <div className="min-h-[60vh] flex items-center justify-center"><Loader2 className="w-8 h-8 text-[#00f0ff] animate-spin" /></div>;

  const owned = has(tool.slug);

  return (
    <div className="max-w-[1400px] mx-auto px-5 py-10" data-testid="tool-detail-page">
      <Link to="/marketplace" className="inline-flex items-center gap-2 font-code text-sm text-[#8b9bb4] hover:text-[#00f0ff] mb-8 transition-colors">
        <ArrowLeft className="w-4 h-4" /> BACK TO ARSENAL
      </Link>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Left: info */}
        <div className="lg:col-span-2 space-y-8">
          <div className="animate-hud-in">
            <div className="flex items-start gap-5">
              <div className="w-16 h-16 clip-hud-sm bg-[#00f0ff]/10 border border-[#00f0ff]/40 flex items-center justify-center glow-cyan shrink-0">
                <Icon name={tool.icon} className="w-8 h-8 text-[#00f0ff]" />
              </div>
              <div>
                <div className="font-code text-[11px] tracking-[0.25em] uppercase text-[#8b9bb4]">{tool.category}</div>
                <h1 className="font-display font-bold text-4xl text-white">{tool.name}</h1>
                <p className="font-code text-[#8b9bb4] mt-1">{tool.tagline}</p>
                <div className="flex items-center gap-5 mt-3 font-code text-sm">
                  <span className="flex items-center gap-1 text-[#ffb000]"><Star className="w-4 h-4 fill-[#ffb000]" /> {tool.rating}</span>
                  <span className="flex items-center gap-1 text-[#8b9bb4]"><Users className="w-4 h-4" /> {tool.users.toLocaleString()} operators</span>
                  {tool.badge && <span className="px-2 py-0.5 clip-hud-sm bg-[#ffb000]/15 text-[#ffb000] text-[10px] tracking-widest uppercase border border-[#ffb000]/40">{tool.badge}</span>}
                </div>
              </div>
            </div>
          </div>

          <div className="glass clip-hud p-6">
            <h2 className="font-display font-bold text-xl text-white mb-4">Capabilities</h2>
            <div className="grid sm:grid-cols-2 gap-3">
              {tool.features.map((f) => (
                <div key={f} className="flex items-center gap-3 font-code text-sm text-[#e6f6ff]">
                  <span className="w-5 h-5 shrink-0 clip-hud-sm bg-[#00f0ff]/15 border border-[#00f0ff]/40 flex items-center justify-center">
                    <Check className="w-3 h-3 text-[#00f0ff]" />
                  </span>
                  {f}
                </div>
              ))}
            </div>
          </div>

          {/* Live demo terminal */}
          <div className="glass clip-hud overflow-hidden" data-testid="demo-terminal">
            <div className="px-5 py-3 border-b border-[#00f0ff]/20 flex items-center gap-2 scanlines">
              <Terminal className="w-4 h-4 text-[#00f0ff]" />
              <span className="font-orbit font-bold text-sm tracking-widest text-white">LIVE SIMULATION</span>
              <span className="ml-auto font-code text-[10px] text-[#00f0ff] flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00f0ff] animate-blink" /> ENGINE READY
              </span>
            </div>
            <div className="p-5 space-y-4">
              <label className="font-code text-xs tracking-widest text-[#8b9bb4] uppercase">{tool.demo_label}</label>
              <textarea
                value={demoInput}
                onChange={(e) => setDemoInput(e.target.value)}
                placeholder={tool.demo_placeholder}
                rows={3}
                data-testid="demo-input"
                className="w-full bg-[#050a10] border border-[#00f0ff]/25 clip-hud-sm p-3 font-code text-sm text-[#e6f6ff] outline-none focus:border-[#00f0ff] placeholder:text-[#8b9bb4]/50 resize-none"
              />
              <button onClick={runDemo} disabled={running} data-testid="run-demo"
                className="inline-flex items-center gap-2 px-6 py-3 clip-hud-sm bg-[#00f0ff] text-black font-display font-bold tracking-wide hover:glow-cyan-strong transition-shadow disabled:opacity-60">
                {running ? <><Loader2 className="w-4 h-4 animate-spin" /> PROCESSING…</> : <><Play className="w-4 h-4" /> RUN SIMULATION</>}
              </button>

              {(demoOutput || running) && (
                <div className="mt-2 bg-[#050a10] border border-[#00f0ff]/20 clip-hud-sm p-4 font-code text-sm text-[#e6f6ff] whitespace-pre-wrap leading-relaxed min-h-[80px]" data-testid="demo-output">
                  <div className="text-[#00f0ff] text-xs mb-2 tracking-widest">◈ {tool.name.toUpperCase()} OUTPUT</div>
                  {demoOutput || <span className="animate-blink">Generating response…</span>}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right: purchase */}
        <div className="lg:col-span-1">
          <div className="glass clip-hud p-6 lg:sticky lg:top-24 space-y-5">
            <div>
              <div className="font-code text-xs text-[#8b9bb4] tracking-widest uppercase">One-time deployment</div>
              <div className="font-display font-bold text-5xl text-white mt-1">${tool.price.toFixed(0)}</div>
              <div className="font-code text-xs text-[#8b9bb4] mt-1">Lifetime access · instant unlock</div>
            </div>
            <button
              data-testid="detail-add-cart"
              disabled={owned}
              onClick={() => { addItem(tool); toast.success(`${tool.name} added to arsenal`); }}
              className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 clip-hud bg-[#00f0ff] text-black font-display font-bold tracking-wide hover:glow-cyan-strong transition-shadow disabled:opacity-60">
              <ShoppingCart className="w-4 h-4" /> {owned ? "IN YOUR CART" : "ADD TO CART"}
            </button>
            <Link to="/cart" data-testid="detail-checkout"
              className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 clip-hud glass border border-[#00f0ff]/40 text-white font-display font-bold tracking-wide hover:border-[#00f0ff] transition-colors">
              GO TO CHECKOUT
            </Link>
            <div className="pt-4 border-t border-[#00f0ff]/10 space-y-2 font-code text-xs text-[#8b9bb4]">
              <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[#00f0ff]" /> Secure Stripe payment</div>
              <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[#00f0ff]" /> Instant library access</div>
              <div className="flex items-center gap-2"><Check className="w-3.5 h-3.5 text-[#00f0ff]" /> Try live before you buy</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
