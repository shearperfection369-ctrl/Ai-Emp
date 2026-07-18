import * as LucideIcons from "lucide-react";

export function Icon({ name, ...props }) {
  const Cmp = LucideIcons[name] || LucideIcons.Box;
  return <Cmp {...props} />;
}

// Polished, high-tech holographic icon tile with a rotating light-sweep ring + glow.
export function ToolIcon({ name, size = "md", accent = "#00f0ff", className = "" }) {
  const dims = size === "lg" ? "w-16 h-16" : size === "sm" ? "w-10 h-10" : "w-12 h-12";
  const isz = size === "lg" ? "w-7 h-7" : size === "sm" ? "w-5 h-5" : "w-6 h-6";
  const Cmp = LucideIcons[name] || LucideIcons.Box;
  return (
    <div className={`relative ${dims} shrink-0 ${className}`}>
      {/* ambient glow */}
      <div className="absolute -inset-1 rounded-md opacity-60 blur-[6px]"
        style={{ background: `radial-gradient(circle at 50% 45%, ${accent}55, transparent 70%)` }} />
      {/* rotating light sweep ring */}
      <div className="absolute inset-0 clip-hud-sm animate-spin" style={{ animationDuration: "7s",
        background: `conic-gradient(from 0deg, transparent 0deg, ${accent} 60deg, transparent 150deg, transparent 360deg)` }} />
      {/* inner tile */}
      <div className="absolute inset-[1.5px] clip-hud-sm flex items-center justify-center overflow-hidden"
        style={{ background: "linear-gradient(150deg, rgba(0,240,255,0.10) 0%, rgba(6,11,18,0.96) 60%)",
          boxShadow: `inset 0 0 14px ${accent}30` }}>
        <div className="absolute inset-0 scanlines opacity-40" />
        <span className="absolute top-1 left-1 w-1.5 h-1.5 border-t border-l" style={{ borderColor: accent }} />
        <span className="absolute bottom-1 right-1 w-1.5 h-1.5 border-b border-r" style={{ borderColor: accent }} />
        <Cmp className={`${isz} relative z-10`} strokeWidth={1.7}
          style={{ color: accent, filter: `drop-shadow(0 0 6px ${accent}) drop-shadow(0 0 2px ${accent})` }} />
      </div>
    </div>
  );
}

