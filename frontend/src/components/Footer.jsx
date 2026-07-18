import { Link } from "react-router-dom";
import { Zap } from "lucide-react";

export default function Footer() {
  return (
    <footer className="relative z-10 border-t border-[#00f0ff]/15 mt-24 glass" data-testid="footer">
      <div className="max-w-[1400px] mx-auto px-5 py-12 grid md:grid-cols-4 gap-8">
        <div className="md:col-span-2">
          <div className="flex items-center gap-2 mb-3">
            <Zap className="w-5 h-5 text-[#00f0ff]" />
            <span className="font-orbit font-bold tracking-widest text-white">AI TOOL <span className="text-[#00f0ff]">EMPORIUM</span></span>
          </div>
          <p className="font-code text-sm text-[#8b9bb4] max-w-md leading-relaxed">
            The one-stop arsenal for battle-ready AI tools across every industry. Packaged, deployed, and ready to sell you results — not promises.
          </p>
        </div>
        <div>
          <div className="font-display font-semibold tracking-widest text-[#00f0ff] text-xs uppercase mb-3">Navigate</div>
          <ul className="space-y-2 font-code text-sm text-[#8b9bb4]">
            <li><Link to="/marketplace" className="hover:text-white transition-colors">Marketplace</Link></li>
            <li><Link to="/branding" className="hover:text-white transition-colors">Brand Kit</Link></li>
            <li><Link to="/library" className="hover:text-white transition-colors">My Library</Link></li>
          </ul>
        </div>
        <div>
          <div className="font-display font-semibold tracking-widest text-[#00f0ff] text-xs uppercase mb-3">System</div>
          <ul className="space-y-2 font-code text-sm text-[#8b9bb4]">
            <li className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#00f0ff] animate-blink" /> All systems operational</li>
            <li>Secure Stripe payments</li>
            <li>Powered by ARIA AI</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-[#00f0ff]/10 py-4 text-center font-code text-xs text-[#8b9bb4]/70">
        © 2026 AI TOOL EMPORIUM // ALL SYSTEMS NOMINAL
      </div>
    </footer>
  );
}
