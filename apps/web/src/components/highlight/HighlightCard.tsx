"use client";

import { useState } from "react";
import { Pencil, Trash2, X, Check } from "lucide-react";
import { HIGHLIGHT_COLORS, type HighlightData, type HighlightColor } from "@/lib/highlight-types";

interface HighlightCardProps {
  highlight: HighlightData;
  position: { x: number; y: number };
  onUpdateNote: (id: string, note: string) => void;
  onUpdateColor: (id: string, color: HighlightColor) => void;
  onRemove: (id: string) => void;
  onClose: () => void;
}

export default function HighlightCard({
  highlight,
  position,
  onUpdateNote,
  onUpdateColor,
  onRemove,
  onClose,
}: HighlightCardProps) {
  const [editing, setEditing] = useState(false);
  const [noteText, setNoteText] = useState(highlight.note);
  const cfg = HIGHLIGHT_COLORS[highlight.color];

  const handleSave = () => {
    onUpdateNote(highlight.id, noteText);
    setEditing(false);
  };

  return (
    <div
      className="fixed z-[60] animate-in fade-in zoom-in-95 duration-150"
      style={{ top: position.y, left: position.x }}
    >
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 p-4 w-72 space-y-3">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5">
            <span className="text-sm">{cfg.emoji}</span>
            <span className="text-[11px] font-bold text-slate-700">{cfg.label}</span>
          </div>
          <button onClick={onClose} className="p-0.5 rounded text-slate-300 hover:text-slate-500 transition-colors">
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        <p className="text-xs text-slate-500 leading-relaxed line-clamp-3 bg-slate-50 rounded-lg px-3 py-2 border border-slate-100">
          &quot;{highlight.text}&quot;
        </p>

        <div className="grid grid-cols-4 gap-1">
          {(Object.keys(HIGHLIGHT_COLORS) as HighlightColor[]).map((c) => {
            const cc = HIGHLIGHT_COLORS[c];
            return (
              <button
                key={c}
                onClick={() => onUpdateColor(highlight.id, c)}
                className={`flex items-center justify-center py-1.5 rounded-lg border transition-all text-xs ${
                  highlight.color === c
                    ? `${cc.bg} ${cc.border} shadow-sm`
                    : "border-transparent hover:bg-slate-50"
                }`}
                title={cc.label}
              >
                {cc.emoji}
              </button>
            );
          })}
        </div>

        {editing ? (
          <div className="space-y-2">
            <textarea
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              autoFocus
              rows={2}
              className="w-full resize-none text-xs text-slate-700 bg-slate-50 border border-slate-100 rounded-lg px-3 py-2 outline-none focus:border-[#4F8EF7] transition-colors"
            />
            <button
              onClick={handleSave}
              className="w-full flex items-center justify-center gap-1.5 py-1.5 text-[11px] font-semibold text-white bg-[#4F8EF7] rounded-lg hover:bg-[#3b76e6] transition-colors"
            >
              <Check className="w-3 h-3" />
              Simpan Catatan
            </button>
          </div>
        ) : highlight.note ? (
          <div className="space-y-2">
            <p className="text-xs text-slate-600 leading-relaxed bg-amber-50 border border-amber-100 rounded-lg px-3 py-2">
              {highlight.note}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setEditing(true)}
                className="flex-1 flex items-center justify-center gap-1 py-1.5 text-[11px] font-semibold text-[#4F8EF7] bg-[#4F8EF7]/8 hover:bg-[#4F8EF7]/15 rounded-lg transition-colors"
              >
                <Pencil className="w-3 h-3" />
                Edit
              </button>
              <button
                onClick={() => { onRemove(highlight.id); onClose(); }}
                className="flex-1 flex items-center justify-center gap-1 py-1.5 text-[11px] font-semibold text-rose-500 bg-rose-50 hover:bg-rose-100 rounded-lg transition-colors"
              >
                <Trash2 className="w-3 h-3" />
                Hapus
              </button>
            </div>
          </div>
        ) : (
          <div className="flex gap-2">
            <button
              onClick={() => setEditing(true)}
              className="flex-1 flex items-center justify-center gap-1 py-1.5 text-[11px] font-semibold text-[#4F8EF7] bg-[#4F8EF7]/8 hover:bg-[#4F8EF7]/15 rounded-lg transition-colors"
            >
              <Pencil className="w-3 h-3" />
              + Tambah Catatan
            </button>
            <button
              onClick={() => { onRemove(highlight.id); onClose(); }}
              className="flex items-center justify-center gap-1 py-1.5 px-3 text-[11px] font-semibold text-rose-500 bg-rose-50 hover:bg-rose-100 rounded-lg transition-colors"
            >
              <Trash2 className="w-3 h-3" />
            </button>
          </div>
        )}

        <p className="text-[9px] text-slate-300 text-center">
          {new Date(highlight.createdAt).toLocaleDateString("id-ID", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" })}
        </p>
      </div>
    </div>
  );
}
