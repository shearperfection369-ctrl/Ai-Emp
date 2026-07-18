import { Icon, ToolIcon } from "../lib/icons";
import { useCart } from "../context/CartContext";
import { toast } from "sonner";
import { Check, PlusCircle } from "lucide-react";

export default function BundleCard({ bundle, index = 0 }) {
  const { addItem, has } = useCart();
  const inCart = has(bundle.slug);

  return (
    <div
      className="group relative glass clip-hud p-6 flex flex-col animate-hud-in hover:border-[#ffb000]/50 transition-all duration-300 hover:-translate-y-1"
      style={{ animationDelay: `${index * 70}ms` }}
      data-testid={`bundle-card-${bundle.slug}`}
    >
      <div className="absolute top-4 right-4 font-code text-[10px] font-bold tracking-widest uppercase px-2 py-1 clip-hud-sm bg-[#ffb000]/15 text-[#ffb000] border border-[#ffb000]/40">
        SAVE {bundle.savings_pct}%
      </div>
      <div className="flex items-center gap-3 mb-3">
        <ToolIcon name={bundle.icon} accent="#ffb000" />
        <div>
          <div className="font-code text-[10px] tracking-[0.25em] uppercase text-[#8b9bb4]">Value Bundle</div>
          <h3 className="font-display font-bold text-xl text-white">{bundle.name}</h3>
        </div>
      </div>
      <p className="font-code text-sm text-[#8b9bb4] leading-relaxed">{bundle.tagline}</p>

      <div className="mt-4 space-y-2 flex-1">
        {bundle.tools.map((t) => (
          <div key={t.slug} className="flex items-center gap-2 font-code text-sm text-[#e6f6ff]">
            <Check className="w-3.5 h-3.5 text-[#ffb000] shrink-0" />
            <Icon name={t.icon} className="w-3.5 h-3.5 text-[#00f0ff]" />
            {t.name}
            <span className="ml-auto text-[#8b9bb4] text-xs">${t.price.toFixed(0)}</span>
          </div>
        ))}
      </div>

      <div className="flex items-center justify-between mt-5 pt-4 border-t border-[#ffb000]/15">
        <div>
          <div className="font-code text-xs text-[#8b9bb4] line-through">${bundle.original_price.toFixed(0)}</div>
          <div className="font-display font-bold text-2xl text-[#ffb000] text-glow-amber">${bundle.price.toFixed(0)}</div>
        </div>
        <button
          data-testid={`add-bundle-${bundle.slug}`}
          disabled={inCart}
          onClick={() => { addItem({ ...bundle }); toast.success(`${bundle.name} added to arsenal`); }}
          className="inline-flex items-center gap-1.5 px-4 py-2 clip-hud-sm font-display font-bold text-sm tracking-wide transition-all disabled:opacity-50 bg-[#ffb000]/10 border border-[#ffb000]/40 text-[#ffb000] hover:bg-[#ffb000] hover:text-black"
        >
          <PlusCircle className="w-4 h-4" /> {inCart ? "IN CART" : "GET PACK"}
        </button>
      </div>
    </div>
  );
}
