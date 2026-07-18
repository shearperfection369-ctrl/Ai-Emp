const TIERS = {
  Gold: { c: "#ffb000", bg: "rgba(255,176,0,0.12)" },
  Silver: { c: "#c7d0dc", bg: "rgba(199,208,220,0.12)" },
  Bronze: { c: "#e08b4c", bg: "rgba(224,139,76,0.12)" },
};

export default function TierBadge({ tier, className = "" }) {
  const t = TIERS[tier] || TIERS.Silver;
  return (
    <span
      className={`font-code text-[10px] font-bold tracking-widest uppercase px-2 py-0.5 clip-hud-sm border inline-flex items-center gap-1 ${className}`}
      style={{ color: t.c, background: t.bg, borderColor: t.c + "66" }}
      data-testid={`tier-${tier}`}
    >
      <span className="w-1.5 h-1.5 rounded-full" style={{ background: t.c }} />
      {tier}
    </span>
  );
}
