"use client";

import { useState } from "react";
import { CheckCircle2, HelpCircle, Lightbulb, ListChecks, Footprints, Scale, Zap } from "lucide-react";
import { useLanguage } from "@/context/LanguageContext";

export type FollowUpKind = "jelaskan" | "contoh" | "langkah" | "analogi" | "dalam";

interface UnderstandingCheckProps {
  stepTitle?: string | null;
  topicTitle?: string | null;
  onAsk: (prompt: string) => void;
}

export default function UnderstandingCheck({ stepTitle, topicTitle, onAsk }: UnderstandingCheckProps) {
  const { t } = useLanguage();
  const [state, setState] = useState<"idle" | "understood" | "confused">("idle");

  const followUps: { kind: FollowUpKind; label: string; icon: React.ReactNode; prompt: string }[] = [
    { kind: "jelaskan", label: t("materi.followJelaskan"), icon: <Lightbulb className="w-3.5 h-3.5" />, prompt: t("materi.promptJelaskan") },
    { kind: "contoh", label: t("materi.followContoh"), icon: <ListChecks className="w-3.5 h-3.5" />, prompt: t("materi.promptContoh") },
    { kind: "langkah", label: t("materi.followLangkah"), icon: <Footprints className="w-3.5 h-3.5" />, prompt: t("materi.promptLangkah") },
    { kind: "analogi", label: t("materi.followAnalogi"), icon: <Zap className="w-3.5 h-3.5" />, prompt: t("materi.promptAnalogi") },
    { kind: "dalam", label: t("materi.followDalam"), icon: <Scale className="w-3.5 h-3.5" />, prompt: t("materi.promptDalam") },
  ];

  const ctx = `Saya sedang mempelajari materi "${stepTitle ?? ""}" dalam topik "${topicTitle ?? ""}". `;

  const handleFollow = (p: string) => {
    onAsk(ctx + p);
  };

  return (
    <div className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-5 sm:p-6">
      <div className="flex items-center gap-2.5 mb-4">
        <div className="w-9 h-9 rounded-xl bg-[#22C55E]/10 flex items-center justify-center">
          <HelpCircle className="w-5 h-5 text-[#16A34A]" />
        </div>
        <div>
          <h3 className="font-extrabold text-slate-900 dark:text-slate-100 text-sm">{t("materi.checkTitle")}</h3>
          <p className="text-[11px] text-slate-400 dark:text-slate-500">{t("materi.checkDesc")}</p>
        </div>
      </div>

      {state === "idle" && (
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => setState("understood")}
            className="flex flex-col items-center gap-1.5 py-4 rounded-xl border-2 border-emerald-500/30 bg-emerald-50/70 dark:bg-emerald-500/10 hover:bg-emerald-100 dark:hover:bg-emerald-500/20 transition-all cursor-pointer"
          >
            <CheckCircle2 className="w-5 h-5 text-[#16A34A]" />
            <span className="text-xs font-bold text-emerald-700 dark:text-emerald-300">{t("materi.iUnderstand")}</span>
          </button>
          <button
            onClick={() => { setState("confused"); }}
            className="flex flex-col items-center gap-1.5 py-4 rounded-xl border-2 border-rose-500/30 bg-rose-50/70 dark:bg-rose-500/10 hover:bg-rose-100 dark:hover:bg-rose-500/20 transition-all cursor-pointer"
          >
            <HelpCircle className="w-5 h-5 text-rose-500" />
            <span className="text-xs font-bold text-rose-600 dark:text-rose-300">{t("materi.imConfused")}</span>
          </button>
        </div>
      )}

      {state === "understood" && (
        <div className="text-center space-y-3">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-50 dark:bg-emerald-500/10 rounded-full text-emerald-700 dark:text-emerald-300 text-xs font-semibold">
            <CheckCircle2 className="w-4 h-4" /> {t("materi.greatJob")}
          </div>
          <div className="flex items-center justify-center gap-2">
            <button onClick={() => setState("idle")} className="text-[11px] font-semibold text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 transition-colors cursor-pointer">
              {t("materi.markAgain")}
            </button>
          </div>
        </div>
      )}

      {state === "confused" && (
        <div className="space-y-3">
          <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{t("materi.confusedPrompt")}</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {followUps.map((f) => (
              <button
                key={f.kind}
                onClick={() => handleFollow(f.prompt)}
                className="flex items-center gap-2 px-3 py-2.5 rounded-xl border border-slate-200 dark:border-[#334155] bg-slate-50 dark:bg-[#0f172a] hover:border-[#4F8EF7]/40 hover:bg-[#4F8EF7]/5 text-left transition-all cursor-pointer"
              >
                <span className="text-[#4F8EF7] dark:text-[#60a5fa] shrink-0">{f.icon}</span>
                <span className="text-[11px] font-semibold text-slate-700 dark:text-slate-200">{f.label}</span>
              </button>
            ))}
          </div>
          <div className="flex items-center justify-center gap-2">
            <button onClick={() => setState("idle")} className="text-[11px] font-semibold text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 transition-colors cursor-pointer">
              {t("materi.markAgain")}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
