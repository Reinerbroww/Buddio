"use client";

import React, { Suspense, useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  ArrowLeft,
  Loader2,
  BookOpen,
  Video,
  MessageCircle,
  Sparkles,
  CheckCircle2,
  Play,
  ExternalLink,
  RefreshCw,
  Maximize2,
  Minimize2,
  StickyNote,
  Highlighter,
  Save,
} from "lucide-react";
import api, { ApiError } from "@/services/api";
import type { Lesson } from "@/lib/types";
import { useHighlights } from "@/hooks/useHighlights";
import { HIGHLIGHT_COLORS } from "@/lib/highlight-types";
import { useLanguage } from "@/context/LanguageContext";
import HighlightableContent from "@/components/highlight/HighlightableContent";

function extractYouTubeId(url: string): string | null {
  const patterns = [
    /youtube\.com\/watch\?v=([^&]+)/,
    /youtu\.be\/([^?]+)/,
    /youtube\.com\/embed\/([^?]+)/,
    /youtube\.com\/v\/([^?]+)/,
  ];
  for (const p of patterns) {
    const m = url.match(p);
    if (m) return m[1];
  }
  return null;
}

function NotesPanel({ lessonId, onClose }: { lessonId: number; onClose: () => void }) {
  const { t } = useLanguage();
  const [notes, setNotes] = useState(() => {
    if (typeof window === "undefined") return "";
    return localStorage.getItem(`buddio_notes_${lessonId}`) ?? "";
  });
  const [saved, setSaved] = useState(false);
  const timerRef = React.useRef<ReturnType<typeof setTimeout> | null>(null);
  const storageKey = `buddio_notes_${lessonId}`;

  const handleChange = (value: string) => {
    setNotes(value);
    setSaved(false);
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => {
      localStorage.setItem(storageKey, value);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    }, 800);
  };

  const handleSaveNow = () => {
    if (timerRef.current) clearTimeout(timerRef.current);
    localStorage.setItem(storageKey, notes);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-200 dark:border-[#334155] bg-white dark:bg-[#1e293b] shrink-0">
        <div className="flex items-center gap-2">
          <StickyNote className="w-4 h-4 text-[#7C5CFF]" />
          <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">{t("materi.notesTitle")}</h3>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleSaveNow}
            className="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-[11px] font-semibold text-[#4F8EF7] bg-[#4F8EF7]/8 dark:bg-[#60a5fa]/15 hover:bg-[#4F8EF7]/15 rounded-lg transition-colors"
          >
            <Save className="w-3 h-3" />
            {saved ? t("common.saved") : t("common.save")}
          </button>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 dark:text-slate-500 hover:bg-slate-100 dark:hover:bg-[#334155] hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
          >
            <Minimize2 className="w-4 h-4" />
          </button>
        </div>
      </div>
      <div className="flex-1 p-4 overflow-hidden">
        <textarea
          value={notes}
          onChange={(e) => handleChange(e.target.value)}
          placeholder={t("materi.notesPlaceholder")}
          className="w-full h-full resize-none text-sm text-slate-700 dark:text-slate-300 leading-relaxed bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] rounded-xl p-4 outline-none focus:border-[#4F8EF7] dark:focus:bg-[#0f172a] focus:bg-white transition-all placeholder-slate-400 dark:placeholder-slate-500"
        />
      </div>
      <div className="px-4 py-2 border-t border-slate-100 dark:border-[#334155] bg-slate-50/50 dark:bg-[#0f172a]/50 shrink-0">
        <p className="text-[10px] text-slate-400 dark:text-slate-500 text-center">
          {t("materi.notesAuto", { count: notes.length })}
        </p>
      </div>
    </div>
  );
}

function MateriPageContent() {
  const params = useParams();
  const router = useRouter();
  const lessonId = Number(params?.id);
  const { t } = useLanguage();

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [completing, setCompleting] = useState(false);
  const [fullscreen, setFullscreen] = useState(false);
  const [showNotes, setShowNotes] = useState(false);
  const [highlightMode, setHighlightMode] = useState(false);

  const { highlights, addHighlight, updateNote, updateColor, removeHighlight } = useHighlights(lessonId);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await api.get<Lesson>(`/lessons/${lessonId}`);
        if (!cancelled) setLesson(data);
      } catch (err) {
        if (!cancelled) setError(err instanceof ApiError ? err.message : "Gagal memuat materi.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [lessonId]);

  useEffect(() => {
    if (fullscreen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => { document.body.style.overflow = ""; };
  }, [fullscreen]);

  const handleGenerateContent = async () => {
    if (!lesson || generating) return;
    setGenerating(true);
    setError(null);
    try {
      const data = await api.post<Lesson>(`/lessons/generate/${lesson.roadmap_step_id}`);
      setLesson(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Gagal generate materi.");
    } finally {
      setGenerating(false);
    }
  };

  const handleComplete = async () => {
    if (!lesson || completing) return;
    setCompleting(true);
    try {
      await api.patch(`/lessons/${lesson.id}/complete`);
    } catch {} finally {
      setCompleting(false);
    }
  };

  const handleTanyaBuddio = () => {
    if (!lesson) return;
    const ctx = `Aku sedang belajar materi "${lesson.step_title}" dalam topik "${lesson.topic_title}". `;
    router.push(`/dashboard/mentor?topic=${lesson.topic_id ?? ""}&prompt=${encodeURIComponent(ctx)}`);
  };

  const scrollToHighlight = (color: string) => {
    const h = highlights.find((x) => x.color === color);
    if (!h) return;
    const el = document.querySelector(`[data-highlight-id="${h.id}"]`) as HTMLElement | null;
    if (!el) return;
    el.scrollIntoView({ behavior: "smooth", block: "center" });
    el.style.transition = "outline 0.2s";
    el.style.outline = `3px solid ${color === "yellow" ? "#f59e0b" : color === "green" ? "#22c55e" : color === "blue" ? "#3b82f6" : "#ef4444"}`;
    el.style.outlineOffset = "2px";
    setTimeout(() => {
      el.style.outline = "none";
    }, 1500);
  };

  const hasRichContent = lesson?.content && (lesson.content.includes("## ") || lesson.content.length > 500);
  const videos = lesson?.video_urls ?? [];
  const yellowCount = highlights.filter((h) => h.color === "yellow").length;
  const greenCount = highlights.filter((h) => h.color === "green").length;
  const blueCount = highlights.filter((h) => h.color === "blue").length;
  const redCount = highlights.filter((h) => h.color === "red").length;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
      </div>
    );
  }

  if (error && !lesson) {
    return (
      <div className="max-w-3xl mx-auto py-6 sm:py-8 space-y-6 animate-in fade-in duration-300">
        <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">{error}</div>
        <button onClick={() => router.back()} className="inline-flex items-center gap-1.5 text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors">
          <ArrowLeft className="w-4 h-4" /> Kembali
        </button>
      </div>
    );
  }

  if (!lesson) return null;

  const MateriBody = (
    <>
      {error && <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">{error}</div>}

      {highlights.length > 0 && (
        <div className="flex items-center gap-3 flex-wrap bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-xl px-4 py-2.5">
          <span className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">{t("materi.highlightLabel")}</span>
          {yellowCount > 0 && (
            <button onClick={() => scrollToHighlight("yellow")} className="text-[10px] font-semibold text-amber-700 bg-amber-100 hover:bg-amber-200 px-2 py-0.5 rounded-full transition-colors cursor-pointer">
              {HIGHLIGHT_COLORS.yellow.emoji} {yellowCount}
            </button>
          )}
          {greenCount > 0 && (
            <button onClick={() => scrollToHighlight("green")} className="text-[10px] font-semibold text-emerald-700 bg-emerald-100 hover:bg-emerald-200 px-2 py-0.5 rounded-full transition-colors cursor-pointer">
              {HIGHLIGHT_COLORS.green.emoji} {greenCount}
            </button>
          )}
          {blueCount > 0 && (
            <button onClick={() => scrollToHighlight("blue")} className="text-[10px] font-semibold text-blue-700 bg-blue-100 hover:bg-blue-200 px-2 py-0.5 rounded-full transition-colors cursor-pointer">
              {HIGHLIGHT_COLORS.blue.emoji} {blueCount}
            </button>
          )}
          {redCount > 0 && (
            <button onClick={() => scrollToHighlight("red")} className="text-[10px] font-semibold text-rose-700 bg-rose-100 hover:bg-rose-200 px-2 py-0.5 rounded-full transition-colors cursor-pointer">
              {HIGHLIGHT_COLORS.red.emoji} {redCount}
            </button>
          )}
        </div>
      )}

      {!hasRichContent && !generating ? (
        <div className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-6 sm:p-8 text-center space-y-5">
          <div className="mx-auto w-14 h-14 rounded-full bg-[#4F8EF7]/10 flex items-center justify-center">
            <Sparkles className="w-7 h-7 text-[#4F8EF7]" />
          </div>
          <div className="space-y-1.5 max-w-sm mx-auto">
            <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">{t("materi.notReady")}</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{t("materi.notReadyDesc")}</p>
          </div>
          <button onClick={handleGenerateContent} disabled={generating} className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg transition-all duration-300">
            <Sparkles className="w-4 h-4" /> {t("materi.generate")}
          </button>
        </div>
      ) : generating ? (
        <div className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-6 sm:p-8 text-center space-y-5">
          <Loader2 className="w-10 h-10 text-[#4F8EF7] animate-spin mx-auto" />
          <div className="space-y-1.5">
            <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">{t("materi.generating")}</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">{t("materi.generatingDesc")}</p>
          </div>
        </div>
      ) : (
        <>
          <div className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-5 sm:p-7 space-y-6">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-[#4F8EF7]/10 flex items-center justify-center">
                  <BookOpen className="w-5 h-5 text-[#4F8EF7]" />
                </div>
                <div>
                  <h3 className="font-extrabold text-slate-900 dark:text-slate-100 text-sm">{t("materi.coreTitle")}</h3>
                  <p className="text-[11px] text-slate-400 dark:text-slate-500">{lesson.source ?? "AI Buddio"}</p>
                </div>
              </div>
              <button
                onClick={() => setHighlightMode(!highlightMode)}
                className={`inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-1 rounded-lg transition-all duration-200 ${
                  highlightMode
                    ? "text-amber-700 dark:text-amber-300 bg-amber-100 dark:bg-amber-500/15 border border-amber-200 dark:border-amber-500/30 shadow-sm"
                    : "text-slate-400 dark:text-slate-500 bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] hover:text-slate-600 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-[#334155]"
                }`}
              >
                <Highlighter className="w-3 h-3" />
                {highlightMode ? t("materi.highlightActive") : t("materi.highlightInactive")}
              </button>
            </div>
            <HighlightableContent
              content={lesson.content ?? ""}
              highlights={highlights}
              onAdd={addHighlight}
              onUpdateNote={updateNote}
              onUpdateColor={updateColor}
              onRemove={removeHighlight}
              enabled={highlightMode}
            />
          </div>

          {videos.length > 0 && (
            <div className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-5 sm:p-7 space-y-5">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-rose-50 dark:bg-rose-500/10 flex items-center justify-center">
                  <Video className="w-5 h-5 text-rose-500" />
                </div>
                <div>
                  <h3 className="font-extrabold text-slate-900 dark:text-slate-100 text-sm">{t("materi.videoTitle")}</h3>
                  <p className="text-[11px] text-slate-400 dark:text-slate-500">{t("materi.videoDesc")}</p>
                </div>
              </div>
              <div className="space-y-4">
                {videos.map((v, i) => {
                  const ytId = extractYouTubeId(v.url);
                  return (
                    <div key={i} className="bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] rounded-xl overflow-hidden hover:border-[#4F8EF7]/30 transition-all duration-200">
                      {ytId ? (
                        <>
                          <div className="aspect-video w-full">
                            <iframe src={`https://www.youtube.com/embed/${ytId}?rel=0`} title={v.title} allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen className="w-full h-full" />
                          </div>
                          <div className="px-4 py-3">
                            <p className="text-sm font-bold text-slate-900 dark:text-slate-100">{v.title}</p>
                            {v.description && <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">{v.description}</p>}
                          </div>
                        </>
                      ) : (
                        <a href={v.url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-4 p-4 hover:bg-slate-100/80 dark:hover:bg-[#334155] transition-colors">
                          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-rose-100 to-rose-50 dark:from-rose-500/20 dark:to-rose-500/10 flex items-center justify-center shrink-0">
                            <Play className="w-6 h-6 text-rose-500 ml-0.5" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-bold text-slate-900 dark:text-slate-100">{v.title}</p>
                            {v.description && <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{v.description}</p>}
                          </div>
                          <ExternalLink className="w-4 h-4 text-slate-400 dark:text-slate-500 shrink-0" />
                        </a>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          <div className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-5 sm:p-7">
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
              <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white flex items-center justify-center shadow-md shadow-[#4F8EF7]/15 shrink-0">
                <MessageCircle className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">{t("materi.stillConfused")}</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed mt-0.5">{t("materi.stillConfusedDesc", { step: lesson.step_title ?? "" })}</p>
              </div>
              <button onClick={handleTanyaBuddio} className="shrink-0 inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg transition-all duration-300">
                <MessageCircle className="w-4 h-4" /> {t("materi.askBuddio")}
              </button>
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button onClick={handleGenerateContent} disabled={generating} className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold text-[#4F8EF7] bg-[#4F8EF7]/8 hover:bg-[#4F8EF7]/15 border border-[#4F8EF7]/20 rounded-xl transition-all duration-200">
              <RefreshCw className="w-3.5 h-3.5" /> {t("materi.regenerate")}
            </button>
          </div>
        </>
      )}
    </>
  );

  if (fullscreen) {
    return (
      <div className="fixed inset-0 z-50 flex flex-col bg-[#F8FAFC] dark:bg-[#0f172a]">
        <div className="flex items-center justify-between px-6 py-3 bg-white dark:bg-[#1e293b] border-b border-slate-200 dark:border-[#334155] shrink-0">
          <div className="flex items-center gap-3 min-w-0">
            <button onClick={() => setFullscreen(false)} className="inline-flex items-center gap-1.5 text-[11px] font-bold text-slate-400 dark:text-slate-500 hover:text-slate-700 dark:hover:text-slate-200 transition-colors cursor-pointer">
              <Minimize2 className="w-3.5 h-3.5" /> {t("materi.exitStudyMode")}
            </button>
            <div className="w-px h-4 bg-slate-200 dark:bg-[#334155]" />
            <h1 className="text-sm font-extrabold text-slate-900 dark:text-slate-100 truncate">{lesson.step_title}</h1>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={() => setHighlightMode(!highlightMode)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-semibold rounded-lg transition-all duration-200 ${
                highlightMode
                  ? "text-amber-700 dark:text-amber-300 bg-amber-100 dark:bg-amber-500/15 border border-amber-200 dark:border-amber-500/30 shadow-sm"
                  : "text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-500/10 hover:bg-amber-100 dark:hover:bg-amber-500/20 border border-amber-100 dark:border-amber-500/20"
              }`}
            >
              <Highlighter className="w-3.5 h-3.5" /> {highlightMode ? t("materi.highlightOn") : t("materi.highlight")}
            </button>
            <button
              onClick={() => setShowNotes(!showNotes)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-semibold rounded-lg transition-all duration-200 ${
                showNotes ? "text-white bg-[#7C5CFF] shadow-md shadow-[#7C5CFF]/15" : "text-[#7C5CFF] bg-[#7C5CFF]/8 hover:bg-[#7C5CFF]/15 border border-[#7C5CFF]/20"
              }`}
            >
              <StickyNote className="w-3.5 h-3.5" /> {t("materi.notes")}
            </button>
            <button onClick={handleComplete} disabled={completing} className="inline-flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-semibold text-white bg-gradient-to-r from-[#22C55E] to-emerald-400 rounded-lg shadow-md hover:scale-[1.02] transition-all duration-300 disabled:opacity-50">
              {completing ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <CheckCircle2 className="w-3.5 h-3.5" />} {t("materi.done")}
            </button>
          </div>
        </div>
        <div className="flex flex-1 min-h-0">
          <div className={`flex-1 overflow-y-auto transition-all duration-300 ${showNotes ? "" : ""}`}>
            <div className={`mx-auto py-6 space-y-6 ${showNotes ? "max-w-2xl px-6" : "max-w-3xl px-6"}`}>
              {MateriBody}
            </div>
          </div>
          {showNotes && (
            <div className="w-[380px] shrink-0 border-l border-slate-200 dark:border-[#334155] bg-white dark:bg-[#1e293b] animate-in slide-in-from-right duration-300">
              <NotesPanel lessonId={lessonId} onClose={() => setShowNotes(false)} />
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      <div className="flex items-center justify-between gap-4 border-b border-slate-100 dark:border-[#334155] pb-6">
        <div className="space-y-1.5 min-w-0">
          <button onClick={() => router.back()} className="inline-flex items-center gap-1.5 text-[11px] font-bold text-slate-400 dark:text-slate-500 hover:text-slate-700 dark:hover:text-slate-200 transition-colors cursor-pointer mb-2">
            <ArrowLeft className="w-3.5 h-3.5" /> {t("materi.backToRoadmap")}
          </button>
          <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">{lesson.step_title}</h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">{t("materi.topic", { topic: lesson.topic_title ?? "" })}</p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={() => setHighlightMode(!highlightMode)}
            className={`inline-flex items-center gap-1.5 px-3 py-2.5 text-xs font-semibold rounded-xl transition-all duration-200 ${
              highlightMode
                ? "text-amber-700 dark:text-amber-300 bg-amber-100 dark:bg-amber-500/15 border border-amber-200 dark:border-amber-500/30 shadow-sm"
                : "text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-[#1e293b] border border-slate-200 dark:border-[#334155] hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#334155]"
            }`}
          >
            <Highlighter className="w-4 h-4" /> <span className="hidden sm:inline">{highlightMode ? t("materi.highlightOn") : t("materi.highlight")}</span>
          </button>
          <button onClick={() => { setFullscreen(true); setShowNotes(true); }} className="inline-flex items-center gap-1.5 px-3 py-2.5 text-xs font-semibold text-[#4F8EF7] bg-[#4F8EF7]/8 hover:bg-[#4F8EF7]/15 border border-[#4F8EF7]/20 rounded-xl transition-all duration-200">
            <Maximize2 className="w-4 h-4" /> <span className="hidden sm:inline">{t("materi.studyMode")}</span>
          </button>
          <button onClick={handleComplete} disabled={completing} className="inline-flex items-center gap-2 px-4 py-2.5 text-xs font-semibold text-white bg-gradient-to-r from-[#22C55E] to-emerald-400 rounded-xl shadow-md hover:scale-[1.02] transition-all duration-300 disabled:opacity-50">
            {completing ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />} {t("materi.done")}
          </button>
        </div>
      </div>
      {MateriBody}
    </div>
  );
}

export default function MateriPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center py-24"><Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" /></div>}>
      <MateriPageContent />
    </Suspense>
  );
}
