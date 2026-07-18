import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../lib/api";
import { Icon, ToolIcon } from "../lib/icons";
import { useAuth } from "../context/AuthContext";
import { Package, ArrowRight, Loader2 } from "lucide-react";

export default function Library() {
  const { user } = useAuth();
  const [tools, setTools] = useState(null);

  useEffect(() => {
    api.get("/library").then(({ data }) => setTools(data)).catch(() => setTools([]));
  }, []);

  return (
    <div className="max-w-[1400px] mx-auto px-5 py-12" data-testid="library-page">
      <div className="font-code text-[11px] tracking-[0.3em] text-[#00f0ff] uppercase mb-1">// OPERATOR {user?.name || ""}</div>
      <h1 className="font-display font-bold text-3xl md:text-4xl text-white mb-2">Your Library</h1>
      <p className="font-code text-[#8b9bb4] mb-8">Every AI tool you own, ready to deploy.</p>

      {tools === null ? (
        <div className="flex justify-center py-24"><Loader2 className="w-8 h-8 text-[#00f0ff] animate-spin" /></div>
      ) : tools.length === 0 ? (
        <div className="glass clip-hud p-16 text-center" data-testid="empty-library">
          <Package className="w-12 h-12 text-[#00f0ff]/50 mx-auto mb-4" />
          <p className="font-code text-[#8b9bb4] mb-6">Your library is empty. Acquire your first AI tool.</p>
          <Link to="/marketplace" className="inline-flex items-center gap-2 px-6 py-3 clip-hud bg-[#00f0ff] text-black font-display font-bold">
            BROWSE ARSENAL <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5" data-testid="library-grid">
          {tools.map((t, i) => (
            <Link to={`/tool/${t.slug}`} key={t.slug} data-testid={`library-tool-${t.slug}`}
              className="glass clip-hud p-6 hover:border-[#00f0ff]/60 hover:glow-cyan transition-all hover:-translate-y-1 animate-hud-in" style={{ animationDelay: `${i * 60}ms` }}>
              <div className="flex items-center justify-between mb-4">
                <ToolIcon name={t.icon} />
                <span className="font-code text-[10px] tracking-widest uppercase px-2 py-1 clip-hud-sm bg-[#00f0ff]/15 text-[#00f0ff] border border-[#00f0ff]/40">OWNED</span>
              </div>
              <h3 className="font-display font-bold text-xl text-white">{t.name}</h3>
              <p className="font-code text-sm text-[#8b9bb4] mt-1">{t.tagline}</p>
              <div className="mt-4 pt-4 border-t border-[#00f0ff]/10 font-code text-xs text-[#00f0ff] flex items-center gap-1.5">
                LAUNCH TOOL <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
