"use client";

import { useCallback, useEffect, useState } from "react";
import {
  Sparkles,
  BookOpen,
  ListChecks,
  FileQuestion,
  CheckCircle2,
  Check,
  X,
  ArrowLeft,
  Loader2,
  AlertCircle,
  Play,
  RotateCcw,
  ChevronDown,
  Trophy,
  Target,
  Smile,
} from "lucide-react";
import api, { ApiError } from "@/services/api";
import type { Quiz, QuizAttemptResult, Topic } from "@/lib/types";
import { useLanguage } from "@/context/LanguageContext";

type View = "list" | "taking" | "result";

function optionText(quiz: Quiz, questionId: number, optionIndex: number | null): string | null {
  if (optionIndex === null || optionIndex === undefined) return null;
  const question = quiz.questions.find((q) => q.id === questionId);
  const options = question?.options ?? [];
  if (optionIndex < 0 || optionIndex >= options.length) return null;
  return options[optionIndex] ?? null;
}

export default function AssessmentPage() {
  const { t } = useLanguage();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopicId, setSelectedTopicId] = useState<number | null>(null);
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loadingTopics, setLoadingTopics] = useState(true);
  const [loadingQuizzes, setLoadingQuizzes] = useState(false);
  const [view, setView] = useState<View>("list");
  const [activeQuiz, setActiveQuiz] = useState<Quiz | null>(null);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [result, setResult] = useState<QuizAttemptResult | null>(null);
  const [generating, setGenerating] = useState(false);
  const [quotaExceeded, setQuotaExceeded] = useState(false);
  const [quotaMessage, setQuotaMessage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadQuizzes = useCallback((topicId: number) => {
    setLoadingQuizzes(true);
    api
      .get<Quiz[]>(`/quiz/topic/${topicId}`)
      .then((data) => setQuizzes(data))
      .catch((err) => {
        setQuizzes([]);
        setError(err instanceof ApiError ? err.message : t("assessment.loadQuizzesFail"));
      })
      .finally(() => setLoadingQuizzes(false));
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await api.get<Topic[]>("/topics");
        if (cancelled) return;
        setTopics(data);
        if (data.length > 0) setSelectedTopicId(data[0].id);
      } catch (err) {
        if (cancelled) return;
        setError(err instanceof ApiError ? err.message : t("assessment.loadTopicsFail"));
      } finally {
        if (!cancelled) setLoadingTopics(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (selectedTopicId == null) return;
    let cancelled = false;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- loading state before async is fine
    setLoadingQuizzes(true);
    api
      .get<Quiz[]>(`/quiz/topic/${selectedTopicId}`)
      .then((data) => { if (!cancelled) setQuizzes(data); })
      .catch((err) => {
        if (!cancelled) {
          setQuizzes([]);
          setError(err instanceof ApiError ? err.message : t("assessment.loadQuizzesFail"));
        }
      })
      .finally(() => { if (!cancelled) setLoadingQuizzes(false); });
    return () => { cancelled = true; };
  }, [selectedTopicId]);

  const activeQuestions = activeQuiz?.questions ?? [];
  const answeredCount = activeQuestions.filter((q) => answers[q.id] !== undefined).length;
  const allAnswered = activeQuestions.length > 0 && answeredCount === activeQuestions.length;
  const progressPercent = activeQuestions.length > 0 ? (answeredCount / activeQuestions.length) * 100 : 0;
  const percent = result && result.total > 0 ? Math.round((result.score / result.total) * 100) : 0;

  const startQuiz = useCallback((quiz: Quiz) => {
    setActiveQuiz(quiz);
    setAnswers({});
    setResult(null);
    setError(null);
    setView("taking");
  }, []);

  const handleSelect = useCallback((questionId: number, optionIndex: number) => {
    setAnswers((prev) => ({ ...prev, [questionId]: optionIndex }));
  }, []);

  const handleGenerate = async () => {
    if (!selectedTopicId || generating) return;
    setGenerating(true);
    setError(null);
    setQuotaExceeded(false);
    setQuotaMessage(null);
    try {
      const quiz = await api.post<Quiz>("/quiz/generate", { topic_id: selectedTopicId, count: 5 });
      startQuiz(quiz);
    } catch (err) {
      if (err instanceof ApiError && err.status === 429) {
        setQuotaExceeded(true);
        setQuotaMessage(err.message);
      } else {
        setError(err instanceof ApiError ? err.message : t("assessment.newQuizFail"));
      }
    } finally {
      setGenerating(false);
    }
  };

  const handleSubmit = async () => {
    if (!activeQuiz || submitting || !allAnswered) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await api.post<QuizAttemptResult>(`/quiz/${activeQuiz.id}/submit`, { answers });
      setResult(res);
      setView("result");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("assessment.submitFail"));
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetake = useCallback(() => {
    if (!activeQuiz) return;
    setAnswers({});
    setResult(null);
    setError(null);
    setView("taking");
  }, [activeQuiz]);

  const handleBackToList = useCallback(() => {
    setView("list");
    setActiveQuiz(null);
    setResult(null);
    setAnswers({});
    setError(null);
    if (selectedTopicId != null) loadQuizzes(selectedTopicId);
  }, [selectedTopicId, loadQuizzes]);

  if (loadingTopics) {
    return (
      <div className="flex items-center justify-center py-24">
        <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      {error && view !== "result" && (
        <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
          {error}
        </div>
      )}

      {view === "list" && (
        <div className="space-y-8 animate-in fade-in duration-300">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6 border-b border-slate-100 dark:border-[#334155] pb-8">
            <div className="space-y-1.5">
              <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight font-sans">
                {t("assessment.listTitle")}
              </h2>
              <p className="text-sm sm:text-base text-slate-500 dark:text-slate-400 font-sans">
                {t("assessment.listDesc")}
              </p>
            </div>
            <div className="shrink-0">
              <button
                onClick={handleGenerate}
                disabled={!selectedTopicId || generating || quotaExceeded}
                className={`w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 text-white font-semibold text-sm rounded-xl shadow-md transition-all duration-300 group cursor-pointer ${
                  !selectedTopicId || generating || quotaExceeded
                    ? "bg-slate-300 shadow-none cursor-not-allowed"
                    : "bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg hover:shadow-[#4F8EF7]/20"
                }`}
              >
                {generating ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Sparkles className="w-5 h-5 transition-transform group-hover:rotate-12 duration-300" />
                )}
                <span>
                  {quotaExceeded ? t("assessment.quotaDailyExhausted") : generating ? t("assessment.generatingQuiz") : t("assessment.newQuizBtn")}
                </span>
              </button>
            </div>
          </div>

          {quotaExceeded && quotaMessage && (
            <div className="flex items-center gap-2 text-xs bg-amber-50 border border-amber-200 text-amber-700 rounded-xl px-4 py-3">
              <AlertCircle className="w-4 h-4 shrink-0" />
              {quotaMessage}
            </div>
          )}

          {topics.length === 0 ? (
            <div className="flex flex-col items-center justify-center text-center py-20 px-4 space-y-4">
              <div className="w-16 h-16 rounded-full bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] flex items-center justify-center">
                <BookOpen className="w-8 h-8 text-[#4F8EF7]" />
              </div>
              <div className="space-y-1.5 max-w-sm">
                <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">{t("assessment.noTopicsTitle")}</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  {t("assessment.noTopicsDesc")}
                </p>
              </div>
            </div>
          ) : (
            <>
              <div className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-4 sm:p-5 space-y-2.5">
                <label className="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-[#4F8EF7]" />
                  {t("assessment.pickTopic")}
                </label>
                <div className="relative">
                  <select
                    value={selectedTopicId ?? ""}
                    onChange={(e) => setSelectedTopicId(Number(e.target.value))}
                    className="w-full px-4 py-3 pr-10 text-sm bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] focus:border-[#4F8EF7] focus:bg-white dark:focus:bg-[#0f172a] rounded-xl outline-none transition-all text-slate-900 dark:text-slate-100 appearance-none"
                  >
                    {topics.map((topic) => (
                      <option key={topic.id} value={topic.id}>
                        {topic.title}
                      </option>
                    ))}
                  </select>
                  <ChevronDown className="absolute right-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 dark:text-slate-500 pointer-events-none" />
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="text-xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                  <ListChecks className="w-4 h-4 text-[#4F8EF7]" />
                  {t("assessment.quizList", { count: quizzes.length })}
                </h3>

                {loadingQuizzes ? (
                  <div className="flex items-center justify-center py-12">
                    <Loader2 className="w-6 h-6 text-[#4F8EF7] animate-spin" />
                  </div>
                ) : quizzes.length === 0 ? (
                  <div className="flex flex-col items-center justify-center text-center py-16 px-4 space-y-4">
                    <div className="w-14 h-14 rounded-full bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] flex items-center justify-center">
                      <FileQuestion className="w-7 h-7 text-[#4F8EF7]" />
                    </div>
                    <div className="space-y-1.5 max-w-sm">
                      <h4 className="font-bold text-slate-900 dark:text-slate-100 text-sm">{t("assessment.noQuizTitle")}</h4>
                      <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                        {t("assessment.noQuizDesc")}
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {quizzes.map((quiz) => (
                      <button
                        key={quiz.id}
                        onClick={() => startQuiz(quiz)}
                        className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-5 text-left hover:border-[#4F8EF7]/30 hover:shadow-md transition-all duration-200 group cursor-pointer"
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div className="min-w-0">
                            <h5 className="font-bold text-slate-900 dark:text-slate-100 text-sm leading-snug">{quiz.title}</h5>
                            <div className="flex items-center gap-2 mt-2 flex-wrap">
                              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 text-[9px] font-bold text-[#4F8EF7] bg-[#4F8EF7]/8 rounded-full">
                                <FileQuestion className="w-3 h-3" />
                                {t("assessment.questions", { count: quiz.questions.length })}
                              </span>
                              {quiz.mode === "mock" && (
                                <span className="inline-flex items-center px-2.5 py-0.5 text-[9px] font-bold text-amber-600 bg-amber-50 border border-amber-200 rounded-full">
                                  {t("assessment.demoMode")}
                                </span>
                              )}
                            </div>
                          </div>
                          <span className="w-9 h-9 rounded-xl bg-[#4F8EF7]/10 text-[#4F8EF7] flex items-center justify-center shrink-0 transition-colors group-hover:bg-gradient-to-r group-hover:from-[#4F8EF7] group-hover:to-[#7C5CFF] group-hover:text-white">
                            <Play className="w-4 h-4" />
                          </span>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      )}

      {view === "taking" && activeQuiz && (
        <div className="space-y-6 animate-in fade-in duration-300">
          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 border-b border-slate-100 dark:border-[#334155] pb-6">
            <div className="space-y-2">
              <button
                onClick={handleBackToList}
                className="inline-flex items-center gap-1.5 text-[11px] font-bold text-slate-400 dark:text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors cursor-pointer"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                {t("assessment.backToList")}
              </button>
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">
                  {activeQuiz.title}
                </h2>
                {activeQuiz.mode === "mock" && (
                  <span className="inline-flex items-center px-2.5 py-0.5 text-[9px] font-bold text-amber-600 bg-amber-50 border border-amber-200 rounded-full">
                    {t("assessment.demoMode")}
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">{t("assessment.takingDesc")}</p>
            </div>
            <span className="shrink-0 inline-flex items-center gap-1.5 text-xs font-bold text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] rounded-xl px-3 py-2">
              <CheckCircle2 className="w-4 h-4 text-[#22C55E]" />
              {t("assessment.answered", { answered: answeredCount, total: activeQuiz.questions.length })}
            </span>
          </div>

          <div className="h-2 w-full bg-slate-100 dark:bg-[#334155] rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] rounded-full transition-all duration-500"
              style={{ width: `${progressPercent}%` }}
            />
          </div>

          <div className="space-y-6">
            {activeQuiz.questions.map((q, idx) => (
              <div key={q.id} className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-5 sm:p-6">
                <div className="flex items-start gap-3">
                  <span className="shrink-0 w-7 h-7 rounded-lg bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white text-xs font-bold flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <p className="font-semibold text-slate-900 dark:text-slate-100 text-sm sm:text-base leading-relaxed pt-0.5">
                    {q.question}
                  </p>
                </div>
                <div className="mt-4 space-y-2 pl-10">
                  {(q.options ?? []).map((opt, optIdx) => {
                    const selected = answers[q.id] === optIdx;
                    return (
                      <label
                        key={optIdx}
                        className={`flex items-center gap-3 px-4 py-3 rounded-xl border cursor-pointer transition-all duration-200 ${
                          selected
                            ? "border-[#4F8EF7] bg-[#4F8EF7]/8 shadow-sm shadow-[#4F8EF7]/10"
                            : "border-slate-100 dark:border-[#334155] bg-white dark:bg-[#0f172a] hover:border-slate-300 dark:hover:border-[#334155] hover:bg-slate-50 dark:hover:bg-[#334155]"
                        }`}
                      >
                        <input
                          type="radio"
                          name={`quiz-q-${q.id}`}
                          checked={selected}
                          onChange={() => handleSelect(q.id, optIdx)}
                          className="sr-only"
                        />
                        <span
                          className={`shrink-0 w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors ${
                            selected ? "border-[#4F8EF7] bg-[#4F8EF7]" : "border-slate-300 dark:border-[#334155]"
                          }`}
                        >
                          {selected && <span className="w-2 h-2 rounded-full bg-white" />}
                        </span>
                        <span className="text-sm text-slate-700 dark:text-slate-300">{opt}</span>
                      </label>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          <div className="sticky bottom-4 bg-white/90 dark:bg-[#1e293b]/90 backdrop-blur-sm border border-slate-100 dark:border-[#334155] rounded-2xl p-4 flex flex-col sm:flex-row items-center gap-3 shadow-xs">
            <div className="flex-1 text-xs text-slate-500 dark:text-slate-400">
              {allAnswered ? (
                <span className="font-semibold text-emerald-600 inline-flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" />
                  {t("assessment.allAnswered")}
                </span>
              ) : (
                <span>
                  {t("assessment.unansweredLeft", { count: activeQuiz.questions.length - answeredCount })}
                </span>
              )}
            </div>
            <button
              onClick={handleSubmit}
              disabled={!allAnswered || submitting}
              className={`w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 text-white font-semibold text-sm rounded-xl transition-all duration-300 ${
                allAnswered && !submitting
                  ? "bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg cursor-pointer"
                  : "bg-slate-200 cursor-not-allowed"
              }`}
            >
              {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
              {t("assessment.submitAnswers")}
            </button>
          </div>
        </div>
      )}

      {view === "result" && activeQuiz && result && (
        <div className="space-y-8 animate-in fade-in duration-300">
          <div className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-6 sm:p-8">
            <div className="flex flex-col items-center text-center space-y-5">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white flex items-center justify-center shadow-lg shadow-[#4F8EF7]/20">
                {percent >= 80 ? <Trophy className="w-9 h-9" /> : percent >= 50 ? <Smile className="w-9 h-9" /> : <Target className="w-9 h-9" />}
              </div>
              <div className="space-y-1.5">
                <div className="flex items-center justify-center gap-2 flex-wrap">
                  <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">
                    {t("assessment.score", { score: result.score, total: result.total, percent })}
                  </h2>
                  {activeQuiz.mode === "mock" && (
                    <span className="inline-flex items-center px-2.5 py-0.5 text-[9px] font-bold text-amber-600 bg-amber-50 border border-amber-200 rounded-full">
                      {t("assessment.demoMode")}
                    </span>
                  )}
                </div>
                {result.feedback && (
                  <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-md mx-auto">{result.feedback}</p>
                )}
              </div>
            </div>

            <div className="mt-6 grid grid-cols-2 gap-4 max-w-sm mx-auto">
              <div className="bg-emerald-50 border border-emerald-100 rounded-2xl p-4 text-center">
                <p className="text-2xl font-extrabold text-emerald-600">{result.score}</p>
                <p className="text-[11px] font-semibold text-emerald-600/80">{t("assessment.correct")}</p>
              </div>
              <div className="bg-rose-50 border border-rose-100 rounded-2xl p-4 text-center">
                <p className="text-2xl font-extrabold text-rose-500">{result.total - result.score}</p>
                <p className="text-[11px] font-semibold text-rose-500/80">{t("assessment.wrong")}</p>
              </div>
            </div>

            <div className="mt-8 flex flex-col sm:flex-row gap-3 justify-center">
              <button
                onClick={handleRetake}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg transition-all duration-300 cursor-pointer"
              >
                <RotateCcw className="w-4 h-4" />
                {t("assessment.retake")}
              </button>
              <button
                onClick={handleBackToList}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 bg-white dark:bg-[#0f172a] border border-slate-200 dark:border-[#334155] text-slate-700 dark:text-slate-200 font-semibold text-sm rounded-xl hover:bg-slate-50 dark:hover:bg-[#334155] hover:border-slate-300 transition-all duration-300 cursor-pointer"
              >
                <ArrowLeft className="w-4 h-4" />
                {t("assessment.backToList")}
              </button>
            </div>
          </div>

          {result.details && result.details.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-xs font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                <ListChecks className="w-4 h-4 text-[#4F8EF7]" />
                {t("assessment.reviewAnswers")}
              </h3>
              <div className="space-y-4">
                {result.details.map((d, idx) => {
                  const yourText = optionText(activeQuiz, d.question_id, d.your_answer);
                  const correctText = optionText(activeQuiz, d.question_id, d.correct_answer);
                  return (
                    <div
                      key={d.question_id}
                      className={`border rounded-2xl p-5 sm:p-6 ${
                        d.correct ? "border-emerald-200 bg-emerald-50/60" : "border-rose-200 bg-rose-50/60"
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <span
                          className={`shrink-0 w-7 h-7 rounded-lg flex items-center justify-center ${
                            d.correct ? "bg-emerald-100 text-emerald-600" : "bg-rose-100 text-rose-600"
                          }`}
                        >
                          {d.correct ? <Check className="w-4 h-4" /> : <X className="w-4 h-4" />}
                        </span>
                        <div className="space-y-3 min-w-0 flex-1">
                          <p className="font-semibold text-slate-900 dark:text-slate-100 text-sm leading-relaxed pt-0.5">
                            {idx + 1}. {d.question}
                          </p>
                          <div className="space-y-1.5 text-xs">
                            {d.your_answer !== null && yourText && (
                              <p className={d.correct ? "text-emerald-700" : "text-rose-700"}>
                                {t("assessment.yourAnswer")} <b>{yourText}</b>
                              </p>
                            )}
                            {!d.correct && (
                              <p className="text-emerald-700">
                                {t("assessment.correctAnswer")} <b>{correctText ?? t("assessment.unknownAnswer")}</b>
                              </p>
                            )}
                          </div>
                          {d.explanation && (
                            <div className="text-xs bg-white/80 dark:bg-[#0f172a]/80 border border-slate-100 dark:border-[#334155] rounded-xl px-3.5 py-2.5 text-slate-600 dark:text-slate-300 leading-relaxed">
                              <span className="font-bold text-slate-500 dark:text-slate-400">{t("assessment.explanation")}</span>
                              {d.explanation}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {generating && (
        <>
          <div className="fixed inset-0 bg-slate-950/40 backdrop-blur-xs z-50 animate-in fade-in duration-300" />
          <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white dark:bg-[#1e293b] rounded-2xl shadow-xl border border-slate-100 dark:border-[#334155] p-8 w-[90%] max-w-sm z-50 animate-in fade-in zoom-in-95 duration-200 text-center space-y-4">
            <div className="mx-auto w-14 h-14 rounded-full bg-[#4F8EF7]/10 flex items-center justify-center">
              <Loader2 className="w-7 h-7 text-[#4F8EF7] animate-spin" />
            </div>
            <div className="space-y-1.5">
              <h3 className="font-bold text-slate-900 dark:text-slate-100 text-base">{t("assessment.generatingModalTitle")}</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                {t("assessment.generatingModalDesc")}
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
