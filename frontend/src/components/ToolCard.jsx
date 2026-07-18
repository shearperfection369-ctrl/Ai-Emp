import { Link } from "react-router-dom";
import { Icon, ToolIcon } from "../lib/icons";
import { Star, Users, Zap } from "lucide-react";
import { useCart } from "../context/CartContext";
import { toast } from "sonner";
import TierBadge from "./TierBadge";

export default function ToolCard({ tool, index = 0 }) {
  const { addItem, has } = useCart();
  const owned = has(tool.slug);

  return (
    <div
      className="group relative glass clip-hud p-5 flex flex-col animate-hud-in hover:border-[#00f0ff]/60 hover:glow-cyan transition-all duration-300 hover:-translate-y-1"
      style={{ animationDelay: `${Math.min(index * 60, 600)}ms` }}
      data-testid={`tool-card-${tool.slug}`}
    >
      {tool.badge && (
        <span className="absolute top-4 right-4 font-code text-[10px] font-bold tracking-widest uppercase px-2 py-1 clip-hud-sm bg-[#ffb000]/15 text-[#ffb000] border border-[#ffb000]/40">
          {tool.badge}
        </span>
      )}
      <Link to={`/tool/${tool.slug}`} className="flex-1">
        <div className="mb-4"><ToolIcon name={tool.icon} /></div>
        <div className="flex items-center gap-2 mb-1">
          <span className="font-code text-[10px] tracking-[0.25em] uppercase text-[#8b9bb4]">{tool.category}</span>
          {tool.tier && <TierBadge tier={tool.tier} />}
        </div>
        <h3 className="font-display font-bold text-xl text-white group-hover:text-[#00f0ff] transition-colors">{tool.name}</h3>
        <p className="font-code text-sm text-[#8b9bb4] mt-1.5 leading-relaxed line-clamp-2">{tool.tagline}</p>
        <div className="flex items-center gap-4 mt-4 font-code text-xs text-[#8b9bb4]">
          <span className="flex items-center gap-1 text-[#ffb000]"><Star className="w-3.5 h-3.5 fill-[#ffb000]" /> {tool.rating}</span>
          <span className="flex items-center gap-1"><Users className="w-3.5 h-3.5" /> {tool.users.toLocaleString()}</span>
          {tool.speed && <span className="flex items-center gap-1 text-[#00f0ff]"><Zap className="w-3.5 h-3.5" /> {tool.speed}</span>}
        </div>
      </Link>
      <div className="flex items-center justify-between mt-5 pt-4 border-t border-[#00f0ff]/10">
        <div className="font-display font-bold text-2xl text-white">
          ${tool.price.toFixed(0)}<span className="font-code text-xs text-[#8b9bb4] font-normal"> /once</span>
        </div>
        <button
          data-testid={`add-cart-${tool.slug}`}
          disabled={owned}
          onClick={() => { addItem(tool); toast.success(`${tool.name} added to arsenal`); }}
          className="px-4 py-2 clip-hud-sm font-display font-bold text-sm tracking-wide transition-all disabled:opacity-50 disabled:cursor-not-allowed bg-[#00f0ff]/10 border border-[#00f0ff]/40 text-[#00f0ff] hover:bg-[#00f0ff] hover:text-black"
        >
          {owned ? "IN CART" : "DEPLOY"}
        </button>
      </div>
    </div>
  );
}
