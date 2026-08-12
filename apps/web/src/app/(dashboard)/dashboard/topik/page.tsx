"use client";

import React, { useState } from "react";
import {
  Search,
  BookOpen,
  Compass,
  Zap,
  FlaskConical,
  Dna,
  Languages,
  Code,
  Layers,
  Brain,
  ArrowRight,
  Sparkles,
  X,
  Loader2,
} from "lucide-react";
import api, { ApiError } from "@/services/api";
import type { Topic } from "@/lib/types";

const POPULAR_TOPICS = [
  { name: "Matematika", icon: Compass, learners: "2.4k pembelajar" },
  { name: "Fisika", icon: Zap, learners: "1.8k pembelajar" },
  { name: "Kimia", icon: FlaskConical, learners: "1.2k pembelajar" },
  { name: "Biologi", icon: Dna, learners: "950 pembelajar" },
  { name: "Bahasa Inggris", icon: Languages, learners: "3.1k pembelajar" },
  { name: "Pemrograman", icon: Code, learners: "4.2k pembelajar" },
  { name: "UI/UX", icon: Layers, learners: "2.0k pembelajar" },
  { name: "Machine Learning", icon: Brain, learners: "1.5k pembelajar" },
];

export default function PilihTopikPage() {
  const [searchVal, setSearchVal] = useState("");
  const [selectedTopic, setSelectedTopic] = useState("");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setSearchVal(val);
    setSelectedTopic(val);
  };

  const handleCardSelect = (topicName: string) => {
    setSelectedTopic(topicName);
    setSearchVal(topicName);
  };

  const handleCreateTopic = async () => {
    if (!selectedTopic.trim() || creating) return;
    setCreating(true);
    setError(null);
    try {
      const topic = await api.post<Topic>("/topics", { title: selectedTopic.trim() });
      window.location.href = `/dashboard/roadmap?topic=${topic.id}`;
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Gagal membuat topik.");
      setCreating(false);
    }
  };

  const isButtonActive = selectedTopic.trim().length > 0;

  return (
    <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-10 animate-in fade-in duration-300">
      {/* Title Header */}
      <div className="text-center space-y-2 max-w-xl mx-auto py-4">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight font-sans">
          Apa yang ingin kamu pelajari hari ini?
        </h2>
        <p className="text-sm text-slate-500 font-sans leading-relaxed">
          Tentukan topik pelajaran atau bidang keahlianmu. AI Mentor Buddio akan menganalisis dan menyusun peta jalan belajar yang disesuaikan khusus untukmu.
        </p>
      </div>

      {error && (
        <div className="max-w-2xl mx-auto text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
          {error}
        </div>
      )}

      {/* Large Search Box */}
      <div className="relative max-w-2xl mx-auto">
        <span className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-slate-400" />
        </span>
        <input
          type="text"
          value={searchVal}
          onChange={handleSearchChange}
          placeholder="Contoh: React, Kalkulus, Fisika, TOEFL..."
          className="w-full pl-11 pr-5 py-4 text-base bg-white border border-slate-100 focus:border-[#4F8EF7] rounded-xl outline-none shadow-xs focus:shadow-md transition-all duration-200 text-slate-900 placeholder-slate-400"
        />
        {searchVal && (
          <button
            onClick={() => {
              setSearchVal("");
              setSelectedTopic("");
            }}
            className="absolute inset-y-0 right-0 pr-4 flex items-center text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Popular Topics Section */}
      <div className="space-y-4">
        <h3 className="text-xs font-extrabold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <Sparkles className="w-4 h-4 text-[#4F8EF7]" />
          Topik Populer
        </h3>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {POPULAR_TOPICS.map((topic) => {
            const TopicIcon = topic.icon;
            const isSelected = selectedTopic.toLowerCase() === topic.name.toLowerCase();

            return (
              <button
                key={topic.name}
                onClick={() => handleCardSelect(topic.name)}
                className={`p-5 rounded-xl border text-left flex flex-col justify-between gap-4 transition-all duration-300 cursor-pointer group ${
                  isSelected
                    ? "border-[#4F8EF7] bg-[#4F8EF7]/5 shadow-sm shadow-[#4F8EF7]/10"
                    : "border-slate-100 bg-white hover:border-slate-300 hover:scale-[1.02]"
                }`}
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center transition-colors shrink-0 ${
                  isSelected
                    ? "bg-[#4F8EF7] text-white"
                    : "bg-slate-50 text-slate-500 group-hover:bg-[#4F8EF7]/10 group-hover:text-[#4F8EF7]"
                }`}>
                  <TopicIcon className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-slate-900 text-sm leading-tight">{topic.name}</h4>
                  <span className="text-[10px] text-slate-400 font-medium block mt-0.5">{topic.learners}</span>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Big Action Button */}
      <div className="pt-6 text-center">
        <button
          disabled={!isButtonActive || creating}
          onClick={handleCreateTopic}
          className={`w-full sm:w-auto inline-flex items-center justify-center gap-2 px-10 py-4 font-bold text-sm rounded-xl shadow-md transition-all duration-300 group ${
            isButtonActive
              ? "bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white shadow-[#4F8EF7]/15 hover:scale-[1.02] hover:shadow-lg hover:shadow-[#4F8EF7]/20"
              : "bg-slate-100 border border-slate-200/50 text-slate-400 cursor-not-allowed shadow-none"
          }`}
        >
          {creating ? <Loader2 className="w-4.5 h-4.5 animate-spin" /> : <BookOpen className="w-4.5 h-4.5" />}
          <span>{creating ? "Menyiapkan topik..." : "Buat Roadmap Belajar"}</span>
          <ArrowRight className="w-4.5 h-4.5 transition-transform group-hover:translate-x-1 duration-200" />
        </button>
      </div>
    </div>
  );
}
