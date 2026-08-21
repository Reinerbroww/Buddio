"use client";

import React, { Suspense, useCallback, useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
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
} from "lucide-react";
import api, { ApiError } from "@/services/api";
import type { Lesson } from "@/lib/types";

function MateriContent({ content }: { content: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm, remarkMath]}
      rehypePlugins={[rehypeKatex]}
      components={{
        h2: (props) => (
          <h2
            className="text-lg font-extrabold text-slate-900 mt-8 mb-3 first:mt-0 flex items-center gap-2"
            {...props}
          />
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
          <blockquote
            className="border-l-4 border-[#4F8EF7] pl-4 italic my-3 text-slate-600 bg-[#4F8EF7]/5 py-2 pr-3 rounded-r-lg"
            {...props}
          />
        ),
        hr: (props) => <hr className="my-5 border-slate-200/60" {...props} />,
        pre: (props) => (
          <pre
            className="block bg-slate-50 text-slate-800 p-4 rounded-xl text-xs font-mono border border-slate-100 overflow-x-auto my-3 max-w-full"
            {...props}
          />
        ),
        code: ({ className, children, ...props }: any) => {
          const isBlock = className?.includes("language-");
          return isBlock ? (
            <code className="font-mono text-xs" {...props}>
              {children}
            </code>
          ) : (
            <code
              className="bg-slate-100 text-[#4F8EF7] px-1.5 py-0.5 rounded text-xs font-mono"
              {...props}
            >
              {children}
            </code>
          );
        },
        table: (props) => (
          <div className="overflow-x-auto my-3">
            <table className="min-w-full text-sm border border-slate-200 rounded-xl overflow-hidden" {...props} />
          </div>
        ),
        thead: (props) => <thead className="bg-slate-50" {...props} />,
        th: (props) => (
          <th className="px-4 py-2 text-left text-xs font-bold text-slate-600 border-b border-slate-200" {...props} />
        ),
        td: (props) => (
          <td className="px-4 py-2 text-sm text-slate-700 border-b border-slate-100" {...props} />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}

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

function extractYouTubeSearchQuery(url: string): string | null {
  const match = url.match(/youtube\.com\/results\?search_query=([^&]+)/);
  if (match) return decodeURIComponent(match[1].replace(/\+/g, " "));
  return null;
}

function MateriPageContent() {
  const params = useParams();
  const router = useRouter();
  const lessonId = Number(params?.id);

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [completing, setCompleting] = useState(false);

  const loadLesson = useCallback(async () => {
    if (!lessonId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.get<Lesson>(`/lessons/${lessonId}`);
      setLesson(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Gagal memuat materi.");
    } finally {
      setLoading(false);
    }
  }, [lessonId]);

  useEffect(() => {
    loadLesson();
  }, [loadLesson]);

  const handleGenerateContent = async () => {
    if (!lesson || generating) return;
    setGenerating(true);
    setError(null);
    try {
      const stepId = lesson.roadmap_step_id;
      const data = await api.post<Lesson>(`/lessons/generate/${stepId}`);
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
    } catch {
    } finally {
      setCompleting(false);
    }
  };

  const handleTanyaBuddio = () => {
    if (!lesson) return;
    const context = `Aku sedang belajar materi "${lesson.step_title}" dalam topik "${lesson.topic_title}". `;
    router.push(
      `/dashboard/mentor?topic=${lesson.topic_id ?? ""}&prompt=${encodeURIComponent(context)}`
    );
  };

  const hasRichContent =
    lesson?.content && (lesson.content.includes("## ") || lesson.content.length > 500);
  const videos = lesson?.video_urls ?? [];

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
        <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
          {error}
        </div>
        <button
          onClick={() => router.back()}
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Kembali
        </button>
      </div>
    );
  }

  if (!lesson) return null;

  return (
    <div className="max-w-3xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      {error && (
        <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
          {error}
        </div>
      )}

      <div className="flex items-center justify-between gap-4 border-b border-slate-100 pb-6">
        <div className="space-y-1.5 min-w-0">
          <button
            onClick={() => router.back()}
            className="inline-flex items-center gap-1.5 text-[11px] font-bold text-slate-400 hover:text-slate-700 transition-colors cursor-pointer mb-2"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            Kembali ke Roadmap
          </button>
          <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
            {lesson.step_title}
          </h2>
          <p className="text-xs text-slate-500">
            Topik: {lesson.topic_title}
          </p>
        </div>
        <button
          onClick={handleComplete}
          disabled={completing}
          className="shrink-0 inline-flex items-center gap-2 px-4 py-2.5 text-xs font-semibold text-white bg-gradient-to-r from-[#22C55E] to-emerald-400 rounded-xl shadow-md hover:scale-[1.02] transition-all duration-300 disabled:opacity-50"
        >
          {completing ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <CheckCircle2 className="w-4 h-4" />
          )}
          Selesai
        </button>
      </div>

      {!hasRichContent && !generating ? (
        <div className="bg-white border border-slate-100 rounded-2xl p-6 sm:p-8 text-center space-y-5">
          <div className="mx-auto w-14 h-14 rounded-full bg-[#4F8EF7]/10 flex items-center justify-center">
            <Sparkles className="w-7 h-7 text-[#4F8EF7]" />
          </div>
          <div className="space-y-1.5 max-w-sm mx-auto">
            <h3 className="font-bold text-slate-900 text-sm">Materi belum tersedia</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Klik tombol di bawah agar AI Buddio menyusun materi pembelajaran lengkap, termasuk video
              pembelajaran.
            </p>
          </div>
          <button
            onClick={handleGenerateContent}
            disabled={generating}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg transition-all duration-300"
          >
            <Sparkles className="w-4 h-4" />
            Generate Materi Sekarang
          </button>
        </div>
      ) : generating ? (
        <div className="bg-white border border-slate-100 rounded-2xl p-6 sm:p-8 text-center space-y-5">
          <Loader2 className="w-10 h-10 text-[#4F8EF7] animate-spin mx-auto" />
          <div className="space-y-1.5">
            <h3 className="font-bold text-slate-900 text-sm">Menyusun materi...</h3>
            <p className="text-xs text-slate-500">
              AI Buddio sedang menyiapkan materi lengkap untukmu.
            </p>
          </div>
        </div>
      ) : (
        <>
          <div className="bg-white border border-slate-100 rounded-2xl p-5 sm:p-7 space-y-6">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-[#4F8EF7]/10 flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-[#4F8EF7]" />
              </div>
              <div>
                <h3 className="font-extrabold text-slate-900 text-sm">Materi Inti</h3>
                <p className="text-[11px] text-slate-400">
                  {lesson.source ?? "AI Buddio"}
                </p>
              </div>
            </div>
            <div className="prose-sm max-w-none">
              <MateriContent content={lesson.content ?? ""} />
            </div>
          </div>

          {videos.length > 0 && (
            <div className="bg-white border border-slate-100 rounded-2xl p-5 sm:p-7 space-y-5">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-rose-50 flex items-center justify-center">
                  <Video className="w-5 h-5 text-rose-500" />
                </div>
                <div>
                  <h3 className="font-extrabold text-slate-900 text-sm">Belajar Lewat Video</h3>
                  <p className="text-[11px] text-slate-400">
                    Video relevan untuk memperdalam pemahamanmu.
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {videos.map((v, i) => {
                  const ytId = extractYouTubeId(v.url);
                  const searchQuery = !ytId ? extractYouTubeSearchQuery(v.url) : null;
                  return (
                    <div
                      key={i}
                      className="bg-slate-50 border border-slate-100 rounded-xl overflow-hidden hover:border-[#4F8EF7]/30 transition-all duration-200"
                    >
                      {ytId ? (
                        <div className="aspect-video w-full">
                          <iframe
                            src={`https://www.youtube.com/embed/${ytId}`}
                            title={v.title}
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                            className="w-full h-full"
                          />
                        </div>
                      ) : searchQuery ? (
                        <div className="aspect-video w-full">
                          <iframe
                            src={`https://www.youtube.com/embed?listType=search&list=${encodeURIComponent(searchQuery)}`}
                            title={v.title}
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                            className="w-full h-full"
                          />
                        </div>
                      ) : (
                        <a
                          href={v.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-3 p-4 hover:bg-slate-100 transition-colors"
                        >
                          <div className="w-10 h-10 rounded-lg bg-rose-100 flex items-center justify-center shrink-0">
                            <Play className="w-5 h-5 text-rose-500" />
                          </div>
                          <div className="min-w-0 flex-1">
                            <p className="text-sm font-semibold text-slate-900 truncate">{v.title}</p>
                            <p className="text-[11px] text-slate-500 truncate">
                              {v.description || "Klik untuk menonton"}
                            </p>
                          </div>
                          <ExternalLink className="w-4 h-4 text-slate-400 shrink-0" />
                        </a>
                      )}
                      <div className="px-3 py-2.5 border-t border-slate-100">
                        <p className="text-xs font-semibold text-slate-900">{v.title}</p>
                        {v.description && (
                          <p className="text-[11px] text-slate-500 mt-0.5">{v.description}</p>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          <div className="bg-white border border-slate-100 rounded-2xl p-5 sm:p-7">
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
              <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white flex items-center justify-center shadow-md shadow-[#4F8EF7]/15 shrink-0">
                <MessageCircle className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-bold text-slate-900 text-sm">Masih Bingung?</h3>
                <p className="text-xs text-slate-500 leading-relaxed mt-0.5">
                  Tanya Kak Buddio langsung tentang materi &quot;{lesson.step_title}&quot; ini.
                  Buddio sudah tahu konteks yang kamu pelajari!
                </p>
              </div>
              <button
                onClick={handleTanyaBuddio}
                className="shrink-0 inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg transition-all duration-300"
              >
                <MessageCircle className="w-4 h-4" />
                Tanya Kak Buddio
              </button>
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={handleGenerateContent}
              disabled={generating}
              className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold text-[#4F8EF7] bg-[#4F8EF7]/8 hover:bg-[#4F8EF7]/15 border border-[#4F8EF7]/20 rounded-xl transition-all duration-200"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Regenerate Materi
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default function MateriPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center py-24">
          <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
        </div>
      }
    >
      <MateriPageContent />
    </Suspense>
  );
}
