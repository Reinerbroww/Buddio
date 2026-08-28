"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { BookOpen, GraduationCap, Sparkles, Loader2 } from "lucide-react";
import api, { ApiError } from "@/services/api";
import { useAuth } from "@/context/AuthContext";
import { BuddioLogo } from "@/components/BuddioLogo";

const GRADE_CONFIGS = [
  {
    key: "sd",
    title: "Elementary School (SD)",
    badge: "Grades 1-6",
    desc: "Visual learning with everyday analogies.",
  },
  {
    key: "smp",
    title: "Middle School (SMP)",
    badge: "Grades 7-9",
    desc: "Structured concepts with engaging analogies.",
  },
  {
    key: "sma",
    title: "High School (SMA)",
    badge: "College / SNBT Prep",
    desc: "Analytical, formulas, and targeted practice.",
  },
  {
    key: "mahasiswa",
    title: "University",
    badge: "Academic & Research",
    desc: "Professional language and critical analysis.",
  },
  {
    key: "self_learner",
    title: "Self Learner / Professional",
    badge: "Skills & Career",
    desc: "Practical, industry-oriented, ready to apply.",
  },
];

export default function OnboardingPage() {
  const router = useRouter();
  const { user, loading, refreshUser } = useAuth();
  const [selected, setSelected] = useState<string | null>(user?.grade_level ?? null);
  const [goal, setGoal] = useState(user?.learning_goal ?? "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [loading, user, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
      </div>
    );
  }

  if (!user) return null;

  const handleFinish = async () => {
    setSaving(true);
    setError(null);
    try {
      if (selected && selected !== user.grade_level) {
        await api.post<{ grade_level: string }>("/onboarding/grade-level", {
          grade_level: selected,
        });
      }
      if (goal.trim() && goal !== user.learning_goal) {
        await api.post<{ goal: string }>("/onboarding/learning-goal", {
          goal: goal.trim(),
        });
      }
      await refreshUser();
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 flex flex-col relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-[420px] bg-gradient-to-b from-[#4F8EF7]/10 via-[#7C5CFF]/5 to-transparent pointer-events-none" />
      <div className="absolute top-16 -left-24 w-72 h-72 bg-[#4F8EF7]/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-16 -right-24 w-72 h-72 bg-[#7C5CFF]/10 rounded-full blur-3xl pointer-events-none" />

      <header className="sticky top-0 z-50 border-b border-slate-100 bg-white/80 backdrop-blur-md">
        <div className="max-w-2xl mx-auto px-4 h-16 flex items-center">
          <BuddioLogo />
        </div>
      </header>

      <main className="flex-1 max-w-2xl w-full mx-auto px-4 py-12 relative z-10 flex flex-col gap-10">
        <div className="text-center space-y-3">
          <div className="mx-auto w-14 h-14 bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] rounded-2xl flex items-center justify-center shadow-md shadow-[#4F8EF7]/20">
            <Sparkles className="h-7 w-7 text-white" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900">
            Which education level fits you best?
          </h1>
          <p className="text-sm text-slate-500 max-w-lg mx-auto leading-relaxed">
            Buddio will adjust the language, difficulty, and teaching style to match the level you
            choose.
          </p>
        </div>

        {error && (
          <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3 text-center">
            {error}
          </div>
        )}

        <div className="flex flex-col gap-3">
          {GRADE_CONFIGS.map((g) => {
            const isActive = selected === g.key;
            return (
              <button
                key={g.key}
                onClick={() => setSelected(g.key)}
                className={`w-full text-left p-4 rounded-2xl border transition-all flex items-center gap-4 ${
                  isActive
                    ? "bg-white border-[#4F8EF7] shadow-md shadow-[#4F8EF7]/10"
                    : "bg-white border-slate-100 hover:border-slate-300"
                }`}
              >
                <div
                  className={`h-10 w-10 rounded-xl flex items-center justify-center shrink-0 transition-colors ${
                    isActive
                      ? "bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white"
                      : "bg-slate-50 text-slate-400"
                  }`}
                >
                  <BookOpen className="h-5 w-5" />
                </div>
                <div className="flex-1">
                  <div className={`text-sm font-bold ${isActive ? "text-slate-900" : "text-slate-700"}`}>
                    {g.title}
                  </div>
                  <div className="text-[11px] text-slate-500">{g.desc}</div>
                </div>
                <div
                  className={`text-[10px] font-bold px-2.5 py-1 rounded-full whitespace-nowrap ${
                    isActive
                      ? "text-[#4F8EF7] bg-[#4F8EF7]/8"
                      : "text-slate-500 bg-slate-50"
                  }`}
                >
                  {g.badge}
                </div>
              </button>
            );
          })}
        </div>

        <div className="bg-white border border-slate-100 rounded-2xl p-5 flex flex-col gap-3 shadow-sm">
          <label className="text-xs font-extrabold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <GraduationCap className="w-4 h-4 text-[#4F8EF7]" /> Your learning goal (optional)
          </label>
          <input
            type="text"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="Example: Prepare for SNBT, become fluent in Python, get into university..."
            className="w-full px-4 py-3 text-sm bg-slate-50 border border-slate-100 text-slate-900 placeholder-slate-400 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all"
          />
        </div>

        <button
          onClick={handleFinish}
          disabled={saving}
          className="w-full py-3.5 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] hover:scale-[1.01] hover:shadow-lg hover:shadow-[#4F8EF7]/20 disabled:opacity-60 disabled:hover:scale-100 text-white font-bold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 transition-all flex items-center justify-center gap-2"
        >
          {saving && <Loader2 className="w-4 h-4 animate-spin" />}
          Continue to Dashboard
        </button>
      </main>
    </div>
  );
}
