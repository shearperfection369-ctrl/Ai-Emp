import { useEffect, useRef } from "react";

// Futuristic JARVIS-inspired animated HUD backdrop:
// drifting particle constellation + mouse reactivity + sonar pings + rotating reticle.
export default function StarField() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    let raf, w, h, nodes = [], rings = [], t = 0;
    const mouse = { x: -9999, y: -9999 };
    const CYAN = "0, 240, 255";
    const AMBER = "255, 176, 0";

    const init = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
      const count = Math.min(130, Math.floor((w * h) / 15000));
      nodes = Array.from({ length: count }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.28,
        vy: (Math.random() - 0.5) * 0.28,
        r: Math.random() * 1.6 + 0.6,
        amber: Math.random() < 0.12,
      }));
    };

    const spawnRing = () => {
      rings.push({
        x: Math.random() * w,
        y: Math.random() * h,
        rad: 0,
        max: 120 + Math.random() * 160,
        amber: Math.random() < 0.25,
      });
    };

    const drawReticle = (cx, cy, base) => {
      const a = t * 0.0008;
      ctx.save();
      ctx.translate(cx, cy);
      // outer rotating dashed arc
      ctx.strokeStyle = `rgba(${CYAN}, 0.10)`;
      ctx.lineWidth = 1;
      for (let seg = 0; seg < 3; seg++) {
        ctx.beginPath();
        const start = a + (seg * Math.PI * 2) / 3;
        ctx.arc(0, 0, base, start, start + Math.PI / 2.4);
        ctx.stroke();
      }
      // mid ring
      ctx.beginPath();
      ctx.strokeStyle = `rgba(${CYAN}, 0.07)`;
      ctx.arc(0, 0, base * 0.72, 0, Math.PI * 2);
      ctx.stroke();
      // ticks
      ctx.strokeStyle = `rgba(${CYAN}, 0.12)`;
      for (let i = 0; i < 60; i++) {
        const ang = -a * 1.6 + (i / 60) * Math.PI * 2;
        const inner = base * 0.86;
        const outer = base * (i % 5 === 0 ? 0.94 : 0.9);
        ctx.beginPath();
        ctx.moveTo(Math.cos(ang) * inner, Math.sin(ang) * inner);
        ctx.lineTo(Math.cos(ang) * outer, Math.sin(ang) * outer);
        ctx.stroke();
      }
      // inner counter-rotating arc
      ctx.beginPath();
      ctx.strokeStyle = `rgba(${AMBER}, 0.09)`;
      ctx.arc(0, 0, base * 0.5, -a * 2, -a * 2 + Math.PI, false);
      ctx.stroke();
      ctx.restore();
    };

    const draw = () => {
      t += 1;
      ctx.clearRect(0, 0, w, h);

      // rotating reticles (top-right + bottom-left, large & faint)
      drawReticle(w * 0.82, h * 0.28, Math.min(w, h) * 0.34);
      drawReticle(w * 0.12, h * 0.82, Math.min(w, h) * 0.22);

      // constellation connections
      for (let i = 0; i < nodes.length; i++) {
        const p = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
          const q = nodes[j];
          const dx = p.x - q.x, dy = p.y - q.y;
          const d2 = dx * dx + dy * dy;
          if (d2 < 15000) {
            const alpha = (1 - d2 / 15000) * 0.16;
            ctx.strokeStyle = `rgba(${CYAN}, ${alpha})`;
            ctx.lineWidth = 0.6;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.stroke();
          }
        }
      }

      // nodes + mouse reactivity
      for (const p of nodes) {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;

        const mdx = mouse.x - p.x, mdy = mouse.y - p.y;
        const md2 = mdx * mdx + mdy * mdy;
        if (md2 < 26000) {
          const f = (1 - md2 / 26000);
          p.x += (mdx / Math.sqrt(md2 + 1)) * f * 0.6;
          p.y += (mdy / Math.sqrt(md2 + 1)) * f * 0.6;
          // link to cursor
          ctx.strokeStyle = `rgba(${CYAN}, ${f * 0.28})`;
          ctx.lineWidth = 0.7;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.stroke();
        }

        const col = p.amber ? AMBER : CYAN;
        const glow = 0.5 + 0.5 * Math.sin((t + p.x) * 0.02);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${col}, ${0.45 + glow * 0.35})`;
        ctx.shadowBlur = 6;
        ctx.shadowColor = `rgba(${col}, 0.6)`;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // cursor node
      if (mouse.x > 0) {
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, 2.4, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${CYAN}, 0.9)`;
        ctx.fill();
      }

      // sonar pings
      for (let i = rings.length - 1; i >= 0; i--) {
        const r = rings[i];
        r.rad += 1.4;
        const prog = r.rad / r.max;
        const alpha = (1 - prog) * 0.4;
        const col = r.amber ? AMBER : CYAN;
        ctx.beginPath();
        ctx.strokeStyle = `rgba(${col}, ${alpha})`;
        ctx.lineWidth = 1.2;
        ctx.arc(r.x, r.y, r.rad, 0, Math.PI * 2);
        ctx.stroke();
        if (prog >= 1) rings.splice(i, 1);
      }
      if (t % 120 === 0) spawnRing();

      raf = requestAnimationFrame(draw);
    };

    const onMove = (e) => { mouse.x = e.clientX; mouse.y = e.clientY; };
    const onLeave = () => { mouse.x = -9999; mouse.y = -9999; };

    init();
    if (reduce) {
      // static frame for reduced-motion users
      for (const p of nodes) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${CYAN}, 0.5)`;
        ctx.fill();
      }
    } else {
      draw();
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseout", onLeave);
    }
    window.addEventListener("resize", init);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", init);
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseout", onLeave);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 z-0 pointer-events-none"
      style={{ opacity: 0.6 }}
      data-testid="hud-background"
    />
  );
}
