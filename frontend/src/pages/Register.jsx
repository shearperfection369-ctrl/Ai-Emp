import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Zap, Loader2, UserPlus } from "lucide-react";

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
function googleLogin() {
  const redirectUrl = window.location.origin + "/library";
  window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
}

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError(""); setLoading(true);
    const res = await register(name, email, password);
    setLoading(false);
    if (res.ok) navigate("/library");
    else setError(res.error);
  };

  return (
    <div className="max-w-md mx-auto px-5 py-16" data-testid="register-page">
      <div className="glass clip-hud p-8 animate-hud-in">
        <div className="flex items-center gap-2 mb-6">
          <div className="w-10 h-10 clip-hud-sm bg-[#00f0ff]/10 border border-[#00f0ff]/40 flex items-center justify-center glow-cyan">
            <Zap className="w-5 h-5 text-[#00f0ff]" />
          </div>
          <div>
            <h1 className="font-display font-bold text-2xl text-white">Enlist Now</h1>
            <p className="font-code text-xs text-[#8b9bb4]">Create your operator profile</p>
          </div>
        </div>

        {error && <div className="mb-4 clip-hud-sm bg-[#ff2a2a]/10 border border-[#ff2a2a]/40 px-4 py-2.5 font-code text-sm text-[#ff8080]" data-testid="register-error">{error}</div>}

        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="font-code text-xs tracking-widest text-[#8b9bb4] uppercase">Callsign / Name</label>
            <input value={name} onChange={(e) => setName(e.target.value)} required data-testid="register-name"
              className="w-full mt-1.5 bg-[#050a10] border border-[#00f0ff]/25 clip-hud-sm px-3 py-2.5 font-code text-sm text-white outline-none focus:border-[#00f0ff]" />
          </div>
          <div>
            <label className="font-code text-xs tracking-widest text-[#8b9bb4] uppercase">Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required data-testid="register-email"
              className="w-full mt-1.5 bg-[#050a10] border border-[#00f0ff]/25 clip-hud-sm px-3 py-2.5 font-code text-sm text-white outline-none focus:border-[#00f0ff]" />
          </div>
          <div>
            <label className="font-code text-xs tracking-widest text-[#8b9bb4] uppercase">Password (min 6)</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={6} data-testid="register-password"
              className="w-full mt-1.5 bg-[#050a10] border border-[#00f0ff]/25 clip-hud-sm px-3 py-2.5 font-code text-sm text-white outline-none focus:border-[#00f0ff]" />
          </div>
          <button type="submit" disabled={loading} data-testid="register-submit"
            className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 clip-hud bg-[#00f0ff] text-black font-display font-bold tracking-wide hover:glow-cyan-strong transition-shadow disabled:opacity-60">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <UserPlus className="w-4 h-4" />} DEPLOY PROFILE
          </button>
        </form>

        <div className="flex items-center gap-3 my-5">
          <div className="flex-1 h-px bg-[#00f0ff]/15" />
          <span className="font-code text-xs text-[#8b9bb4]">OR</span>
          <div className="flex-1 h-px bg-[#00f0ff]/15" />
        </div>

        <button onClick={googleLogin} data-testid="google-register"
          className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 clip-hud glass border border-[#00f0ff]/40 text-white font-display font-semibold hover:border-[#00f0ff] transition-colors">
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="" className="w-4 h-4" />
          Continue with Google
        </button>

        <p className="font-code text-sm text-[#8b9bb4] text-center mt-6">
          Already enlisted? <Link to="/login" className="text-[#00f0ff] hover:text-glow" data-testid="to-login">Access terminal</Link>
        </p>
      </div>
    </div>
  );
}
