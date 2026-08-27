"use client";

import React, { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { Plus, Sparkles, GraduationCap, ArrowRight, X, Play, Loader2, Flame, Clock, Target, Zap } from "lucide-react";
import api, { ApiError } from "@/services/api";
import { useAuth } from "@/context/AuthContext";
import type { ProgressStat, Topic, Usage } from "@/lib/types";

export default function DashboardPage() {
  const { user } = useAuth();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [stats, setStats] = useState<ProgressStat | null>(null);
  const [usage, setUsage] = useState<Usage | null>(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [topicName, setTopicName] = useState("");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(() => {
    Promise.all([
      api.get<Topic[]>("/topics"),
      api.get<ProgressStat>("/progress/statistics"),
      api.get<Usage>("/usage/me"),
    ])
      .then(([t, s, u]) => {
        setTopics(t);
        setStats(s);
        setUsage(u);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? err.message : "Gagal memuat data.");
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleCreateTopic = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topicName.trim()) return;
    setCreating(true);
    setError(null);
    try {
      const topic = await api.post<Topic>("/topics", { title: topicName.trim() });
      setTopicName("");
      setShowModal(false);
      window.location.href = `/dashboard/roadmap?topic=${topic.id}`;
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Gagal membuat topik.");
      setCreating(false);
    }
  };

  const sorted = [...topics].sort((a, b) => b.progress_percentage - a.progress_percentage);
  const active = sorted[0];
  const others = sorted.slice(1);

  const aiRecommendations = [
    { name: "Algoritma & Pemrograman", reason: "Cocok untuk memperkuat dasar logika matematika.", tag: "Logika Dasar" },
    { name: "Persiapan SNBT: Tes Kognitif", reason: "Dirancang khusus untuk target masuk PTN.", tag: "Ujian PTN" },
    { name: "Pengenalan Sains Data", reason: "Langkah lanjutan ideal setelah topik data.", tag: "Lanjutan" },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
      </div>
    );
  }

  const name = user?.full_name || user?.email.split("@")[0] || "Pembelajar";

  const statCards = [
    { label: "Jam Belajar", value: stats?.study_hours ?? 0, icon: Clock, color: "#4F8EF7" },
    { label: "Topik Aktif", value: stats?.topics ?? 0, icon: Target, color: "#7C5CFF" },
    { label: "Streak Hari", value: stats?.streak ?? 0, icon: Flame, color: "#F97316" },
    { label: "Rata-rata Progres", value: `${stats?.completion ?? 0}%`, icon: Zap, color: "#22C55E" },
  ];

  return (
    <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      {error && (
        <div className="text-xs bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 text-rose-600 dark:text-rose-400 rounded-xl px-4 py-3">
          {error}
        </div>
      )}

      {/* Welcome Section Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6 border-b border-slate-100 dark:border-[#334155] pb-8">
        <div className="space-y-1.5">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight font-sans">
            Halo {name} 👋
          </h2>
          <p className="text-sm sm:text-base text-slate-500 dark:text-slate-400 font-sans">
            Apa yang ingin kamu pelajari hari ini? AI Mentor siap mendampingi perjalanan belajarmu.
          </p>
        </div>

        <div className="shrink-0">
          <button
            onClick={() => setShowModal(true)}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg transition-all duration-300 group cursor-pointer"
          >
            <Plus className="w-5 h-5 transition-transform group-hover:rotate-90 duration-300" />
            <span>Buat Topik Baru</span>
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card) => {
          const Icon = card.icon;
          return (
            <div key={card.label} className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-4 flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: `${card.color}14`, color: card.color }}>
                <Icon className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <p className="text-xl font-extrabold text-slate-900 dark:text-slate-100 leading-tight">{card.value}</p>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 font-medium">{card.label}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quota Indicator */}
      {usage && (
        <div className="bg-gradient-to-r from-[#4F8EF7]/8 to-[#7C5CFF]/8 border border-slate-100 dark:border-[#334155] rounded-2xl p-4 flex flex-wrap items-center gap-x-6 gap-y-2">
          <span className="text-[11px] font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Kuota AI hari ini</span>
          <span className="text-xs text-slate-600 dark:text-slate-300">💬 Chat <b>{usage.chat_remaining}/{usage.limits.chat}</b></span>
          <span className="text-xs text-slate-600 dark:text-slate-300">🗺️ Roadmap <b>{usage.roadmap_remaining}/{usage.limits.roadmap}</b></span>
          <span className="text-xs text-slate-600 dark:text-slate-300">📝 Kuis <b>{usage.quiz_remaining}/{usage.limits.quiz}</b></span>
        </div>
      )}

      {topics.length > 0 ? (
        <div className="space-y-8 animate-in fade-in duration-300">
          {/* Continue Learning */}
          <div className="space-y-4">
            <h3 className="text-xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Lanjutkan Belajar</h3>
            <div className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-6 shadow-xs hover:shadow-md transition-all duration-300 relative overflow-hidden group">
              <div className="absolute -right-16 -bottom-16 w-36 h-36 bg-gradient-to-br from-[#4F8EF7]/5 to-[#7C5CFF]/5 rounded-full blur-2xl group-hover:scale-110 transition-transform duration-500" />
              <div className="space-y-5 relative z-10">
                <div className="h-2.5 w-full bg-slate-100 dark:bg-[#334155] rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] rounded-full transition-all duration-500" style={{ width: `${active?.progress_percentage ?? 0}%` }} />
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div>
                    <h4 className="text-xl font-bold text-slate-900 dark:text-slate-100">{active?.title}</h4>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                      {active?.has_roadmap ? "Roadmap siap dilanjutkan." : "Belum ada roadmap. Buat peta belajarnya sekarang!"}
                    </p>
                  </div>
                  <div className="flex items-center justify-between sm:justify-end gap-6">
                    <span className="text-lg font-extrabold text-slate-900 dark:text-slate-100">{active?.progress_percentage ?? 0}%</span>
                    <Link
                      href={`/dashboard/roadmap?topic=${active?.id}`}
                      className="inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-[#4F8EF7] hover:bg-[#4F8EF7]/90 text-white font-semibold text-xs rounded-xl transition-all duration-200 shadow-xs hover:scale-[1.02]"
                    >
                      <Play className="w-3.5 h-3.5 fill-current shrink-0" />
                      <span>{active?.has_roadmap ? "Lanjutkan" : "Buat Roadmap"}</span>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Other topics */}
          {others.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Topik Aktif Lainnya</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {others.map((topic) => (
                  <Link
                    key={topic.id}
                    href={`/dashboard/roadmap?topic=${topic.id}`}
                    className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-xl p-5 hover:border-[#4F8EF7]/30 transition-all duration-200 flex flex-col justify-between gap-4"
                  >
                    <div>
                      <h5 className="font-bold text-slate-900 dark:text-slate-100 text-sm">{topic.title}</h5>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1 truncate">
                        {topic.has_roadmap ? "Roadmap tersedia" : "Belum ada roadmap"}
                      </p>
                    </div>
                    <div className="space-y-1.5">
                      <div className="flex justify-between items-center text-[10px] font-semibold text-slate-400 dark:text-slate-500">
                        <span>Progres</span>
                        <span className="text-slate-800 dark:text-slate-200">{topic.progress_percentage}%</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-50 dark:bg-[#334155] rounded-full overflow-hidden">
                        <div className="h-full bg-[#4F8EF7] rounded-full" style={{ width: `${topic.progress_percentage}%` }} />
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {/* AI Recommendations */}
          <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-[#334155]">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#7C5CFF]" />
              <h3 className="text-xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Rekomendasi Belajar AI</h3>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {aiRecommendations.map((rec) => (
                <div key={rec.name} className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-xl p-5 hover:border-[#7C5CFF]/30 transition-all duration-200 flex flex-col justify-between gap-4 group">
                  <div className="space-y-2">
                    <span className="inline-block px-2.5 py-0.5 text-[9px] font-bold text-[#7C5CFF] bg-[#7C5CFF]/8 rounded-full">{rec.tag}</span>
                    <h5 className="font-bold text-slate-900 dark:text-slate-100 text-sm">{rec.name}</h5>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-normal">{rec.reason}</p>
                  </div>
                  <button
                    onClick={() => {
                      setTopicName(rec.name);
                      setShowModal(true);
                    }}
                    className="inline-flex items-center gap-1 text-[11px] font-bold text-[#4F8EF7] hover:text-[#7C5CFF] transition-colors mt-2 text-left"
                  >
                    <span>Buat Peta Belajar</span>
                    <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5 duration-200" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        /* Empty State */
        <div className="flex flex-col items-center justify-center text-center py-20 px-4 space-y-6 animate-in fade-in duration-300">
          <div className="relative flex items-center justify-center w-16 h-16 rounded-full bg-slate-50 dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155]">
            <GraduationCap className="w-8 h-8 text-[#4F8EF7]" />
          </div>
          <div className="space-y-2 max-w-sm">
            <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">Belum ada topik aktif</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
              Mari mulai perjalanan belajarmu. Tentukan topik pertama yang ingin kamu pelajari bersama AI Mentor.
            </p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-50 dark:bg-[#1e293b] hover:bg-slate-100 dark:hover:bg-[#334155] text-xs font-bold text-[#4F8EF7] rounded-xl transition-all duration-300 group border border-slate-100 dark:border-[#334155]"
          >
            <span>Mulai Belajar</span>
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1 duration-200" />
          </button>
        </div>
      )}

      {/* Modal Dialog for Topic Creation */}
      {showModal && (
        <>
          <div className="fixed inset-0 bg-slate-950/40 dark:bg-black/60 backdrop-blur-xs z-50 animate-in fade-in duration-300" onClick={() => setShowModal(false)} />
          <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white dark:bg-[#1e293b] rounded-2xl shadow-xl border border-slate-100 dark:border-[#334155] p-6 w-[90%] max-w-md z-50 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-[#334155]">
              <h3 className="font-bold text-slate-900 dark:text-slate-100 text-base flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-[#4F8EF7]" />
                Topik Belajar Baru
              </h3>
              <button onClick={() => setShowModal(false)} className="p-1 rounded-lg text-slate-400 dark:text-slate-500 hover:bg-slate-50 dark:hover:bg-[#334155] hover:text-slate-600 dark:hover:text-slate-300 transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleCreateTopic} className="mt-4 space-y-4">
              <div className="space-y-1.5">
                <label className="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Apa yang ingin kamu pelajari?</label>
                <input
                  type="text"
                  required
                  value={topicName}
                  onChange={(e) => setTopicName(e.target.value)}
                  placeholder="Contoh: Python Dasar, Machine Learning, Aljabar..."
                  className="w-full px-4 py-3 text-sm bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] focus:border-[#4F8EF7] focus:bg-white dark:focus:bg-[#0f172a] rounded-xl outline-none transition-all text-slate-900 dark:text-slate-200"
                />
              </div>
              <button
                type="submit"
                disabled={creating}
                className="w-full mt-2 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md hover:opacity-90 hover:scale-[1.01] transition-all flex items-center justify-center gap-2"
              >
                {creating && <Loader2 className="w-4 h-4 animate-spin" />}
                Buat Peta Belajar AI (Roadmap)
              </button>
            </form>
          </div>
        </>
      )}
    </div>
  );
}
