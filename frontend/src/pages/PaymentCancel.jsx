import { Link } from "react-router-dom";
import { XCircle, ArrowLeft } from "lucide-react";

export default function PaymentCancel() {
  return (
    <div className="max-w-lg mx-auto px-5 py-24 text-center" data-testid="payment-cancel-page">
      <div className="glass clip-hud p-12 animate-hud-in">
        <XCircle className="w-14 h-14 text-[#ffb000] mx-auto mb-5" />
        <h1 className="font-display font-bold text-2xl text-white">Checkout Aborted</h1>
        <p className="font-code text-sm text-[#8b9bb4] mt-2">No charge was made. Your arsenal is still waiting in your cart.</p>
        <Link to="/cart" className="inline-flex items-center gap-2 px-6 py-3 clip-hud bg-[#00f0ff] text-black font-display font-bold mt-8">
          <ArrowLeft className="w-4 h-4" /> RETURN TO CART
        </Link>
      </div>
    </div>
  );
}
