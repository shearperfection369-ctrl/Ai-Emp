import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";
import { ShoppingCart, Zap, LogOut, LayoutDashboard, Library as LibIcon, Menu, X } from "lucide-react";
import { useState } from "react";

export default function Navbar() {
  const { user, logout } = useAuth();
  const { count } = useCart();
  const navigate = useNavigate();
  const location = useLocation();
  const [open, setOpen] = useState(false);

  const links = [
    { to: "/marketplace", label: "Marketplace" },
    { to: "/branding", label: "Brand Kit" },
  ];

  const active = (to) => location.pathname === to;

  return (
    <nav className="fixed top-0 inset-x-0 z-50 glass-strong border-b border-[#00f0ff]/20" data-testid="navbar">
      <div className="max-w-[1400px] mx-auto px-5 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2.5 group" data-testid="nav-logo">
          <img src="/logo-mark.png" alt="AI Tool Emporium" className="w-10 h-10 object-contain drop-shadow-[0_0_10px_rgba(0,240,255,0.5)] group-hover:drop-shadow-[0_0_16px_rgba(0,240,255,0.75)] transition-all" />
          <div className="leading-none">
            <div className="font-orbit text-[15px] font-bold tracking-widest text-white">
              AI TOOL <span className="text-[#00f0ff] text-glow">EMPORIUM</span>
            </div>
            <div className="font-code text-[9px] text-[#8b9bb4] tracking-[0.35em] mt-0.5">FUTURE-GRADE AI ARSENAL</div>
          </div>
        </Link>

        <div className="hidden md:flex items-center gap-1">
          {links.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              data-testid={`nav-${l.label.toLowerCase().replace(/\s/g, "-")}`}
              className={`px-4 py-2 font-display font-medium tracking-wide text-sm transition-colors ${
                active(l.to) ? "text-[#00f0ff] text-glow" : "text-[#8b9bb4] hover:text-white"
              }`}
            >
              {l.label}
            </Link>
          ))}
          {user && (
            <Link to="/library" data-testid="nav-library"
              className={`px-4 py-2 font-display font-medium tracking-wide text-sm transition-colors flex items-center gap-1.5 ${active("/library") ? "text-[#00f0ff]" : "text-[#8b9bb4] hover:text-white"}`}>
              <LibIcon className="w-4 h-4" /> Library
            </Link>
          )}
          {user?.role === "admin" && (
            <Link to="/admin" data-testid="nav-admin"
              className={`px-4 py-2 font-display font-medium tracking-wide text-sm transition-colors flex items-center gap-1.5 ${active("/admin") ? "text-[#ffb000]" : "text-[#8b9bb4] hover:text-[#ffb000]"}`}>
              <LayoutDashboard className="w-4 h-4" /> Command
            </Link>
          )}
        </div>

        <div className="flex items-center gap-3">
          <Link to="/cart" className="relative p-2 text-[#8b9bb4] hover:text-[#00f0ff] transition-colors" data-testid="nav-cart">
            <ShoppingCart className="w-5 h-5" />
            {count > 0 && (
              <span className="absolute -top-0.5 -right-0.5 bg-[#00f0ff] text-black text-[10px] font-bold w-4 h-4 flex items-center justify-center rounded-full glow-cyan" data-testid="cart-count">
                {count}
              </span>
            )}
          </Link>

          {user ? (
            <div className="hidden sm:flex items-center gap-2.5">
              <div className="w-8 h-8 clip-hud-sm bg-[#00f0ff]/15 border border-[#00f0ff]/40 flex items-center justify-center font-display font-bold text-[#00f0ff] text-sm">
                {(user.name || user.email || "U")[0].toUpperCase()}
              </div>
              <button onClick={() => { logout(); navigate("/"); }} data-testid="nav-logout"
                className="p-2 text-[#8b9bb4] hover:text-[#ff2a2a] transition-colors">
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <Link to="/login" data-testid="nav-login"
              className="hidden sm:inline-flex px-5 py-2 clip-hud-sm bg-[#00f0ff] text-black font-display font-bold text-sm tracking-wide hover:glow-cyan-strong transition-shadow">
              ACCESS
            </Link>
          )}

          <button className="md:hidden p-2 text-[#00f0ff]" onClick={() => setOpen((o) => !o)} data-testid="nav-mobile-toggle">
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {open && (
        <div className="md:hidden glass-strong border-t border-[#00f0ff]/20 px-5 py-4 flex flex-col gap-2" data-testid="nav-mobile-menu">
          {links.map((l) => (
            <Link key={l.to} to={l.to} onClick={() => setOpen(false)} className="py-2 font-display text-[#8b9bb4] hover:text-[#00f0ff]">{l.label}</Link>
          ))}
          {user && <Link to="/library" onClick={() => setOpen(false)} className="py-2 font-display text-[#8b9bb4]">Library</Link>}
          {user?.role === "admin" && <Link to="/admin" onClick={() => setOpen(false)} className="py-2 font-display text-[#ffb000]">Command Center</Link>}
          {user
            ? <button onClick={() => { logout(); setOpen(false); navigate("/"); }} className="py-2 text-left font-display text-[#ff2a2a]">Disconnect</button>
            : <Link to="/login" onClick={() => setOpen(false)} className="py-2 font-display text-[#00f0ff]">Access Terminal</Link>}
        </div>
      )}
    </nav>
  );
}
