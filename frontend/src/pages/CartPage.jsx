import { useState } from "react";
import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";
import api, { apiErr } from "../lib/api";
import { Icon } from "../lib/icons";
import { toast } from "sonner";
import { Trash2, ShoppingCart, Loader2, ArrowRight, ShieldCheck } from "lucide-react";

export default function CartPage() {
  const { items, removeItem, total } = useCart();
  const [loading, setLoading] = useState(false);

  const checkout = async () => {
    if (items.length === 0) return;
    setLoading(true);
    try {
      const { data } = await api.post("/payments/checkout", {
        items: items.map((i) => ({ lookup_key: i.lookup_key, quantity: i.quantity })),
        origin_url: window.location.origin,
      });
      window.location.href = data.checkout_url;
    } catch (e) {
      toast.error(apiErr(e));
      setLoading(false);
    }
  };

  return (
    <div className="max-w-[1000px] mx-auto px-5 py-12" data-testid="cart-page">
      <div className="font-code text-[11px] tracking-[0.3em] text-[#00f0ff] uppercase mb-1">// LOADOUT</div>
      <h1 className="font-display font-bold text-3xl md:text-4xl text-white mb-8">Your Arsenal</h1>

      {items.length === 0 ? (
        <div className="glass clip-hud p-16 text-center" data-testid="empty-cart">
          <ShoppingCart className="w-12 h-12 text-[#00f0ff]/50 mx-auto mb-4" />
          <p className="font-code text-[#8b9bb4] mb-6">Your cart is empty. Time to gear up.</p>
          <Link to="/marketplace" className="inline-flex items-center gap-2 px-6 py-3 clip-hud bg-[#00f0ff] text-black font-display font-bold">
            BROWSE ARSENAL <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      ) : (
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-3">
            {items.map((i) => (
              <div key={i.slug} className="glass clip-hud-sm p-4 flex items-center gap-4" data-testid={`cart-item-${i.slug}`}>
                <div className="w-11 h-11 clip-hud-sm bg-[#00f0ff]/10 border border-[#00f0ff]/30 flex items-center justify-center shrink-0">
                  <Icon name={i.icon} className="w-5 h-5 text-[#00f0ff]" />
                </div>
                <Link to={`/tool/${i.slug}`} className="flex-1">
                  <div className="font-display font-bold text-white hover:text-[#00f0ff] transition-colors">{i.name}</div>
                  <div className="font-code text-xs text-[#8b9bb4]">One-time deployment</div>
                </Link>
                <div className="font-display font-bold text-xl text-white">${i.price.toFixed(0)}</div>
                <button onClick={() => removeItem(i.slug)} data-testid={`remove-${i.slug}`} className="p-2 text-[#8b9bb4] hover:text-[#ff2a2a] transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

          <div className="lg:col-span-1">
            <div className="glass clip-hud p-6 space-y-4 lg:sticky lg:top-24">
              <h2 className="font-display font-bold text-lg text-white">Order Summary</h2>
              <div className="flex justify-between font-code text-sm text-[#8b9bb4]">
                <span>Items ({items.length})</span><span>${total.toFixed(2)}</span>
              </div>
              <div className="flex justify-between font-code text-sm text-[#8b9bb4]">
                <span>Tax</span><span>Calculated at checkout</span>
              </div>
              <div className="border-t border-[#00f0ff]/15 pt-4 flex justify-between items-center">
                <span className="font-display font-bold text-white">Total</span>
                <span className="font-display font-bold text-2xl text-[#00f0ff] text-glow">${total.toFixed(2)}</span>
              </div>
              <button onClick={checkout} disabled={loading} data-testid="checkout-btn"
                className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 clip-hud bg-[#00f0ff] text-black font-display font-bold tracking-wide hover:glow-cyan-strong transition-shadow disabled:opacity-60">
                {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> INITIALIZING…</> : <>SECURE CHECKOUT <ArrowRight className="w-4 h-4" /></>}
              </button>
              <div className="flex items-center gap-2 font-code text-xs text-[#8b9bb4] justify-center">
                <ShieldCheck className="w-3.5 h-3.5 text-[#00f0ff]" /> Encrypted Stripe payment
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
