import { useEffect, useState } from "react";
import api from "../lib/api";
import { DollarSign, ShoppingBag, Users, Boxes, TrendingUp, Loader2 } from "lucide-react";
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

const fmt = (n) => `$${Number(n || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

function StatCard({ icon: Ic, label, value, accent = "#00f0ff" }) {
  return (
    <div className="glass clip-hud p-5" data-testid={`stat-${label.toLowerCase().replace(/\s/g, "-")}`}>
      <div className="flex items-center justify-between">
        <div className="font-code text-[10px] tracking-widest uppercase text-[#8b9bb4]">{label}</div>
        <Ic className="w-4 h-4" style={{ color: accent }} />
      </div>
      <div className="font-orbit font-bold text-3xl mt-2" style={{ color: accent }}>{value}</div>
    </div>
  );
}

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get("/admin/stats").then(({ data }) => setStats(data));
    api.get("/admin/orders").then(({ data }) => setOrders(data));
  }, []);

  if (!stats) return <div className="flex justify-center py-32"><Loader2 className="w-8 h-8 text-[#00f0ff] animate-spin" /></div>;

  return (
    <div className="max-w-[1400px] mx-auto px-5 py-12" data-testid="admin-page">
      <div className="font-code text-[11px] tracking-[0.3em] text-[#ffb000] uppercase mb-1">// RESTRICTED ACCESS</div>
      <h1 className="font-display font-bold text-3xl md:text-4xl text-white mb-8">Command Center</h1>

      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <StatCard icon={DollarSign} label="Revenue" value={fmt(stats.total_revenue)} />
        <StatCard icon={ShoppingBag} label="Orders" value={stats.total_orders} accent="#ffb000" />
        <StatCard icon={TrendingUp} label="Avg Order" value={fmt(stats.aov)} />
        <StatCard icon={Users} label="Operators" value={stats.total_users} accent="#ffb000" />
        <StatCard icon={Boxes} label="Tools Live" value={stats.total_tools} />
      </div>

      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        <div className="glass clip-hud p-6">
          <h2 className="font-display font-bold text-lg text-white mb-4">Revenue Signal (last 14 days)</h2>
          <ResponsiveContainer width="100%" height={240}>
            <AreaChart data={stats.revenue_series}>
              <defs>
                <linearGradient id="rev" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#00f0ff" stopOpacity={0.5} />
                  <stop offset="100%" stopColor="#00f0ff" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,240,255,0.08)" />
              <XAxis dataKey="date" tick={{ fill: "#8b9bb4", fontSize: 10, fontFamily: "JetBrains Mono" }} />
              <YAxis tick={{ fill: "#8b9bb4", fontSize: 10 }} />
              <Tooltip contentStyle={{ background: "#0a1118", border: "1px solid rgba(0,240,255,0.3)", fontFamily: "JetBrains Mono", fontSize: 12 }} />
              <Area type="monotone" dataKey="revenue" stroke="#00f0ff" strokeWidth={2} fill="url(#rev)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <div className="glass clip-hud p-6">
          <h2 className="font-display font-bold text-lg text-white mb-4">Top Performing Tools</h2>
          {stats.top_tools.length === 0 ? (
            <div className="h-[240px] flex items-center justify-center font-code text-sm text-[#8b9bb4]">No sales yet.</div>
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={stats.top_tools} layout="vertical" margin={{ left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,240,255,0.08)" />
                <XAxis type="number" tick={{ fill: "#8b9bb4", fontSize: 10 }} />
                <YAxis type="category" dataKey="name" width={90} tick={{ fill: "#8b9bb4", fontSize: 10, fontFamily: "JetBrains Mono" }} />
                <Tooltip contentStyle={{ background: "#0a1118", border: "1px solid rgba(0,240,255,0.3)", fontFamily: "JetBrains Mono", fontSize: 12 }} />
                <Bar dataKey="revenue" fill="#ffb000" radius={[0, 3, 3, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="glass clip-hud p-6" data-testid="orders-table">
        <h2 className="font-display font-bold text-lg text-white mb-4">Recent Transactions</h2>
        <div className="overflow-x-auto">
          <table className="w-full font-code text-sm">
            <thead>
              <tr className="text-[#8b9bb4] text-xs uppercase tracking-widest border-b border-[#00f0ff]/15">
                <th className="text-left py-3 px-2">Customer</th>
                <th className="text-left py-3 px-2">Items</th>
                <th className="text-left py-3 px-2">Amount</th>
                <th className="text-left py-3 px-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {orders.length === 0 ? (
                <tr><td colSpan={4} className="py-8 text-center text-[#8b9bb4]">No transactions yet.</td></tr>
              ) : orders.map((o) => (
                <tr key={o.session_id} className="border-b border-[#00f0ff]/8 hover:bg-[#00f0ff]/5 transition-colors">
                  <td className="py-3 px-2 text-white">{o.user_email || "Guest"}</td>
                  <td className="py-3 px-2 text-[#8b9bb4]">{(o.items || []).map((i) => i.name).join(", ")}</td>
                  <td className="py-3 px-2 text-white">{fmt(o.amount)}</td>
                  <td className="py-3 px-2">
                    <span className={`px-2 py-1 clip-hud-sm text-[10px] uppercase tracking-widest border ${
                      o.payment_status === "paid" ? "bg-[#00f0ff]/15 text-[#00f0ff] border-[#00f0ff]/40" :
                      o.payment_status === "pending" ? "bg-[#ffb000]/15 text-[#ffb000] border-[#ffb000]/40" :
                      "bg-[#ff2a2a]/15 text-[#ff8080] border-[#ff2a2a]/40"}`}>
                      {o.payment_status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
