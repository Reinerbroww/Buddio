"use client";

import React, { useCallback, useEffect, useState } from "react";
import { Clock, Target, Flame, Zap, Loader2, BookOpen, MessageSquare, Map, FileQuestion } from "lucide-react";
import api, { ApiError } from "@/services/api";
import type { ProgressStat, ProgressItem } from "@/lib/types";
import { useLanguage } from "@/context/LanguageContext";

function formatDuration(minutes: number): string {
  if (minutes >= 60) {
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return m > 0 ? `${h}h ${m}m` : `${h}h`;
  }
  return `${minutes}m`;
}

export default function ProgressPage() {
  const { t } = useLanguage();
  const [stats, setStats] = useState<ProgressStat | null>(null);
  const [items, setItems] = useState<ProgressItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(() => {
    Promise.all([
      api.get<ProgressStat>("/progress/statistics"),
      api.get<ProgressItem[]>("/progress/all"),
    ])
      .then(([s, i]) => {
        setStats(s);
        setItems(i);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? err.message : t("progress.loadFail"));
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
      </div>
    );
  }

  const statCards = [
    { label: t("progress.studyHours"), value: stats?.study_hours ?? 0, icon: Clock, color: "#4F8EF7" },
    { label: t("progress.activeTopics"), value: stats?.topics ?? 0, icon: Target, color: "#7C5CFF" },
    { label: t("progress.streakDays"), value: stats?.streak ?? 0, icon: Flame, color: "#F97316" },
    { label: t("progress.avgProgress"), value: `${stats?.completion ?? 0}%`, icon: Zap, color: "#22C55E" },
  ];

  const quotaChips = [
    { label: t("progress.chat"), value: stats?.chat_remaining ?? 0, icon: MessageSquare, color: "#4F8EF7" },
    { label: t("progress.roadmap"), value: stats?.roadmap_remaining ?? 0, icon: Map, color: "#7C5CFF" },
    { label: t("progress.quiz"), value: stats?.quiz_remaining ?? 0, icon: FileQuestion, color: "#F97316" },
  ];

  return (
    <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      {error && (
        <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
          {error}
        </div>
      )}

      <div className="border-b border-slate-100 pb-8">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight font-sans">
          {t("progress.title")}
        </h2>
        <p className="text-sm sm:text-base text-slate-500 font-sans mt-1.5">
          {t("progress.subtitle")}
        </p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card) => {
          const Icon = card.icon;
          return (
            <div key={card.label} className="bg-white border border-slate-100 rounded-2xl p-4 flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: `${card.color}14`, color: card.color }}>
                <Icon className="w-5 h-5" />
              </div>
              <div className="min-w-0">
                <p className="text-xl font-extrabold text-slate-900 leading-tight">{card.value}</p>
                <p className="text-[11px] text-slate-500 font-medium">{card.label}</p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-gradient-to-r from-[#4F8EF7]/8 to-[#7C5CFF]/8 border border-slate-100 rounded-2xl p-4 flex flex-wrap items-center gap-x-6 gap-y-2">
        <span className="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider">{t("progress.aiQuota")}</span>
        {quotaChips.map((chip) => {
          const Icon = chip.icon;
          return (
            <span key={chip.label} className="inline-flex items-center gap-1.5 text-xs text-slate-600">
              <Icon className="w-3.5 h-3.5" style={{ color: chip.color }} />
              {chip.label}: <b>{t("progress.left", { value: chip.value })}</b>
            </span>
          );
        })}
      </div>

      {items.length > 0 ? (
        <div className="space-y-4">
          <h3 className="text-xs font-extrabold text-slate-400 uppercase tracking-wider">{t("progress.perTopic")}</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {items.map((item) => (
              <div key={item.topic_id} className="bg-white border border-slate-100 rounded-2xl p-5 flex flex-col justify-between gap-4">
                <div className="space-y-2">
                  <div className="flex items-start justify-between gap-4">
                    <h5 className="font-bold text-slate-900 text-sm leading-snug">{item.topic_title}</h5>
                    <span className="text-sm font-extrabold text-slate-900 shrink-0">{item.completion_percentage}%</span>
                  </div>
                  <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] rounded-full transition-all duration-500" style={{ width: `${item.completion_percentage}%` }} />
                  </div>
                </div>
                <div className="flex items-center justify-between gap-4 pt-2 border-t border-slate-50">
                  <span className="text-[11px] text-slate-500 flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-[#4F8EF7]" />
                    {t("progress.studied", { duration: formatDuration(item.study_minutes) })}
                  </span>
                  {item.current_step && (
                    <span className="text-[11px] text-slate-500 truncate flex items-center gap-1.5">
                      <BookOpen className="w-3.5 h-3.5 text-[#7C5CFF] shrink-0" />
                      <span className="truncate">{item.current_step}</span>
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center text-center py-20 px-4 space-y-6 animate-in fade-in duration-300">
          <div className="relative flex items-center justify-center w-16 h-16 rounded-full bg-slate-50 border border-slate-100">
            <BookOpen className="w-8 h-8 text-[#4F8EF7]" />
          </div>
          <div className="space-y-2 max-w-sm">
            <h3 className="text-base font-bold text-slate-900">{t("progress.emptyTitle")}</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              {t("progress.emptyDesc")}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
