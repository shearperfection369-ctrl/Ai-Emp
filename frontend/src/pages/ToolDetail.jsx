import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api, { apiErr } from "../lib/api";
import { Icon } from "../lib/icons";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import TierBadge from "../components/TierBadge";
import { toast } from "sonner";
import { Star, Users, Check, Play, Terminal, ArrowLeft, ShoppingCart, Loader2, Zap, Award, MessageSquare } from "lucide-react";

export default function ToolDetail() {
  const { slug } = useParams();
  const { addItem, has } = useCart();
  const { user } = useAuth();
  const [tool, setTool] = useState(null);
  const [notFound, setNotFound] = useState(false);
  const [demoInput, setDemoInput] = useState("");
  const [demoOutput, setDemoOutput] = useState("");
  const [running, setRunning] = useState(false);
  const [reviews, setReviews] = useState({ reviews: [], average: 0, count: 0 });
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");
  const [posting, setPosting] = useState(false);

  const loadReviews = () => api.get(`/tools/${slug}/reviews`).then(({ data }) => setReviews(data)).catch(() => {});

  useEffect(() => {
    setTool(null); setDemoOutput(""); setDemoInput("");
    api.get(`/tools/${slug}`).then(({ data }) => setTool(data)).catch(() => setNotFound(true));
    loadReviews();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  const submitReview = async () => {
    setPosting(true);
    try {
      await api.post(`/tools/${slug}/reviews`, { rating, comment });
      setComment("");
      toast.success("Review posted — thanks, operator!");
      loadReviews();
    } catch (e) {
      toast.error(apiErr(e));
    } finally {
      setPosting(false);
    }
  };

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
                  <span className="flex items-center gap-1 text-[#ffb000]"><Star className="w-4 h-4 fill-[#ffb000]" /> {reviews.count > 0 ? reviews.average : tool.rating}</span>
                  <span className="flex items-center gap-1 text-[#8b9bb4]"><Users className="w-4 h-4" /> {tool.users.toLocaleString()} operators</span>
                  {tool.tier && <TierBadge tier={tool.tier} />}
                  {tool.badge && <span className="px-2 py-0.5 clip-hud-sm bg-[#ffb000]/15 text-[#ffb000] text-[10px] tracking-widest uppercase border border-[#ffb000]/40">{tool.badge}</span>}
                </div>
              </div>
            </div>
          </div>

          <div className="glass clip-hud p-6" data-testid="why-panel">
            <h2 className="font-display font-bold text-xl text-white mb-4 flex items-center gap-2"><Award className="w-5 h-5 text-[#ffb000]" /> Why pick this one?</h2>
            <div className="grid grid-cols-3 gap-3 mb-4">
              <div className="glass clip-hud-sm p-3 text-center">
                <div className="font-code text-[10px] text-[#8b9bb4] uppercase tracking-widest">Tier</div>
                <div className="mt-2 flex justify-center"><TierBadge tier={tool.tier} /></div>
              </div>
              <div className="glass clip-hud-sm p-3 text-center">
                <div className="font-code text-[10px] text-[#8b9bb4] uppercase tracking-widest">Speed</div>
                <div className="font-display font-bold text-[#00f0ff] mt-1.5 flex items-center justify-center gap-1"><Zap className="w-4 h-4" />{tool.speed}</div>
              </div>
              <div className="glass clip-hud-sm p-3 text-center">
                <div className="font-code text-[10px] text-[#8b9bb4] uppercase tracking-widest">Quality</div>
                <div className="font-display font-bold text-white mt-1.5 text-sm">{tool.quality_tier}</div>
              </div>
            </div>
            <p className="font-code text-sm text-[#e6f6ff] leading-relaxed">{tool.why}</p>
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
          {/* Reviews */}
          <div className="glass clip-hud p-6" data-testid="reviews-section">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-display font-bold text-xl text-white flex items-center gap-2"><MessageSquare className="w-5 h-5 text-[#00f0ff]" /> Operator Reviews</h2>
              {reviews.count > 0 && (
                <div className="flex items-center gap-1.5 font-display font-bold text-lg text-[#ffb000]">
                  <Star className="w-4 h-4 fill-[#ffb000]" /> {reviews.average}
                  <span className="font-code text-xs text-[#8b9bb4] font-normal">({reviews.count})</span>
                </div>
              )}
            </div>

            {user ? (
              <div className="mb-6 pb-6 border-b border-[#00f0ff]/10">
                <div className="flex items-center gap-1.5 mb-2">
                  {[1, 2, 3, 4, 5].map((n) => (
                    <button key={n} onClick={() => setRating(n)} data-testid={`star-${n}`} className="transition-transform hover:scale-110">
                      <Star className={`w-6 h-6 ${n <= rating ? "fill-[#ffb000] text-[#ffb000]" : "text-[#8b9bb4]/50"}`} />
                    </button>
                  ))}
                </div>
                <textarea value={comment} onChange={(e) => setComment(e.target.value)} rows={2} placeholder="Share your experience with this tool…" data-testid="review-comment"
                  className="w-full bg-[#050a10] border border-[#00f0ff]/25 clip-hud-sm p-3 font-code text-sm text-[#e6f6ff] outline-none focus:border-[#00f0ff] placeholder:text-[#8b9bb4]/50 resize-none" />
                <button onClick={submitReview} disabled={posting} data-testid="submit-review"
                  className="mt-3 inline-flex items-center gap-2 px-5 py-2.5 clip-hud-sm bg-[#00f0ff] text-black font-display font-bold text-sm tracking-wide hover:glow-cyan-strong transition-shadow disabled:opacity-60">
                  {posting ? <Loader2 className="w-4 h-4 animate-spin" /> : <MessageSquare className="w-4 h-4" />} POST REVIEW
                </button>
              </div>
            ) : (
              <div className="mb-6 pb-6 border-b border-[#00f0ff]/10 font-code text-sm text-[#8b9bb4]">
                <Link to="/login" className="text-[#00f0ff]">Sign in</Link> to leave a review.
              </div>
            )}

            {reviews.reviews.length === 0 ? (
              <p className="font-code text-sm text-[#8b9bb4]">No reviews yet. Be the first operator to report in.</p>
            ) : (
              <div className="space-y-4">
                {reviews.reviews.map((r, i) => (
                  <div key={i} className="border-b border-[#00f0ff]/8 pb-4 last:border-0 last:pb-0" data-testid="review-item">
                    <div className="flex items-center gap-2.5">
                      <div className="w-8 h-8 clip-hud-sm bg-[#00f0ff]/15 border border-[#00f0ff]/40 flex items-center justify-center font-display font-bold text-[#00f0ff] text-sm shrink-0">
                        {(r.user_name || "U")[0].toUpperCase()}
                      </div>
                      <div>
                        <div className="font-display font-semibold text-white text-sm flex items-center gap-2">
                          {r.user_name}
                          {r.verified && <span className="font-code text-[9px] tracking-widest uppercase px-1.5 py-0.5 clip-hud-sm bg-[#00f0ff]/15 text-[#00f0ff] border border-[#00f0ff]/40">Verified</span>}
                        </div>
                        <div className="flex items-center gap-0.5 mt-0.5">
                          {[1, 2, 3, 4, 5].map((n) => <Star key={n} className={`w-3 h-3 ${n <= r.rating ? "fill-[#ffb000] text-[#ffb000]" : "text-[#8b9bb4]/40"}`} />)}
                        </div>
                      </div>
                    </div>
                    {r.comment && <p className="font-code text-sm text-[#e6f6ff] mt-2 leading-relaxed">{r.comment}</p>}
                  </div>
                ))}
              </div>
            )}
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
