import { useEffect, useState, useRef } from "react";
import { useSearchParams, Link } from "react-router-dom";
import api from "../lib/api";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import { CheckCircle2, Loader2, XCircle, ArrowRight, Library as LibIcon } from "lucide-react";

export default function PaymentSuccess() {
  const [params] = useSearchParams();
  const { clear } = useCart();
  const { refreshUser } = useAuth();
  const [state, setState] = useState("checking"); // checking | paid | failed
  const [info, setInfo] = useState(null);
  const clearedRef = useRef(false);

  useEffect(() => {
    const sessionId = params.get("session_id");
    if (!sessionId) { setState("failed"); return; }
    let attempts = 0;
    let timer;
    const poll = async () => {
      attempts += 1;
      try {
        const { data } = await api.get(`/payments/status/${sessionId}`);
        if (data.payment_status === "paid") {
          setInfo(data);
          setState("paid");
          if (!clearedRef.current) { clear(); refreshUser(); clearedRef.current = true; }
          return;
        }
        if (["expired", "failed"].includes(data.payment_status)) { setState("failed"); return; }
      } catch { /* keep polling */ }
      if (attempts >= 8) { setState("failed"); return; }
      timer = setTimeout(poll, 2000);
    };
    poll();
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="max-w-lg mx-auto px-5 py-24 text-center" data-testid="payment-success-page">
      {state === "checking" && (
        <div className="glass clip-hud p-12 animate-hud-in">
          <Loader2 className="w-12 h-12 text-[#00f0ff] animate-spin mx-auto mb-5" />
          <h1 className="font-display font-bold text-2xl text-white">Verifying Transaction</h1>
          <p className="font-code text-sm text-[#8b9bb4] mt-2">Confirming deployment with secure payment relay…</p>
        </div>
      )}
      {state === "paid" && (
        <div className="glass clip-hud p-12 animate-hud-in glow-cyan">
          <CheckCircle2 className="w-14 h-14 text-[#00f0ff] mx-auto mb-5" />
          <h1 className="font-display font-bold text-3xl text-white">Deployment Complete</h1>
          <p className="font-code text-sm text-[#8b9bb4] mt-2">
            {info?.items?.length || 0} tool(s) unlocked · {info ? `$${Number(info.amount).toFixed(2)}` : ""}
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center mt-8">
            <Link to="/library" data-testid="success-library" className="inline-flex items-center justify-center gap-2 px-6 py-3 clip-hud bg-[#00f0ff] text-black font-display font-bold">
              <LibIcon className="w-4 h-4" /> OPEN LIBRARY
            </Link>
            <Link to="/marketplace" className="inline-flex items-center justify-center gap-2 px-6 py-3 clip-hud glass border border-[#00f0ff]/40 text-white font-display font-bold">
              KEEP BROWSING <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      )}
      {state === "failed" && (
        <div className="glass clip-hud p-12 animate-hud-in">
          <XCircle className="w-14 h-14 text-[#ff2a2a] mx-auto mb-5" />
          <h1 className="font-display font-bold text-2xl text-white">Verification Delayed</h1>
          <p className="font-code text-sm text-[#8b9bb4] mt-2">We couldn't confirm the payment yet. If you were charged, it will appear in your library shortly.</p>
          <Link to="/library" className="inline-flex items-center gap-2 px-6 py-3 clip-hud bg-[#00f0ff] text-black font-display font-bold mt-8">GO TO LIBRARY</Link>
        </div>
      )}
    </div>
  );
}
