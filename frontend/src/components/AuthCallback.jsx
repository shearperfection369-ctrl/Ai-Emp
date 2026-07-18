import { useEffect, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../lib/api";
import { useAuth } from "../context/AuthContext";

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
export default function AuthCallback() {
  const navigate = useNavigate();
  const location = useLocation();
  const { setUser } = useAuth();
  const processed = useRef(false);

  useEffect(() => {
    if (processed.current) return;
    processed.current = true;
    const hash = location.hash || window.location.hash;
    const sid = new URLSearchParams(hash.replace("#", "")).get("session_id");
    if (!sid) { navigate("/"); return; }
    (async () => {
      try {
        const { data } = await api.post("/auth/session", {}, { headers: { "X-Session-ID": sid } });
        setUser(data.user);
        window.history.replaceState({}, "", "/library");
        navigate("/library", { replace: true });
      } catch {
        navigate("/login", { replace: true });
      }
    })();
  }, [location, navigate, setUser]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4" data-testid="auth-callback">
      <div className="w-12 h-12 border-2 border-[#00f0ff]/30 border-t-[#00f0ff] rounded-full animate-spin glow-cyan" />
      <p className="font-code text-[#8b9bb4] text-sm tracking-widest uppercase">Establishing secure uplink…</p>
    </div>
  );
}
