"use client";

import React, { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Sparkles, Loader2, Map, RefreshCw, BookOpen, Clock, Target, ChevronDown, Check } from "lucide-react";
import api, { ApiError } from "@/services/api";
import type { Topic, Roadmap, RoadmapStep } from "@/lib/types";

function difficultyStyle(difficulty: string | null | undefined) {
  if (!difficulty) return null;
  const lower = difficulty.toLowerCase();
  if (lower.includes("mudah") || lower.includes("easy")) {
    return { label: "Mudah", className: "bg-emerald-50 text-emerald-600 border-emerald-100" };
  }
  if (lower.includes("sedang") || lower.includes("medium")) {
    return { label: "Sedang", className: "bg-amber-50 text-amber-600 border-amber-100" };
  }
  if (lower.includes("sulit") || lower.includes("hard") || lower.includes("sukar")) {
    return { label: "Sulit", className: "bg-rose-50 text-rose-600 border-rose-100" };
  }
  return { label: difficulty, className: "bg-slate-50 text-slate-600 border-slate-100" };
}

function RoadmapPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const topicParam = searchParams.get("topic");
  const selectedTopicId =
    topicParam && !Number.isNaN(Number(topicParam)) ? Number(topicParam) : null;

  const [topics, setTopics] = useState<Topic[]>([]);
  const [topicsLoading, setTopicsLoading] = useState(true);
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [roadmapLoading, setRoadmapLoading] = useState(false);
  const [roadmapMissing, setRoadmapMissing] = useState(false);
  const [loadedTopicId, setLoadedTopicId] = useState<number | null>(null);
  const [generating, setGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [quotaExceeded, setQuotaExceeded] = useState(false);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());
  const timerRef = useRef<number | null>(null);

  const loadTopics = useCallback(() => {
    api
      .get<Topic[]>("/topics")
      .then((data) => setTopics(data))
      .catch((err) => {
        setError(err instanceof ApiError ? err.message : "Gagal memuat daftar topik.");
      })
      .finally(() => setTopicsLoading(false));
  }, []);

  const loadRoadmap = useCallback((topicId: number) => {
    api
      .get<Roadmap>(`/roadmaps/topic/${topicId}`)
      .then((data) => {
        setRoadmap(data);
        setRoadmapMissing(false);
        setLoadedTopicId(topicId);
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 404) {
          setRoadmapMissing(true);
          setLoadedTopicId(topicId);
        } else if (err instanceof ApiError && err.status === 429) {
          setQuotaExceeded(true);
          setError(err.message);
          setRoadmapMissing(true);
          setLoadedTopicId(topicId);
        } else {
          setError(err instanceof ApiError ? err.message : "Gagal memuat roadmap.");
        }
      })
      .finally(() => setRoadmapLoading(false));
  }, []);

  useEffect(() => {
    loadTopics();
  }, [loadTopics]);

  useEffect(() => {
    if (selectedTopicId != null) {
      loadRoadmap(selectedTopicId);
    }
  }, [selectedTopicId, loadRoadmap]);

  useEffect(() => {
    return () => {
      if (timerRef.current) window.clearInterval(timerRef.current);
    };
  }, []);

  const handleSelectTopic = useCallback(
    (topicId: string) => {
      router.replace(`?topic=${topicId}`);
    },
    [router]
  );

  const startGenerate = useCallback(
    async (regenerate: boolean) => {
      if (selectedTopicId == null) return;
      setError(null);
      setQuotaExceeded(false);
      setGenerating(true);
      setProgress(8);
      timerRef.current = window.setInterval(() => {
        setProgress((p) => Math.min(p + Math.floor(Math.random() * 12) + 3, 92));
      }, 400);
      try {
        const data = await api.post<Roadmap>("/roadmaps/generate", {
          topic_id: selectedTopicId,
          ...(regenerate ? { regenerate: true } : {}),
        });
        setProgress(100);
        setRoadmap(data);
        setRoadmapMissing(false);
      } catch (err) {
        if (err instanceof ApiError && err.status === 429) {
          setQuotaExceeded(true);
          setError(err.message);
        } else {
          setError(err instanceof ApiError ? err.message : "Gagal membuat roadmap.");
        }
      } finally {
        if (timerRef.current) {
          window.clearInterval(timerRef.current);
          timerRef.current = null;
        }
        window.setTimeout(() => {
          setGenerating(false);
          setProgress(0);
        }, 600);
      }
    },
    [selectedTopicId]
  );

  const toggleStep = useCallback(async (step: RoadmapStep) => {
    setError(null);
    try {
      const res = await api.patch<{ step_id: number; completed: boolean; completion_percentage: number }>(
        `/roadmaps/steps/${step.id}`,
        { completed: !step.completed }
      );
      setRoadmap((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          completion_percentage: res.completion_percentage,
          steps: prev.steps.map((s) => (s.id === step.id ? { ...s, completed: res.completed } : s)),
        };
      });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Gagal memperbarui langkah.");
    }
  }, []);

  const toggleExpand = useCallback((stepId: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(stepId)) next.delete(stepId);
      else next.add(stepId);
      return next;
    });
  }, []);

  const topic = selectedTopicId != null ? topics.find((t) => t.id === selectedTopicId) : undefined;
  const roadmapLoadedForTopic = selectedTopicId != null && loadedTopicId === selectedTopicId;
  const showRoadmapLoading = roadmapLoading || (selectedTopicId != null && !roadmapLoadedForTopic);
  const showRoadmapMissing = roadmapLoadedForTopic && roadmapMissing;

  return (
    <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      {error && (
        <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
          {error}
        </div>
      )}

      {selectedTopicId == null ? (
        <div className="bg-white border border-slate-100 rounded-2xl p-6 sm:p-8">
          <div className="flex items-center gap-2 mb-1.5">
            <Map className="w-5 h-5 text-[#4F8EF7]" />
            <h3 className="font-bold text-slate-900 text-base">Pilih Topik Belajar</h3>
          </div>
          <p className="text-xs text-slate-500 mb-5">
            Pilih salah satu topikmu untuk melihat peta belajar (roadmap) yang sudah disusun AI.
          </p>
          {topicsLoading ? (
            <div className="flex items-center justify-center py-10">
              <Loader2 className="w-6 h-6 text-[#4F8EF7] animate-spin" />
            </div>
          ) : topics.length === 0 ? (
            <p className="text-sm text-slate-500">
              Belum ada topik. Buat topik terlebih dahulu dari halaman Dashboard.
            </p>
          ) : (
            <div className="space-y-3">
              <select
                value=""
                onChange={(e) => handleSelectTopic(e.target.value)}
                className="w-full px-4 py-3 text-sm bg-slate-50 border border-slate-100 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all"
              >
                <option value="" disabled>
                  Pilih topik...
                </option>
                {topics.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.title} {t.has_roadmap ? "(Roadmap tersedia)" : ""}
                  </option>
                ))}
              </select>
              <div className="space-y-2">
                {topics.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => handleSelectTopic(String(t.id))}
                    className="w-full flex items-center justify-between gap-3 px-4 py-3 bg-slate-50 hover:bg-slate-100 border border-slate-100 rounded-xl transition-all duration-200 text-left group"
                  >
                    <span className="text-sm font-semibold text-slate-800">{t.title}</span>
                    <span className="text-[11px] text-slate-400 shrink-0">
                      {t.has_roadmap ? "Roadmap tersedia" : "Belum ada roadmap"}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : showRoadmapLoading ? (
        <div className="flex items-center justify-center py-24">
          <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
        </div>
      ) : showRoadmapMissing ? (
        <div className="bg-white border border-slate-100 rounded-2xl p-8 sm:p-12 flex flex-col items-center text-center gap-6">
          <div className="relative flex items-center justify-center w-16 h-16 rounded-full bg-slate-50 border border-slate-100">
            <Map className="w-8 h-8 text-[#4F8EF7]" />
          </div>
          <div className="space-y-2 max-w-md">
            <h3 className="text-base font-bold text-slate-900">Belum ada roadmap untuk topik ini</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Biarkan AI Mentor menyusun peta belajar langkah demi langkah untuk {topic?.title ?? "topik ini"}.
            </p>
          </div>
          <button
            onClick={() => startGenerate(false)}
            disabled={generating || quotaExceeded}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Sparkles className="w-4 h-4" />
            Buat Roadmap
          </button>
          {quotaExceeded && (
            <p className="text-xs text-rose-500 font-medium">Kuota harian untuk membuat roadmap telah habis.</p>
          )}
        </div>
      ) : roadmap ? (
        <>
          <div className="bg-white border border-slate-100 rounded-2xl p-6 sm:p-8 space-y-6 relative overflow-hidden">
            <div className="absolute -right-16 -bottom-16 w-36 h-36 bg-gradient-to-br from-[#4F8EF7]/5 to-[#7C5CFF]/5 rounded-full blur-2xl" />
            <div className="relative z-10 space-y-5">
              <div className="flex flex-wrap items-center gap-2">
                {roadmap.mode === "mock" && (
                  <span className="inline-flex items-center px-2.5 py-0.5 text-[9px] font-bold text-amber-600 bg-amber-50 border border-amber-100 rounded-full uppercase tracking-wider">
                    Mode Demo
                  </span>
                )}
                {difficultyStyle(roadmap.difficulty) && (
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 text-[9px] font-bold rounded-full border ${difficultyStyle(roadmap.difficulty)?.className}`}
                  >
                    {difficultyStyle(roadmap.difficulty)?.label}
                  </span>
                )}
              </div>
              <div>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                  {roadmap.title}
                </h2>
                {topic && <p className="text-sm text-slate-500 mt-1">Topik: {topic.title}</p>}
              </div>
              <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-xs text-slate-500">
                {roadmap.estimated_hours != null && (
                  <span className="inline-flex items-center gap-1.5">
                    <Clock className="w-4 h-4 text-[#4F8EF7]" />
                    Estimasi {roadmap.estimated_hours} jam
                  </span>
                )}
                <span className="inline-flex items-center gap-1.5">
                  <Target className="w-4 h-4 text-[#7C5CFF]" />
                  {roadmap.steps.length} langkah
                </span>
              </div>
              <div>
                <div className="flex justify-between items-center text-xs font-semibold text-slate-500 mb-1.5">
                  <span>Progres Peta Belajar</span>
                  <span className="text-slate-900 font-extrabold">{roadmap.completion_percentage}%</span>
                </div>
                <div className="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] rounded-full transition-all duration-500"
                    style={{ width: `${roadmap.completion_percentage}%` }}
                  />
                </div>
              </div>
              <div className="flex justify-end pt-2">
                <button
                  onClick={() => startGenerate(true)}
                  disabled={generating || quotaExceeded}
                  className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold text-[#4F8EF7] bg-[#4F8EF7]/8 hover:bg-[#4F8EF7]/15 border border-[#4F8EF7]/20 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  Generate Ulang Roadmap
                </button>
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <h3 className="text-xs font-extrabold text-slate-400 uppercase tracking-wider">Langkah Belajar</h3>
            {[...roadmap.steps]
              .sort((a, b) => a.order_number - b.order_number)
              .map((step) => {
                const isExpanded = expanded.has(step.id);
                return (
                  <div key={step.id} className="bg-white border border-slate-100 rounded-2xl overflow-hidden">
                    <div className="flex items-center gap-3 p-4">
                      <button
                        onClick={() => toggleStep(step)}
                        aria-label={step.completed ? "Tandai belum selesai" : "Tandai selesai"}
                        className={`shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-200 ${
                          step.completed
                            ? "bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] border-transparent"
                            : "border-slate-300 hover:border-[#4F8EF7]"
                        }`}
                      >
                        {step.completed && <Check className="w-3.5 h-3.5 text-white" />}
                      </button>
                      <div className="flex-1 min-w-0">
                        <p className="text-[10px] font-bold text-slate-400 uppercase">Langkah {step.order_number}</p>
                        <p className={`text-sm font-semibold ${step.completed ? "text-slate-400 line-through" : "text-slate-900"}`}>
                          {step.title}
                        </p>
                      </div>
                      {step.lesson_id && (
                        <button
                          onClick={() => router.push(`/dashboard/materi/${step.lesson_id}`)}
                          className="shrink-0 inline-flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-semibold text-white bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] rounded-lg shadow-xs hover:scale-[1.02] transition-all duration-200"
                        >
                          <BookOpen className="w-3.5 h-3.5" />
                          Buka Materi
                        </button>
                      )}
                      <button
                        onClick={() => {
                          const queryPrompt = `Kak, tolong jelaskan tentang langkah belajar "${step.title}" dalam topik "${topic?.title ?? ""}". Apa konsep utamanya dan bagaimana cara memahaminya?`;
                          router.push(`/dashboard/mentor?topic=${selectedTopicId}&prompt=${encodeURIComponent(queryPrompt)}`);
                        }}
                        title="Tanya Mentor (Fast Track)"
                        className="shrink-0 inline-flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-semibold text-[#4F8EF7] bg-[#4F8EF7]/8 hover:bg-[#4F8EF7]/15 border border-[#4F8EF7]/20 rounded-lg shadow-xs hover:scale-[1.02] transition-all duration-200"
                      >
                        <Sparkles className="w-3.5 h-3.5" />
                        <span className="hidden sm:inline">Tanya Mentor</span>
                      </button>
                      <button
                        onClick={() => toggleExpand(step.id)}
                        aria-label={isExpanded ? "Tutup deskripsi" : "Buka deskripsi"}
                        className="shrink-0 p-1 rounded-lg text-slate-400 hover:bg-slate-50 hover:text-slate-600 transition-colors"
                      >
                        <ChevronDown
                          className={`w-5 h-5 transition-transform duration-200 ${isExpanded ? "rotate-180" : ""}`}
                        />
                      </button>
                    </div>
                    {isExpanded && (
                      <div className="px-4 pb-4">
                        <div className="pl-9">
                          {step.description ? (
                            <p className="text-xs text-slate-500 leading-relaxed whitespace-pre-wrap">{step.description}</p>
                          ) : (
                            <p className="text-xs text-slate-400 italic">Tidak ada deskripsi untuk langkah ini.</p>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
          </div>
        </>
      ) : null}

      {generating && (
        <>
          <div className="fixed inset-0 bg-slate-950/40 backdrop-blur-xs z-50 animate-in fade-in duration-300" />
          <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl shadow-xl border border-slate-100 p-6 w-[90%] max-w-sm z-50 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center gap-2 pb-3">
              <Sparkles className="w-5 h-5 text-[#4F8EF7] animate-pulse" />
              <h3 className="font-bold text-slate-900 text-sm">Menyusun Roadmap AI...</h3>
            </div>
            <p className="text-xs text-slate-500 mb-3">AI Mentor sedang menyusun langkah belajar terbaik untukmu.</p>
            <div className="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-right text-xs font-bold text-slate-500 mt-1.5">{progress}%</p>
          </div>
        </>
      )}

    </div>
  );
}

export default function RoadmapPage() {
  return (
    <Suspense fallback={null}>
      <RoadmapPageContent />
    </Suspense>
  );
}
