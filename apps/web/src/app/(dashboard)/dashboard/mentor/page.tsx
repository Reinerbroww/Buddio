"use client";

import React, { Suspense, useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Send, Sparkles, Trash2, Loader2, GraduationCap, ArrowRight } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import api, { ApiError } from "@/services/api";
import type { ChatHistory, ChatMessageItem, ChatResponse, Topic } from "@/lib/types";

const GREETING = "Halo! Aku Kak Buddio, mentor belajarmu. Mau tanya apa hari ini?";

function BuddioAvatar({ className = "w-7 h-7 text-[10px]" }: { className?: string }) {
  return (
    <div
      className={`${className} rounded-full bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white font-bold flex items-center justify-center shrink-0 select-none`}
    >
      B
    </div>
  );
}

function MentorPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const topicParam = searchParams.get("topic");

  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopicId, setSelectedTopicId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessageItem[]>([]);
  const [input, setInput] = useState("");
  const [remaining, setRemaining] = useState<number | null>(null);
  const [lastMode, setLastMode] = useState<string | null>(null);
  const [loadingTopics, setLoadingTopics] = useState(true);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [sending, setSending] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const loadTopics = useCallback(() => {
    api
      .get<Topic[]>("/topics")
      .then((t) => {
        setTopics(t);
        if (t.length === 0) {
          setSelectedTopicId(null);
          setMessages([]);
        } else {
          const fromParam = topicParam ? t.find((x) => String(x.id) === topicParam) : undefined;
          setSelectedTopicId(fromParam ? fromParam.id : t[0].id);
        }
      })
      .catch((err) => {
        setError(err instanceof ApiError ? err.message : "Gagal memuat topik.");
      })
      .finally(() => setLoadingTopics(false));
  }, [topicParam]);

  useEffect(() => {
    loadTopics();
  }, [loadTopics]);

  const loadHistory = useCallback((topicId: number) => {
    setLoadingHistory(true);
    api
      .get<ChatHistory[]>(`/mentor/history/${topicId}`)
      .then((history) => {
        const sorted = [...history].sort((a, b) => a.id - b.id);
        const latest = sorted.length > 0 ? sorted[sorted.length - 1] : null;
        setMessages(latest ? latest.messages : []);
      })
      .catch((err) => {
        setError(err instanceof ApiError ? err.message : "Gagal memuat riwayat chat.");
        setMessages([]);
      })
      .finally(() => setLoadingHistory(false));
  }, []);

  useEffect(() => {
    if (selectedTopicId == null) return;
    loadHistory(selectedTopicId);
  }, [selectedTopicId, loadHistory]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, sending, loadingHistory]);

  const handleSend = useCallback(async (overrideText?: string) => {
    const text = (overrideText !== undefined ? overrideText : input).trim();
    if (!text || sending || selectedTopicId == null || remaining === 0) return;
    const tempId = Date.now();
    const userMsg: ChatMessageItem = {
      id: tempId,
      role: "user",
      message: text,
      created_at: new Date().toISOString(),
    };
    setMessages((m) => [...m, userMsg]);
    if (overrideText === undefined) {
      setInput("");
    }
    setError(null);
    setSending(true);
    try {
      const res = await api.post<ChatResponse>("/mentor/chat", {
        topic_id: selectedTopicId,
        message: text,
      });
      const assistantMsg: ChatMessageItem = {
        id: tempId + 1,
        role: "assistant",
        message: res.answer,
        created_at: new Date().toISOString(),
      };
      setMessages((m) => [...m, assistantMsg]);
      setRemaining(res.remaining);
      setLastMode(res.mode);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.status === 429 ? err.message || "Sisa kuota chat hari ini sudah habis." : err.message);
        if (err.status === 429) setRemaining(0);
      } else {
        setError("Gagal mengirim pesan.");
      }
      setMessages((m) => m.filter((msg) => msg.id !== tempId));
      if (overrideText === undefined) {
        setInput(text);
      }
    } finally {
      setSending(false);
    }
  }, [input, sending, selectedTopicId, remaining]);

  const hasAutoSent = useRef(false);

  useEffect(() => {
    const promptParam = searchParams.get("prompt");
    if (promptParam && selectedTopicId != null && !loadingTopics && !loadingHistory && !hasAutoSent.current) {
      hasAutoSent.current = true;
      
      const params = new URLSearchParams(window.location.search);
      params.delete("prompt");
      router.replace(`?${params.toString()}`);
      
      handleSend(promptParam);
    }
  }, [selectedTopicId, loadingTopics, loadingHistory, searchParams, router, handleSend]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleDeleteHistory = async () => {
    if (selectedTopicId == null || deleting) return;
    setDeleting(true);
    setError(null);
    try {
      await api.delete(`/mentor/history/${selectedTopicId}`);
      setMessages([]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Gagal menghapus riwayat.");
    } finally {
      setDeleting(false);
    }
  };

  if (loadingTopics) {
    return (
      <div className="max-w-4xl mx-auto py-6 sm:py-8 animate-in fade-in duration-300">
        <div className="flex items-center justify-center py-24">
          <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
        </div>
      </div>
    );
  }

  if (topics.length === 0) {
    return (
      <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
        {error && (
          <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
            {error}
          </div>
        )}
        <div className="flex flex-col items-center justify-center text-center py-20 px-4 space-y-6 animate-in fade-in duration-300 bg-white border border-slate-100 rounded-2xl">
          <div className="relative flex items-center justify-center w-16 h-16 rounded-full bg-slate-50 border border-slate-100">
            <GraduationCap className="w-8 h-8 text-[#4F8EF7]" />
          </div>
          <div className="space-y-2 max-w-sm">
            <h3 className="text-base font-bold text-slate-900">Belum ada topik belajar</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Kamu perlu membuat topik belajar dulu sebelum bisa bertanya pada AI Mentor Buddio.
            </p>
          </div>
          <Link
            href="/dashboard/topik"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white text-xs font-bold rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.02] transition-all duration-300 group"
          >
            <span>Buat Topik Belajar</span>
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1 duration-200" />
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      <div className="flex items-center gap-3 border-b border-slate-100 pb-6">
        <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white flex items-center justify-center shadow-md shadow-[#4F8EF7]/15 shrink-0">
          <Sparkles className="w-5 h-5" />
        </div>
        <div className="space-y-0.5">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight font-sans">
            Mentor AI Buddio
          </h2>
          <p className="text-sm text-slate-500 font-sans">
            Tanya apa saja, Kak Buddio siap membantu belajarmu.
          </p>
        </div>
      </div>

      {error && (
        <div className="text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
          {error}
        </div>
      )}

      <div className="bg-white border border-slate-100 rounded-2xl p-4 sm:p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div className="space-y-1.5 min-w-0">
          <label htmlFor="topic-select" className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
            Pilih Topik
          </label>
          <select
            id="topic-select"
            value={selectedTopicId ?? ""}
            onChange={(e) => setSelectedTopicId(Number(e.target.value))}
            className="w-full sm:w-72 px-4 py-2.5 text-sm bg-slate-50 border border-slate-100 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all text-slate-800 cursor-pointer"
          >
            {topics.map((t) => (
              <option key={t.id} value={t.id}>
                {t.title}
              </option>
            ))}
          </select>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          {remaining !== null && (
            <span className="text-xs text-slate-600 bg-slate-50 border border-slate-100 rounded-full px-3 py-1.5">
              Sisa kuota chat hari ini: <b className="text-slate-900">{remaining}</b>
            </span>
          )}
          {lastMode === "mock" && (
            <span className="text-[10px] font-bold text-[#7C5CFF] bg-[#7C5CFF]/8 border border-[#7C5CFF]/20 rounded-full px-3 py-1.5 uppercase tracking-wider">
              Mode Demo
            </span>
          )}
          <button
            onClick={handleDeleteHistory}
            disabled={deleting || messages.length === 0}
            className="inline-flex items-center gap-2 px-3.5 py-2.5 text-xs font-semibold text-rose-500 bg-rose-50 hover:bg-rose-100 rounded-xl transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {deleting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
            Hapus Riwayat
          </button>
        </div>
      </div>

      <div className="bg-white border border-slate-100 rounded-2xl shadow-xs overflow-hidden">
        <div className="h-[52vh] min-h-[360px] max-h-[560px] overflow-y-auto p-5 sm:p-6 bg-[#F8FAFC]/70 space-y-4">
          {loadingHistory ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="w-6 h-6 text-[#4F8EF7] animate-spin" />
            </div>
          ) : messages.length === 0 ? (
            <div className="flex items-end gap-2 animate-in fade-in duration-300">
              <BuddioAvatar />
              <div className="max-w-[80%] px-4 py-3 bg-white border border-slate-100 text-slate-700 text-sm leading-relaxed rounded-2xl rounded-bl-md shadow-sm">
                {GREETING}
              </div>
            </div>
          ) : (
            messages.map((msg) =>
              msg.role === "user" ? (
                <div key={msg.id} className="flex justify-end animate-in fade-in duration-300">
                  <div className="max-w-[80%] px-4 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white text-sm leading-relaxed rounded-2xl rounded-br-md shadow-sm whitespace-pre-wrap break-words">
                    {msg.message}
                  </div>
                </div>
              ) : (
                <div key={msg.id} className="flex items-end gap-2 animate-in fade-in duration-300">
                  <BuddioAvatar />
                  <div className="max-w-[80%] px-4 py-3 bg-white border border-slate-100 text-slate-700 text-sm leading-relaxed rounded-2xl rounded-bl-md shadow-sm break-words">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm, remarkMath]}
                      rehypePlugins={[rehypeKatex]}
                      components={{
                        p: ({ node, ...props }) => <p className="mb-2 last:mb-0 leading-relaxed text-sm" {...props} />,
                        strong: ({ node, ...props }) => <strong className="font-extrabold text-slate-900" {...props} />,
                        em: ({ node, ...props }) => <em className="italic" {...props} />,
                        h1: ({ node, ...props }) => <h1 className="text-xl font-extrabold text-slate-900 mt-4 mb-2 first:mt-0" {...props} />,
                        h2: ({ node, ...props }) => <h2 className="text-lg font-bold text-slate-900 mt-3 mb-2 first:mt-0" {...props} />,
                        h3: ({ node, ...props }) => <h3 className="text-base font-bold text-slate-900 mt-3 mb-1.5 first:mt-0" {...props} />,
                        h4: ({ node, ...props }) => <h4 className="text-sm font-semibold text-slate-800 mt-2 mb-1 first:mt-0" {...props} />,
                        ul: ({ node, ...props }) => <ul className="list-disc pl-5 mb-2 space-y-1" {...props} />,
                        ol: ({ node, ...props }) => <ol className="list-decimal pl-5 mb-2 space-y-1" {...props} />,
                        li: ({ node, ...props }) => <li className="text-sm leading-relaxed" {...props} />,
                        hr: ({ node, ...props }) => <hr className="my-4 border-slate-200/60" {...props} />,
                        a: ({ node, ...props }) => <a className="text-[#4F8EF7] hover:underline font-semibold" target="_blank" rel="noopener noreferrer" {...props} />,
                        blockquote: ({ node, ...props }) => <blockquote className="border-l-4 border-slate-200 pl-3 italic my-2 text-slate-500 bg-slate-50/50 py-1 pr-2 rounded-r-lg" {...props} />,
                        pre: ({ node, ...props }) => <pre className="block bg-slate-50 text-slate-800 p-3 rounded-xl text-xs font-mono border border-slate-100 overflow-x-auto my-3 max-w-full" {...props} />,
                        code: ({ node, inline, ...props }: any) => 
                          inline ? (
                            <code className="bg-slate-50 text-slate-800 px-1 py-0.5 rounded text-xs font-mono border border-slate-100" {...props} />
                          ) : (
                            <code className="font-mono text-xs" {...props} />
                          )
                      }}
                    >
                      {msg.message}
                    </ReactMarkdown>
                  </div>
                </div>
              )
            )
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="border-t border-slate-100 p-4 flex items-end gap-3">
          <textarea
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Tulis pertanyaanmu di sini..."
            className="flex-1 resize-none px-4 py-3 text-sm bg-slate-50 border border-slate-100 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all text-slate-800 placeholder-slate-400"
          />
          <button
            onClick={() => handleSend()}
            disabled={sending || !input.trim() || remaining === 0}
            className="inline-flex items-center justify-center w-11 h-11 shrink-0 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:scale-[1.05] transition-all disabled:opacity-40 disabled:hover:scale-100 disabled:cursor-not-allowed"
          >
            {sending ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function MentorPage() {
  return (
    <Suspense fallback={null}>
      <MentorPageContent />
    </Suspense>
  );
}
