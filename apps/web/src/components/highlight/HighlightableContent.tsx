"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { marked, type Tokens } from "marked";

type TokenText = { text: string };

function tokenText(token: unknown): string {
  if (token && typeof token === "object" && "text" in token) return (token as TokenText).text;
  return "";
}
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

const CALLOUT_TYPES: Record<string, { bg: string; border: string; icon: string; label: string }> = {
  tip:       { bg: "bg-blue-50",    border: "border-blue-400",    icon: "💡", label: "Tips" },
  funfact:   { bg: "bg-purple-50",  border: "border-purple-400",  icon: "✨", label: "Fakta Unik" },
  ingat:     { bg: "bg-amber-50",   border: "border-amber-400",   icon: "🧠", label: "Wajib Diingat" },
  contoh:    { bg: "bg-emerald-50", border: "border-emerald-400", icon: "📝", label: "Contoh" },
  perhatian: { bg: "bg-rose-50",    border: "border-rose-400",    icon: "⚠️", label: "Perhatian" },
  quiz:      { bg: "bg-indigo-50",  border: "border-indigo-400",  icon: "🎯", label: "Quiz" },
  tujuan:    { bg: "bg-teal-50",    border: "border-teal-400",    icon: "🎯", label: "Tujuan Pembelajaran" },
  prasyarat: { bg: "bg-slate-50",   border: "border-slate-400",   icon: "📋", label: "Prasyarat" },
};

function parseCallout(text: string): { type: string; body: string } | null {
  const m = text.match(/^\s*>\s*\[!(\w+)\]\s*\n?([\s\S]*)/);
  if (!m) return null;
  const type = m[1].toLowerCase();
  if (!CALLOUT_TYPES[type]) return null;
  const body = m[2]
    .split("\n")
    .map((l) => l.replace(/^\s*>\s?/, ""))
    .join("\n")
    .trim();
  return { type, body };
}

function renderCalloutHTML(type: string, body: string): string {
  const cfg = CALLOUT_TYPES[type];
  return `<div class="materi-callout ${cfg.bg} border-l-4 ${cfg.border} rounded-r-xl px-5 py-4 my-5">
    <div class="flex items-center gap-2 mb-2">
      <span class="text-lg">${cfg.icon}</span>
      <span class="text-xs font-extrabold uppercase tracking-wider text-slate-600">${cfg.label}</span>
    </div>
    <div class="text-sm text-slate-700 leading-relaxed space-y-1">${marked.parse(body) as string}</div>
  </div>`;
}

class MateriRenderer extends marked.Renderer {
  heading({ tokens, depth }: Tokens.Heading): string {
    const text = tokens.map(tokenText).join("");
    const tag = `h${depth}`;
    if (depth === 2) {
      return `<${tag} class="materi-h2 text-lg font-extrabold text-slate-900 mt-10 mb-4 first:mt-0 flex items-center gap-2">${text}</${tag}>`;
    }
    if (depth === 3) {
      return `<${tag} class="materi-h3 text-base font-bold text-slate-800 mt-6 mb-3 flex items-center gap-1.5">${text}</${tag}>`;
    }
    return `<${tag} class="text-sm font-bold text-slate-700 mt-4 mb-2">${text}</${tag}>`;
  }

  paragraph({ tokens }: Tokens.Paragraph): string {
    const text = tokens.map(tokenText).join("");
    if (text.startsWith("<div class=")) return text;
    return `<p class="mb-3 last:mb-0 leading-relaxed text-sm text-slate-700">${text}</p>`;
  }

  blockquote({ tokens }: Tokens.Blockquote): string {
    const raw = typeof tokens === "string" ? tokens : (tokens as unknown as Array<unknown>).map(tokenText).join("\n");
    const callout = parseCallout(raw);
    if (callout) return renderCalloutHTML(callout.type, callout.body);
    return `<blockquote class="border-l-4 border-[#4F8EF7] pl-4 italic my-4 text-slate-600 bg-[#4F8EF7]/5 py-3 pr-4 rounded-r-xl text-sm">${raw}</blockquote>`;
  }

  list(token: Tokens.List): string {
    const { items, ordered } = token;
    const tag = ordered ? "ol" : "ul";
    const cls = ordered
      ? "list-decimal pl-6 mb-4 space-y-2"
      : "list-disc pl-6 mb-4 space-y-2";
    const body = items.map((item: Tokens.ListItem) => {
      const itemText = item.tokens.map(tokenText).join("");
      const taskCheckbox = itemText.match(/^\[([ x])\]\s*/);
      if (taskCheckbox) {
        const checked = taskCheckbox[1] === "x";
        const content = itemText.replace(/^\[[ x]\]\s*/, "");
        return `<li class="flex items-start gap-2.5 text-sm text-slate-700 leading-relaxed">
          <span class="mt-0.5 w-5 h-5 rounded-md border-2 ${checked ? "bg-teal-500 border-teal-500 text-white flex items-center justify-center text-[10px]" : "border-slate-300 bg-white"} shrink-0 flex items-center justify-center font-bold text-[10px]">${checked ? "✓" : ""}</span>
          <span>${content}</span>
        </li>`;
      }
      return `<li class="text-sm text-slate-700 leading-relaxed">${itemText}</li>`;
    }).join("\n");
    return `<${tag} class="${cls}">${body}</${tag}>`;
  }

  strong({ tokens }: Tokens.Strong): string {
    const text = tokens.map(tokenText).join("");
    return `<strong class="font-extrabold text-slate-900">${text}</strong>`;
  }

  em({ tokens }: Tokens.Em): string {
    const text = tokens.map(tokenText).join("");
    return `<em class="italic text-slate-600">${text}</em>`;
  }

  hr(): string {
    return `<hr class="my-8 border-0 h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent" />`;
  }

  codespan({ text }: { text: string }): string {
    return `<code class="bg-slate-100 text-[#4F8EF7] px-1.5 py-0.5 rounded text-xs font-mono">${text}</code>`;
  }

  code({ text, lang }: { text: string; lang?: string }): string {
    const langLabel = lang ? `<div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">${lang}</div>` : "";
    return `<div class="materi-code block bg-slate-900 text-slate-100 p-4 rounded-xl text-xs font-mono overflow-x-auto my-4 max-w-full border border-slate-800">${langLabel}<pre class="m-0 p-0 bg-transparent">${text}</pre></div>`;
  }

  table(token: Tokens.Table): string {
    const head = token.header.map((h: Tokens.TableCell) => {
      const text = h.tokens.map(tokenText).join("");
      return `<th class="px-4 py-2.5 text-left text-xs font-bold text-slate-600 bg-slate-50 border-b border-slate-200">${text}</th>`;
    }).join("");
    const body = token.rows.map((row: Tokens.TableCell[]) => {
      const cells = row.map((c: Tokens.TableCell) => {
        const text = c.tokens.map(tokenText).join("");
        return `<td class="px-4 py-2.5 text-sm text-slate-700 border-b border-slate-100">${text}</td>`;
      }).join("");
      return `<tr class="hover:bg-slate-50/50 transition-colors">${cells}</tr>`;
    }).join("");
    return `<div class="overflow-x-auto my-4"><table class="min-w-full text-sm border border-slate-200 rounded-xl overflow-hidden"><thead>${head}</thead><tbody>${body}</tbody></table></div>`;
  }

  image({ href, title, text }: Tokens.Image): string {
    return `<figure class="my-4"><img src="${href}" alt="${text}" class="rounded-xl w-full border border-slate-100" />${title ? `<figcaption class="text-xs text-slate-400 text-center mt-2">${title}</figcaption>` : ""}</figure>`;
  }

  link({ href, title, tokens }: Tokens.Link): string {
    const text = tokens.map(tokenText).join("");
    return `<a href="${href}"${title ? ` title="${title}"` : ""} target="_blank" rel="noopener noreferrer" class="text-[#4F8EF7] font-semibold hover:underline">${text}</a>`;
  }
}

marked.setOptions({
  gfm: true,
  breaks: true,
  renderer: new MateriRenderer(),
});

function mdToHtml(md: string): string {
  return marked.parse(md) as string;
}

interface HighlightableContentProps {
  content: string;
  highlights: HighlightData[];
  onAdd: (text: string, color: HighlightColor, note: string) => void;
  onUpdateNote: (id: string, note: string) => void;
  onUpdateColor: (id: string, color: HighlightColor) => void;
  onRemove: (id: string) => void;
  className?: string;
  enabled?: boolean;
}

function getMarkRect(markEl: HTMLElement): { x: number; y: number } {
  const r = markEl.getBoundingClientRect();
  return {
    x: Math.min(r.left, window.innerWidth - 300),
    y: r.bottom + 8,
  };
}

export default function HighlightableContent({
  content,
  highlights,
  onAdd,
  onUpdateNote,
  onUpdateColor,
  onRemove,
  className = "",
  enabled = true,
}: HighlightableContentProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [popup, setPopup] = useState<{ x: number; y: number; text: string } | null>(null);
  const [activeHighlightId, setActiveHighlightId] = useState<string | null>(null);
  const [cardPos, setCardPos] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const posRafRef = useRef<number>(0);

  const html = useMemo(() => mdToHtml(content), [content]);

  const activeHighlight = useMemo(
    () => (activeHighlightId ? highlights.find((h) => h.id === activeHighlightId) ?? null : null),
    [activeHighlightId, highlights]
  );

  const recalcCardPos = useCallback(() => {
    if (!activeHighlightId) return;
    const markEl = containerRef.current?.querySelector(`[${MARK_ATTR}="${activeHighlightId}"]`) as HTMLElement | null;
    if (!markEl) return;
    setCardPos(getMarkRect(markEl));
  }, [activeHighlightId]);

  useEffect(() => {
    if (!activeHighlightId) return;
    recalcCardPos();
    const onScroll = () => {
      cancelAnimationFrame(posRafRef.current);
      posRafRef.current = requestAnimationFrame(recalcCardPos);
    };
    window.addEventListener("scroll", onScroll, true);
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll, true);
      window.removeEventListener("resize", onScroll);
      cancelAnimationFrame(posRafRef.current);
    };
  }, [activeHighlightId, recalcCardPos]);

  const applyHighlights = useCallback(() => {
    const container = containerRef.current;
    if (!container) return;

    const currentIds = new Set(highlights.map((h) => h.id));

    container.querySelectorAll(`[${MARK_ATTR}]`).forEach((el) => {
      const id = el.getAttribute(MARK_ATTR);
      if (!id || !currentIds.has(id)) {
        const parent = el.parentNode;
        if (parent) {
          parent.replaceChild(document.createTextNode(el.textContent || ""), el);
          parent.normalize();
        }
      }
    });

    if (highlights.length === 0) return;

    const sorted = [...highlights].sort((a, b) => b.text.length - a.text.length);

    for (const h of sorted) {
      if (container.querySelector(`[${MARK_ATTR}="${h.id}"]`)) continue;

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
          mark.style.transition = "filter 0.15s, outline 0.15s";
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
      const marker = el as HTMLElement & { _bindt?: boolean };
      if (marker._bindt) return;
      marker._bindt = true;
      el.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        const id = el.getAttribute(MARK_ATTR);
        if (!id) return;
        setActiveHighlightId(id);
        setCardPos(getMarkRect(el as HTMLElement));
        setPopup(null);
      });
    });
  }, [highlights]);

  useEffect(() => {
    applyHighlights();
  }, [applyHighlights]);

  const handleMouseUp = useCallback(() => {
    if (!enabled) return;
    setTimeout(() => {
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed || !sel.rangeCount) return;

      const range = sel.getRangeAt(0);
      const container = containerRef.current;
      if (!container || !container.contains(range.commonAncestorContainer)) return;

      const text = sel.toString().trim();
      if (text.length < 2) return;

      const rect = range.getBoundingClientRect();
      setActiveHighlightId(null);
      setPopup({
        x: Math.min(rect.left + rect.width / 2, window.innerWidth - 300),
        y: rect.top - 10,
        text,
      });
    }, 10);
  }, [enabled]);

  const handleHighlight = useCallback(
    (color: HighlightColor, note: string) => {
      if (!popup) return;
      onAdd(popup.text, color, note);
      window.getSelection()?.removeAllRanges();
      setPopup(null);
    },
    [popup, onAdd]
  );

  const closeAll = useCallback(() => {
    setPopup(null);
    setActiveHighlightId(null);
  }, []);

  return (
    <div className={`relative ${className}`} onClick={closeAll}>
      <div
        ref={containerRef}
        onMouseUp={handleMouseUp}
        className={`materi-content ${enabled ? "cursor-crosshair" : ""}`}
        dangerouslySetInnerHTML={{ __html: html }}
        style={{ lineHeight: "1.8" }}
      />

      {popup && (
        <div
          className="fixed z-[60] animate-in fade-in zoom-in-95 duration-150"
          style={{ top: popup.y, left: popup.x }}
          onMouseUp={(e) => e.stopPropagation()}
          onClick={(e) => e.stopPropagation()}
        >
          <HighlightPopup
            selectedText={popup.text}
            onHighlight={handleHighlight}
            onClose={() => setPopup(null)}
          />
        </div>
      )}

      {activeHighlight && (
        <div
          className="fixed z-[60] animate-in fade-in zoom-in-95 duration-150"
          style={{ top: cardPos.y, left: cardPos.x }}
          onMouseUp={(e) => e.stopPropagation()}
          onClick={(e) => e.stopPropagation()}
        >
          <HighlightCard
            highlight={activeHighlight}
            onUpdateNote={onUpdateNote}
            onUpdateColor={onUpdateColor}
            onRemove={onRemove}
            onClose={() => setActiveHighlightId(null)}
          />
        </div>
      )}
    </div>
  );
}
