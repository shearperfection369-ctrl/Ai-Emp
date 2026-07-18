import { useState, useRef, useEffect } from "react";
import { Bot, Send, X, Sparkles } from "lucide-react";
import { API_BASE } from "../lib/api";

const SUGGESTIONS = [
  "I run a marketing agency, what do you recommend?",
  "Best tool for a solo developer?",
  "I need help hiring faster",
];

export default function AriaAssistant() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [sessionId] = useState(() => `web_${Math.random().toString(36).slice(2, 12)}`);
  const [messages, setMessages] = useState([
    { role: "assistant", content: "ARIA online. I'm your AI concierge — tell me what you're trying to accomplish and I'll deploy the perfect tool from the Emporium arsenal." },
  ]);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, open]);

  const send = async (text) => {
    const msg = (text ?? input).trim();
    if (!msg || busy) return;
    setInput("");
    setBusy(true);
    setMessages((m) => [...m, { role: "user", content: msg }, { role: "assistant", content: "" }]);
    try {
      const resp = await fetch(`${API_BASE}/assistant/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ session_id: sessionId, message: msg }),
      });
      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        setMessages((m) => {
          const copy = [...m];
          copy[copy.length - 1] = { role: "assistant", content: copy[copy.length - 1].content + chunk };
          return copy;
        });
      }
    } catch {
      setMessages((m) => {
        const copy = [...m];
        copy[copy.length - 1] = { role: "assistant", content: "Signal lost. Please try again." };
        return copy;
      });
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <button
        onClick={() => setOpen((o) => !o)}
        data-testid="aria-toggle"
        className="fixed bottom-6 right-6 z-[60] w-16 h-16 rounded-full bg-[#00f0ff]/15 border border-[#00f0ff]/50 backdrop-blur-md flex items-center justify-center glow-cyan-strong animate-pulse-ring hover:scale-105 transition-transform"
        aria-label="Open ARIA assistant"
      >
        {open ? <X className="w-6 h-6 text-[#00f0ff]" /> : <Bot className="w-7 h-7 text-[#00f0ff]" />}
      </button>

      {open && (
        <div className="fixed bottom-24 right-6 z-[60] w-[calc(100vw-3rem)] sm:w-[400px] h-[560px] max-h-[75vh] glass-strong clip-hud flex flex-col overflow-hidden animate-hud-in" data-testid="aria-panel">
          <div className="px-4 py-3 border-b border-[#00f0ff]/20 flex items-center gap-3 scanlines">
            <div className="w-9 h-9 rounded-full bg-[#00f0ff]/15 border border-[#00f0ff]/50 flex items-center justify-center">
              <Sparkles className="w-4.5 h-4.5 text-[#00f0ff]" />
            </div>
            <div>
              <div className="font-orbit font-bold text-sm tracking-widest text-white">ARIA</div>
              <div className="font-code text-[10px] text-[#00f0ff] flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00f0ff] animate-blink" /> AI CONCIERGE ONLINE
              </div>
            </div>
          </div>

          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`} data-testid={`aria-msg-${m.role}`}>
                <div className={`max-w-[85%] px-3.5 py-2.5 clip-hud-sm font-code text-sm leading-relaxed whitespace-pre-wrap ${
                  m.role === "user" ? "bg-[#00f0ff] text-black" : "bg-[#0a1118] border border-[#00f0ff]/25 text-[#e6f6ff]"
                }`}>
                  {m.content || (busy && i === messages.length - 1 ? <span className="animate-blink">▊</span> : "")}
                </div>
              </div>
            ))}
            {messages.length <= 1 && (
              <div className="space-y-2 pt-2">
                {SUGGESTIONS.map((s) => (
                  <button key={s} onClick={() => send(s)} data-testid="aria-suggestion"
                    className="block w-full text-left px-3 py-2 clip-hud-sm bg-[#00f0ff]/5 border border-[#00f0ff]/20 text-[#8b9bb4] font-code text-xs hover:border-[#00f0ff]/50 hover:text-white transition-colors">
                    {s}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="p-3 border-t border-[#00f0ff]/20 flex items-center gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Ask ARIA anything…"
              data-testid="aria-input"
              className="flex-1 bg-transparent border-b border-[#00f0ff]/30 focus:border-[#00f0ff] outline-none font-code text-sm text-white px-1 py-2 placeholder:text-[#8b9bb4]/60"
            />
            <button onClick={() => send()} disabled={busy} data-testid="aria-send"
              className="w-10 h-10 clip-hud-sm bg-[#00f0ff] text-black flex items-center justify-center hover:glow-cyan-strong transition-shadow disabled:opacity-50">
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
