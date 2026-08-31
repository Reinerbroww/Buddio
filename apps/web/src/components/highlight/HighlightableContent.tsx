"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { marked, type Tokens } from "marked";
import katex from "katex";
import "katex/dist/katex.min.css";

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
  coba:      { bg: "bg-violet-50",  border: "border-violet-400",  icon: "✏️", label: "Coba Sendiri" },
  hubung:    { bg: "bg-cyan-50",    border: "border-cyan-400",    icon: "🔗", label: "Hubungan Antar Konsep" },
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
    <div class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed space-y-1">${marked.parse(body) as string}</div>
  </div>`;
}

class MateriRenderer extends marked.Renderer {
  heading({ tokens, depth }: Tokens.Heading): string {
    const text = tokens.map(tokenText).join("");
    const tag = `h${depth}`;
    if (depth === 2) {
      return `<${tag} class="materi-h2 text-lg font-extrabold text-slate-900 dark:text-slate-100 mt-10 mb-4 first:mt-0 flex items-center gap-2">${text}</${tag}>`;
    }
    if (depth === 3) {
      return `<${tag} class="materi-h3 text-base font-bold text-slate-800 dark:text-slate-200 mt-6 mb-3 flex items-center gap-1.5">${text}</${tag}>`;
    }
    return `<${tag} class="text-sm font-bold text-slate-700 dark:text-slate-300 mt-4 mb-2">${text}</${tag}>`;
  }

  paragraph({ tokens }: Tokens.Paragraph): string {
    const text = tokens.map(tokenText).join("");
    if (text.startsWith("<div class=")) return text;
    return `<p class="mb-3 last:mb-0 leading-relaxed text-sm text-slate-700 dark:text-slate-300">${text}</p>`;
  }

  blockquote({ tokens }: Tokens.Blockquote): string {
    const raw = typeof tokens === "string" ? tokens : (tokens as unknown as Array<unknown>).map(tokenText).join("\n");
    const callout = parseCallout(raw);
    if (callout) return renderCalloutHTML(callout.type, callout.body);
    return `<blockquote class="border-l-4 border-[#4F8EF7] pl-4 italic my-4 text-slate-600 dark:text-slate-400 bg-[#4F8EF7]/5 dark:bg-[#60a5fa]/10 py-3 pr-4 rounded-r-xl text-sm">${raw}</blockquote>`;
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
        return `<li class="flex items-start gap-2.5 text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
          <span class="mt-0.5 w-5 h-5 rounded-md border-2 ${checked ? "bg-teal-500 border-teal-500 text-white flex items-center justify-center text-[10px]" : "border-slate-300 dark:border-slate-600 bg-white dark:bg-[#1e293b]"} shrink-0 flex items-center justify-center font-bold text-[10px]">${checked ? "✓" : ""}</span>
          <span>${content}</span>
        </li>`;
      }
      return `<li class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">${itemText}</li>`;
    }).join("\n");
    return `<${tag} class="${cls}">${body}</${tag}>`;
  }

  strong({ tokens }: Tokens.Strong): string {
    const text = tokens.map(tokenText).join("");
    return `<strong class="font-extrabold text-slate-900 dark:text-slate-50">${text}</strong>`;
  }

  em({ tokens }: Tokens.Em): string {
    const text = tokens.map(tokenText).join("");
    return `<em class="italic text-slate-600 dark:text-slate-400">${text}</em>`;
  }

  hr(): string {
    return `<hr class="my-8 border-0 h-px bg-gradient-to-r from-transparent via-slate-200 dark:via-slate-700 to-transparent" />`;
  }

  codespan({ text }: { text: string }): string {
    return `<code class="bg-slate-100 dark:bg-[#1e293b] text-[#4F8EF7] dark:text-[#93bbfd] px-1.5 py-0.5 rounded text-xs font-mono">${text}</code>`;
  }

  code({ text, lang }: { text: string; lang?: string }): string {
    const langLabel = lang ? `<div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">${lang}</div>` : "";
    return `<div class="materi-code block bg-slate-900 dark:bg-[#0c1222] text-slate-100 p-4 rounded-xl text-xs font-mono overflow-x-auto my-4 max-w-full border border-slate-800 dark:border-[#1e293b]">${langLabel}<pre class="m-0 p-0 bg-transparent">${text}</pre></div>`;
  }

  table(token: Tokens.Table): string {
    const head = token.header.map((h: Tokens.TableCell) => {
      const text = h.tokens.map(tokenText).join("");
      return `<th class="px-4 py-2.5 text-left text-xs font-bold text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-[#1e293b] border-b border-slate-200 dark:border-[#334155]">${text}</th>`;
    }).join("");
    const body = token.rows.map((row: Tokens.TableCell[]) => {
      const cells = row.map((c: Tokens.TableCell) => {
        const text = c.tokens.map(tokenText).join("");
        return `<td class="px-4 py-2.5 text-sm text-slate-700 dark:text-slate-300 border-b border-slate-100 dark:border-[#1e293b]">${text}</td>`;
      }).join("");
      return `<tr class="hover:bg-slate-50/50 dark:hover:bg-[#1e293b]/50 transition-colors">${cells}</tr>`;
    }).join("");
    return `<div class="overflow-x-auto my-4"><table class="min-w-full text-sm border border-slate-200 dark:border-[#334155] rounded-xl overflow-hidden"><thead>${head}</thead><tbody>${body}</tbody></table></div>`;
  }

  image({ href, title, text }: Tokens.Image): string {
    return `<figure class="my-4"><img src="${href}" alt="${text}" class="rounded-xl w-full border border-slate-100 dark:border-[#334155]" />${title ? `<figcaption class="text-xs text-slate-400 dark:text-slate-500 text-center mt-2">${title}</figcaption>` : ""}</figure>`;
  }

  link({ href, title, tokens }: Tokens.Link): string {
    const text = tokens.map(tokenText).join("");
    return `<a href="${href}"${title ? ` title="${title}"` : ""} target="_blank" rel="noopener noreferrer" class="text-[#4F8EF7] dark:text-[#60a5fa] font-semibold hover:underline">${text}</a>`;
  }
}

marked.setOptions({
  gfm: true,
  breaks: true,
  renderer: new MateriRenderer(),
});

// --- Math (LaTeX via KaTeX) ---

type MathItem = { latex: string; display: boolean };

/** $...$ / $$...$$ LaTeX math is extracted and hidden behind opaque tokens so the
 *  markdown parser and text cleaners never mangle backslashes, underscores or carets
 *  inside formulas. Restored later with KaTeX. */
function protectMath(md: string): { text: string; math: MathItem[] } {
  const math: MathItem[] = [];
  const text = md.replace(
    /\$\$([\s\S]+?)\$\$|\$([^\n$]+?)\$/g,
    (full, displayLatex: string | undefined, inlineLatex: string | undefined) => {
      if (displayLatex !== undefined) {
        math.push({ latex: displayLatex.trim(), display: true });
      } else {
        math.push({ latex: (inlineLatex ?? "").trim(), display: false });
      }
      return `\u0000MATH${math.length - 1}\u0000`;
    }
  );
  return { text, math };
}

function renderMath(latex: string, display: boolean): string {
  try {
    const html = katex.renderToString(latex, { displayMode: display, throwOnError: false });
    return display
      ? `<div class="materi-math-block">${html}</div>`
      : `<span class="materi-math-inline">${html}</span>`;
  } catch {
    return display ? `<div class="materi-math-block"></div>` : "";
  }
}

function restoreMath(html: string, math: MathItem[]): string {
  return html.replace(/\u0000MATH(\d+)\u0000/g, (_m, idx: string) => {
    const item = math[Number(idx)];
    return item ? renderMath(item.latex, item.display) : "";
  });
}

function cleanMarkdown(md: string): string {
  let out = md;
  // Drop unusable diagram code fences (mermaid/svg) and raw <svg> blocks entirely.
  out = out.replace(/```(?:mermaid|svg)\b[\s\S]*?```/gi, "");
  out = out.replace(/<svg[\s\S]*?<\/svg>/gi, "");
  // Unescape stray backslashes before common markdown punctuation (fixes \* \** \[ \] \# \_ \>
  // that some generators emit, which otherwise render as literal characters to the student).
  out = out.replace(/\\([*_#>\\|[\]{}~!^$+-.])/g, "$1");
  out = out.replace(/\\\[/g, "[").replace(/\\\]/g, "]");
  // Collapse empty emphasis markers left behind.
  out = out.replace(/\*\*\s*\*\*/g, "").replace(/\*\s*\*/g, "");
  // Convert any callout syntax whose type isn't supported into a plain blockquote so raw
  // "> [!note]" text never leaks. Supported types are rendered by the blockquote renderer.
  out = out.replace(
    /^(\s*)>\s*\[!([a-zA-Z0-9_]+)\]\s*(.*)$/gm,
    (_m, indent, type: string, rest) => {
      if (CALLOUT_TYPES[type.toLowerCase()]) return _m;
      const body = rest ? ` ${rest}` : "";
      return `${indent}> ${body}`;
    }
  );
  // Remove [ ! ... ] callout tokens that appear arbitrarily mid-text but not as blockquote.
  out = out.replace(/\[![a-zA-Z0-9_-]+\]/g, "");
  return out;
}

/** Strip stray characters from plain rendered text so students never see raw Markdown. */
function cleanText(text: string): string {
  // Stray artifacts in plain (non-code) rendered text: backslashes, emphasis markers,
  // and callout tokens. Underscores are preserved (they appear in identifiers).
  let s = text.replace(/\\/g, "");
  // Collapse double+ asterisks (bold artifacts), then drop any asterisk that is not
  // multiplication (so "2*3" survives but "*text*" / "a * b" stars are removed).
  s = s.replace(/\*{2,}/g, "");
  s = s.replace(/(^|[^\s*])\*(?!\S)/g, "$1").replace(/(^|\s)\*+(?=\s|$)/g, (_m) => _m.replace(/\*/g, " "));
  s = s.replace(/\[!([a-z0-9_-]+)\]/gi, " ").replace(/ {2,}/g, " ").trim();
  return s;
}

/** Remove disallowed raw HTML and stray Markdown artifacts, preserving code blocks. */
function sanitizeHtml(html: string): string {
  const protectedBlocks: string[] = [];
  let out = html
    // Protect code so we never strip '*' etc. inside code blocks / inline code.
    .replace(/<pre>[\s\S]*?<\/pre>/gi, (m) => {
      protectedBlocks.push(m);
      return `\u0000${protectedBlocks.length - 1}\u0000`;
    })
    .replace(/<code[^>]*>[\s\S]*?<\/code>/gi, (m) => {
      protectedBlocks.push(m);
      return `\u0000${protectedBlocks.length - 1}\u0000`;
    });
  // Remove raw HTML that must never render.
  out = out
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<svg[\s\S]*?<\/svg>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<iframe[\s\S]*?<\/iframe>/gi, "")
    .replace(/<object[\s\S]*?<\/object>/gi, "")
    .replace(/<embed[\s\S]*?>/gi, "")
    .replace(/\son\w+="[^"]*"/gi, "")
    .replace(/\son\w+='[^']*'/gi, "")
    .replace(/(href|src)\s*=\s*"javascript:[^"]*"/gi, "")
    .replace(/(href|src)\s*=\s*'javascript:[^']*'/gi, "");
  // Clean stray Markdown artifacts in non-code text (code was protected above).
  // Walk text segments (between tags) so we keep the surrounding tags intact.
  out = out.replace(/>([^<>]*)</g, (_m, text: string) => `>${cleanText(text)}<`);
  // Restore protected code blocks.
  out = out.replace(/\u0000(\d+)\u0000/g, (_m, idx: string) => protectedBlocks[Number(idx)] || "");
  return out;
}

function mdToHtml(md: string): string {
  const { text, math } = protectMath(md);
  const parsed = sanitizeHtml(marked.parse(cleanMarkdown(text)) as string);
  return restoreMath(parsed, math);
}

interface HighlightableContentProps {
  content: string;
  highlights: HighlightData[];
  onAdd: (text: string, color: HighlightColor, note: string) => void;
  onUpdateNote: (id: string, note: string) => void;
  onUpdateColor: (id: string, color: HighlightColor) => void;
  onRemove: (id: string) => void;
  onAskHighlight?: (text: string, demand: string) => void;
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
  onAskHighlight,
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
  }, [applyHighlights, html]);

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
            onAsk={onAskHighlight}
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
