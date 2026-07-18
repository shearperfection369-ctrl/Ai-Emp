import { useEffect, useState, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import api from "../lib/api";
import { Icon } from "../lib/icons";
import ToolCard from "../components/ToolCard";
import { Search } from "lucide-react";

const SORTS = [
  { id: "popular", label: "Most Deployed" },
  { id: "rating", label: "Top Rated" },
  { id: "price_asc", label: "Price ↑" },
  { id: "price_desc", label: "Price ↓" },
];

export default function Marketplace() {
  const [params, setParams] = useSearchParams();
  const [tools, setTools] = useState([]);
  const [categories, setCategories] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const category = params.get("category") || "all";
  const sort = params.get("sort") || "popular";

  const load = useCallback(async () => {
    setLoading(true);
    const { data } = await api.get("/tools", { params: { category, sort, search: search || undefined } });
    setTools(data);
    setLoading(false);
  }, [category, sort, search]);

  useEffect(() => { api.get("/categories").then(({ data }) => setCategories(data)); }, []);
  useEffect(() => { const t = setTimeout(load, search ? 300 : 0); return () => clearTimeout(t); }, [load, search]);

  const setParam = (key, val) => {
    const next = new URLSearchParams(params);
    if (val && val !== "all") next.set(key, val); else next.delete(key);
    setParams(next);
  };

  return (
    <div className="max-w-[1400px] mx-auto px-5 py-12" data-testid="marketplace-page">
      <div className="mb-8">
        <div className="font-code text-[11px] tracking-[0.3em] text-[#00f0ff] uppercase mb-1">// ARSENAL</div>
        <h1 className="font-display font-bold text-3xl md:text-5xl text-white">The Marketplace</h1>
        <p className="font-code text-[#8b9bb4] mt-2">Browse {tools.length} battle-ready AI tools. Try any of them live before you deploy.</p>
      </div>

      <div className="flex flex-col lg:flex-row gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#8b9bb4]" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search tools, industries, capabilities…"
            data-testid="search-input"
            className="w-full glass clip-hud-sm pl-10 pr-4 py-3 font-code text-sm text-white outline-none focus:border-[#00f0ff] placeholder:text-[#8b9bb4]/60"
          />
        </div>
        <div className="flex gap-2 flex-wrap">
          {SORTS.map((s) => (
            <button key={s.id} onClick={() => setParam("sort", s.id)} data-testid={`sort-${s.id}`}
              className={`px-3.5 py-2 clip-hud-sm font-code text-xs tracking-wide transition-colors border ${
                sort === s.id ? "bg-[#00f0ff]/15 border-[#00f0ff]/50 text-[#00f0ff]" : "glass border-[#00f0ff]/15 text-[#8b9bb4] hover:text-white"
              }`}>{s.label}</button>
          ))}
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-8">
        <button onClick={() => setParam("category", "all")} data-testid="filter-all"
          className={`px-4 py-2 clip-hud-sm font-display font-semibold text-sm transition-colors border ${category === "all" ? "bg-[#00f0ff] text-black border-[#00f0ff]" : "glass border-[#00f0ff]/15 text-[#8b9bb4] hover:text-white"}`}>
          All Tools
        </button>
        {categories.map((c) => (
          <button key={c.id} onClick={() => setParam("category", c.id)} data-testid={`filter-${c.id}`}
            className={`px-4 py-2 clip-hud-sm font-display font-semibold text-sm transition-colors border flex items-center gap-1.5 ${
              category === c.id ? "bg-[#00f0ff] text-black border-[#00f0ff]" : "glass border-[#00f0ff]/15 text-[#8b9bb4] hover:text-white"}`}>
            <Icon name={c.icon} className="w-3.5 h-3.5" /> {c.name}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {Array.from({ length: 6 }).map((_, i) => <div key={i} className="glass clip-hud h-64 animate-pulse" />)}
        </div>
      ) : tools.length === 0 ? (
        <div className="glass clip-hud p-16 text-center font-code text-[#8b9bb4]" data-testid="no-results">
          No tools matched your scan parameters.
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5" data-testid="tools-grid">
          {tools.map((t, i) => <ToolCard key={t.slug} tool={t} index={i} />)}
        </div>
      )}
    </div>
  );
}
