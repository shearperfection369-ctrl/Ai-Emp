import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Zap, Loader2, LogIn } from "lucide-react";

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
function googleLogin() {
  const redirectUrl = window.location.origin + "/library";
  window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
}

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError(""); setLoading(true);
    const res = await login(email, password);
    setLoading(false);
    if (res.ok) navigate("/library");
    else setError(res.error);
  };

  return (
    <div className="max-w-md mx-auto px-5 py-16" data-testid="login-page">
      <div className="glass clip-hud p-8 animate-hud-in">
        <div className="flex items-center gap-3 mb-6">
          <img src="/logo-mark.png" alt="AI Tool Emporium" className="w-12 h-12 object-contain drop-shadow-[0_0_12px_rgba(0,240,255,0.5)]" />
          <div>
            <h1 className="font-display font-bold text-2xl text-white">Access Terminal</h1>
            <p className="font-code text-xs text-[#8b9bb4]">Authenticate to enter the Emporium</p>
          </div>
        </div>

        {error && <div className="mb-4 clip-hud-sm bg-[#ff2a2a]/10 border border-[#ff2a2a]/40 px-4 py-2.5 font-code text-sm text-[#ff8080]" data-testid="login-error">{error}</div>}

        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="font-code text-xs tracking-widest text-[#8b9bb4] uppercase">Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required data-testid="login-email"
              className="w-full mt-1.5 bg-[#050a10] border border-[#00f0ff]/25 clip-hud-sm px-3 py-2.5 font-code text-sm text-white outline-none focus:border-[#00f0ff]" />
          </div>
          <div>
            <label className="font-code text-xs tracking-widest text-[#8b9bb4] uppercase">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required data-testid="login-password"
              className="w-full mt-1.5 bg-[#050a10] border border-[#00f0ff]/25 clip-hud-sm px-3 py-2.5 font-code text-sm text-white outline-none focus:border-[#00f0ff]" />
          </div>
          <button type="submit" disabled={loading} data-testid="login-submit"
            className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 clip-hud bg-[#00f0ff] text-black font-display font-bold tracking-wide hover:glow-cyan-strong transition-shadow disabled:opacity-60">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <LogIn className="w-4 h-4" />} AUTHENTICATE
          </button>
        </form>

        <div className="flex items-center gap-3 my-5">
          <div className="flex-1 h-px bg-[#00f0ff]/15" />
          <span className="font-code text-xs text-[#8b9bb4]">OR</span>
          <div className="flex-1 h-px bg-[#00f0ff]/15" />
        </div>

        <button onClick={googleLogin} data-testid="google-login"
          className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 clip-hud glass border border-[#00f0ff]/40 text-white font-display font-semibold hover:border-[#00f0ff] transition-colors">
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="" className="w-4 h-4" />
          Continue with Google
        </button>

        <p className="font-code text-sm text-[#8b9bb4] text-center mt-6">
          No credentials? <Link to="/register" className="text-[#00f0ff] hover:text-glow" data-testid="to-register">Register here</Link>
        </p>
      </div>
    </div>
  );
}
