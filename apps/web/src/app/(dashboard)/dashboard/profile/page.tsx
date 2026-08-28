"use client";

import React, { useState } from "react";
import { Loader2, Mail, Target, UserRound } from "lucide-react";
import api, { ApiError } from "@/services/api";
import { useAuth } from "@/context/AuthContext";
import { useLanguage } from "@/context/LanguageContext";
import type { User } from "@/lib/types";

const GRADE_LABELS: Record<string, string> = {
  sd: "Elementary",
  smp: "Middle School",
  sma: "High School",
  mahasiswa: "College",
  self_learner: "Self Learner",
};

export default function ProfilePage() {
  const { user, loading } = useAuth();
  const { t } = useLanguage();

  if (loading || !user) {
    return (
      <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
        <div className="flex items-center justify-center py-24">
          <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
        </div>
      </div>
    );
  }

  const displayName = user.full_name || user.email.split("@")[0] || t("profile.learner");
  const initials = displayName
    .split(/\s+/)
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
  const gradeLabel = user.grade_level ? GRADE_LABELS[user.grade_level] : null;

  return (
    <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      <div className="border-b border-slate-100 pb-8">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight font-sans">
          {t("profile.title")}
        </h2>
        <p className="text-sm sm:text-base text-slate-500 font-sans mt-1.5">
          {t("profile.subtitle")}
        </p>
      </div>

      <div className="bg-white border border-slate-100 rounded-2xl p-6 sm:p-8 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center gap-6">
          <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] flex items-center justify-center text-white text-2xl sm:text-3xl font-extrabold shrink-0 shadow-md shadow-[#4F8EF7]/15">
            {initials}
          </div>
          <div className="min-w-0 flex-1 space-y-2">
            <div className="flex flex-wrap items-center gap-3">
              <h3 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {displayName}
              </h3>
              {gradeLabel && (
                <span className="inline-block px-2.5 py-0.5 text-[10px] font-bold text-[#7C5CFF] bg-[#7C5CFF]/8 rounded-full border border-[#7C5CFF]/15">
                  {gradeLabel}
                </span>
              )}
            </div>
            <p className="text-sm text-slate-500 flex items-center gap-1.5">
              <Mail className="w-4 h-4 shrink-0" />
              {user.email}
            </p>
            {user.learning_goal && (
              <p className="text-xs text-slate-500 flex items-start gap-1.5 leading-relaxed">
                <Target className="w-4 h-4 shrink-0 mt-0.5" />
                {user.learning_goal}
              </p>
            )}
          </div>
        </div>
      </div>

      <div className="bg-white border border-slate-100 rounded-2xl p-6 sm:p-8 shadow-xs">
        <div className="flex items-center gap-2 pb-5 border-b border-slate-100">
          <UserRound className="w-4 h-4 text-[#4F8EF7]" />
          <h3 className="text-xs font-extrabold text-slate-400 uppercase tracking-wider">
            {t("profile.editProfile")}
          </h3>
        </div>
        <ProfileForm key={user.id} user={user} />
      </div>
    </div>
  );
}

function ProfileForm({ user }: { user: User }) {
  const { refreshUser } = useAuth();
  const { t } = useLanguage();
  const [fullName, setFullName] = useState(user.full_name ?? "");
  const [learningGoal, setLearningGoal] = useState(user.learning_goal ?? "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      const payload: { full_name?: string; learning_goal?: string } = {};
      if (fullName.trim()) payload.full_name = fullName.trim();
      if (learningGoal.trim()) payload.learning_goal = learningGoal.trim();
      await api.put<User>("/users/me", payload);
      await refreshUser();
      setSuccess(t("profile.saveSuccess"));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("profile.saveFail"));
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      {success && (
        <div className="text-xs bg-emerald-50 border border-emerald-200 text-emerald-600 rounded-xl px-4 py-3">
          {success}
        </div>
      )}
      {error && (
        <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="mt-6 space-y-5">
        <div className="space-y-1.5">
          <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
            {t("profile.fullName")}
          </label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder={t("profile.fullNamePlaceholder")}
            className="w-full px-4 py-3 text-sm bg-slate-50 border border-slate-100 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all"
          />
        </div>
        <div className="space-y-1.5">
          <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
            {t("profile.learningGoal")}
          </label>
          <input
            type="text"
            value={learningGoal}
            onChange={(e) => setLearningGoal(e.target.value)}
            placeholder={t("profile.learningGoalPlaceholder")}
            className="w-full px-4 py-3 text-sm bg-slate-50 border border-slate-100 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all"
          />
        </div>
        <button
          type="submit"
          disabled={saving}
          className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg transition-all duration-300 disabled:opacity-60 disabled:hover:scale-100 cursor-pointer"
        >
          {saving && <Loader2 className="w-4 h-4 animate-spin" />}
          {t("profile.saveChanges")}
        </button>
      </form>
    </>
  );
}
