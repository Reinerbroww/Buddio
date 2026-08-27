"use client";

import { useState } from "react";
import { StickyNote, X } from "lucide-react";
import { HIGHLIGHT_COLORS, type HighlightColor } from "@/lib/highlight-types";

interface HighlightPopupProps {
  selectedText: string;
  onHighlight: (color: HighlightColor, note: string) => void;
  onClose: () => void;
}

export default function HighlightPopup({ selectedText, onHighlight, onClose }: HighlightPopupProps) {
  const [note, setNote] = useState("");
  const [showNote, setShowNote] = useState(false);

  const truncated = selectedText.length > 80 ? selectedText.slice(0, 80) + "..." : selectedText;

  return (
    <div className="fixed z-[60] animate-in fade-in zoom-in-95 duration-150" style={{ top: "var(--popup-y, 50%)", left: "var(--popup-x, 50%)", transform: "translate(-50%, 8px)" }}>
      <div className="bg-white dark:bg-[#1e293b] rounded-2xl shadow-2xl border border-slate-200 dark:border-[#334155] p-4 w-72 space-y-3">
        <div className="flex items-start justify-between gap-2">
          <p className="text-[10px] text-slate-400 dark:text-slate-500 leading-relaxed line-clamp-2 flex-1">&quot;{truncated}&quot;</p>
          <button onClick={onClose} className="p-0.5 rounded text-slate-300 dark:text-slate-500 hover:text-slate-500 dark:hover:text-slate-300 transition-colors shrink-0">
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-4 gap-1.5">
          {(Object.keys(HIGHLIGHT_COLORS) as HighlightColor[]).map((c) => {
            const cfg = HIGHLIGHT_COLORS[c];
            return (
              <button
                key={c}
                onClick={() => onHighlight(c, note)}
                className={`flex flex-col items-center gap-1 py-2 rounded-xl border-2 transition-all duration-150 hover:scale-105 ${cfg.bg} ${cfg.border} hover:shadow-md cursor-pointer`}
              >
                <span className="text-base">{cfg.emoji}</span>
                <span className="text-[9px] font-bold text-slate-600 dark:text-slate-300 leading-tight">{cfg.label}</span>
              </button>
            );
          })}
        </div>

        {!showNote ? (
          <button
            onClick={() => setShowNote(true)}
            className="w-full flex items-center justify-center gap-1.5 py-2 text-[11px] font-semibold text-[#4F8EF7] bg-[#4F8EF7]/8 hover:bg-[#4F8EF7]/15 rounded-xl transition-colors"
          >
            <StickyNote className="w-3 h-3" />
            + Tambah Catatan
          </button>
        ) : (
          <div className="space-y-2">
            <textarea
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="Tulis catatanmu..."
              autoFocus
              rows={2}
              className="w-full resize-none text-xs text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] rounded-lg px-3 py-2 outline-none focus:border-[#4F8EF7] transition-colors placeholder-slate-400 dark:placeholder-slate-500"
            />
            <p className="text-[9px] text-slate-400 dark:text-slate-500 text-center">Pilih warna di atas, catatan akan ikut tersimpan.</p>
          </div>
        )}
      </div>
    </div>
  );
}
