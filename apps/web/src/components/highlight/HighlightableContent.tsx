"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { marked } from "marked";
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

marked.setOptions({ gfm: true, breaks: true });

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
      if ((el as any)._bindt) return;
      (el as any)._bindt = true;
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
        className={enabled ? "cursor-crosshair" : ""}
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
