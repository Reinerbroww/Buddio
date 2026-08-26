"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import type { HighlightData, HighlightColor } from "@/lib/highlight-types";
import { HIGHLIGHT_COLORS } from "@/lib/highlight-types";
import HighlightPopup from "./HighlightPopup";
import HighlightCard from "./HighlightCard";

const MARK_ATTR = "data-highlight-id";
const COLOR_MAP: Record<HighlightColor, string> = {
  yellow: "rgba(253, 224, 71, 0.4)",
  green: "rgba(134, 239, 172, 0.4)",
  blue: "rgba(147, 197, 253, 0.4)",
  red: "rgba(252, 165, 165, 0.4)",
};

interface HighlightableContentProps {
  content: string;
  highlights: HighlightData[];
  onAdd: (text: string, color: HighlightColor, note: string) => void;
  onUpdateNote: (id: string, note: string) => void;
  onUpdateColor: (id: string, color: HighlightColor) => void;
  onRemove: (id: string) => void;
  className?: string;
}

export default function HighlightableContent({
  content,
  highlights,
  onAdd,
  onUpdateNote,
  onUpdateColor,
  onRemove,
  className = "",
}: HighlightableContentProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [popup, setPopup] = useState<{ x: number; y: number; text: string } | null>(null);
  const [card, setCard] = useState<{ highlight: HighlightData; x: number; y: number } | null>(null);

  const applyHighlights = useCallback(() => {
    const container = containerRef.current;
    if (!container) return;

    container.querySelectorAll(`[${MARK_ATTR}]`).forEach((el) => {
      const parent = el.parentNode;
      if (parent) {
        parent.replaceChild(document.createTextNode(el.textContent || ""), el);
        parent.normalize();
      }
    });

    if (highlights.length === 0) return;

    const sorted = [...highlights].sort((a, b) => b.text.length - a.text.length);

    for (const h of sorted) {
      const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
      let node: Text | null;
      while ((node = walker.nextNode() as Text | null)) {
        if (!node.textContent) continue;
        const idx = node.textContent.indexOf(h.text);
        if (idx === -1) continue;

        try {
          const range = document.createRange();
          range.setStart(node, idx);
          range.setEnd(node, idx + h.text.length);

          const mark = document.createElement("mark");
          mark.setAttribute(MARK_ATTR, h.id);
          mark.style.backgroundColor = COLOR_MAP[h.color];
          mark.style.borderRadius = "3px";
          mark.style.cursor = "pointer";
          mark.style.transition = "filter 0.15s";
          mark.style.padding = "1px 0";
          mark.style.borderBottom = `2px solid ${COLOR_MAP[h.color].replace("0.4", "0.8")}`;
          mark.title = h.note || HIGHLIGHT_COLORS[h.color].label;
          range.surroundContents(mark);
        } catch {
          continue;
        }
        break;
      }
    }

    container.querySelectorAll(`[${MARK_ATTR}]`).forEach((el) => {
      el.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        const id = el.getAttribute(MARK_ATTR);
        const h = highlights.find((x) => x.id === id);
        if (!h) return;
        const rect = (el as HTMLElement).getBoundingClientRect();
        setCard({
          highlight: h,
          x: Math.min(rect.left, window.innerWidth - 300),
          y: rect.bottom + 8,
        });
        setPopup(null);
      });
    });
  }, [highlights]);

  useEffect(() => {
    const t = setTimeout(applyHighlights, 50);
    return () => clearTimeout(t);
  }, [applyHighlights, content]);

  const handleMouseUp = useCallback(() => {
    setTimeout(() => {
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed || !sel.rangeCount) return;

      const range = sel.getRangeAt(0);
      const container = containerRef.current;
      if (!container || !container.contains(range.commonAncestorContainer)) return;

      const text = sel.toString().trim();
      if (text.length < 2) return;

      const rect = range.getBoundingClientRect();
      setCard(null);
      setPopup({
        x: Math.min(rect.left + rect.width / 2, window.innerWidth - 300),
        y: rect.top - 10,
        text,
      });
    }, 10);
  }, []);

  const handleHighlight = useCallback(
    (color: HighlightColor, note: string) => {
      if (!popup) return;
      onAdd(popup.text, color, note);
      window.getSelection()?.removeAllRanges();
      setPopup(null);
    },
    [popup, onAdd]
  );

  return (
    <div className={`relative ${className}`} onClick={() => { setPopup(null); setCard(null); }}>
      <div ref={containerRef} onMouseUp={handleMouseUp}>
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkMath]}
          rehypePlugins={[rehypeKatex]}
          components={{
            h2: (props) => (
              <h2 className="text-lg font-extrabold text-slate-900 mt-8 mb-3 first:mt-0" {...props} />
            ),
            h3: (props) => (
              <h3 className="text-base font-bold text-slate-800 mt-5 mb-2" {...props} />
            ),
            p: (props) => <p className="mb-3 last:mb-0 leading-relaxed text-sm text-slate-700" {...props} />,
            strong: (props) => <strong className="font-extrabold text-slate-900" {...props} />,
            em: (props) => <em className="italic text-slate-600" {...props} />,
            ul: (props) => <ul className="list-disc pl-5 mb-3 space-y-1.5" {...props} />,
            ol: (props) => <ol className="list-decimal pl-5 mb-3 space-y-1.5" {...props} />,
            li: (props) => <li className="text-sm leading-relaxed text-slate-700" {...props} />,
            blockquote: (props) => (
              <blockquote className="border-l-4 border-[#4F8EF7] pl-4 italic my-3 text-slate-600 bg-[#4F8EF7]/5 py-2 pr-3 rounded-r-lg" {...props} />
            ),
            hr: (props) => <hr className="my-5 border-slate-200/60" {...props} />,
            pre: (props) => (
              <pre className="block bg-slate-50 text-slate-800 p-4 rounded-xl text-xs font-mono border border-slate-100 overflow-x-auto my-3 max-w-full" {...props} />
            ),
            code: ({ className: cn, children, ...props }: any) => {
              const isBlock = cn?.includes("language-");
              return isBlock ? (
                <code className="font-mono text-xs" {...cn} {...props}>{children}</code>
              ) : (
                <code className="bg-slate-100 text-[#4F8EF7] px-1.5 py-0.5 rounded text-xs font-mono" {...props}>{children}</code>
              );
            },
            table: (props) => (
              <div className="overflow-x-auto my-3">
                <table className="min-w-full text-sm border border-slate-200 rounded-xl overflow-hidden" {...props} />
              </div>
            ),
            thead: (props) => <thead className="bg-slate-50" {...props} />,
            th: (props) => <th className="px-4 py-2 text-left text-xs font-bold text-slate-600 border-b border-slate-200" {...props} />,
            td: (props) => <td className="px-4 py-2 text-sm text-slate-700 border-b border-slate-100" {...props} />,
          }}
        >
          {content}
        </ReactMarkdown>
      </div>

      {popup && (
        <div className="fixed z-[60] animate-in fade-in zoom-in-95 duration-150" style={{ top: popup.y, left: popup.x }}>
          <HighlightPopup
            selectedText={popup.text}
            onHighlight={handleHighlight}
            onClose={() => setPopup(null)}
          />
        </div>
      )}

      {card && (
        <HighlightCard
          highlight={card.highlight}
          position={{ x: card.x, y: card.y }}
          onUpdateNote={onUpdateNote}
          onUpdateColor={onUpdateColor}
          onRemove={onRemove}
          onClose={() => setCard(null)}
        />
      )}
    </div>
  );
}
