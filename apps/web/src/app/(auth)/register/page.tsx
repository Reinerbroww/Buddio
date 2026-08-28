"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Sparkles, Loader2, AlertCircle } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { ApiError } from "@/services/api";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }

    setSubmitting(true);
    try {
      const user = await register({
        email,
        password,
        full_name: fullName || undefined,
      });
      router.push(user.grade_level ? "/dashboard" : "/onboarding");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to sign up. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white border border-slate-100 rounded-3xl shadow-xl shadow-slate-200/60 p-8 flex flex-col gap-6">
      <div className="text-center space-y-2">
        <div className="mx-auto w-12 h-12 bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] rounded-2xl flex items-center justify-center shadow-md shadow-[#4F8EF7]/20 mb-4">
          <Sparkles className="h-6 w-6 text-white" />
        </div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">Create your Buddio account</h1>
        <p className="text-xs text-slate-500">Start learning with an AI mentor that understands your level.</p>
      </div>

      {error && (
        <div className="flex items-start gap-2 text-xs bg-rose-50 border border-rose-200 text-rose-600 rounded-xl px-4 py-3">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-slate-600">Full Name</label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="Reiner"
            className="w-full px-4 py-3 text-sm bg-slate-50 border border-slate-100 text-slate-900 placeholder-slate-400 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-slate-600">Email</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@email.com"
            className="w-full px-4 py-3 text-sm bg-slate-50 border border-slate-100 text-slate-900 placeholder-slate-400 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-slate-600">Password</label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="At least 6 characters"
            className="w-full px-4 py-3 text-sm bg-slate-50 border border-slate-100 text-slate-900 placeholder-slate-400 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-bold text-slate-600">Confirm Password</label>
          <input
            type="password"
            required
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            placeholder="••••••••"
            className="w-full px-4 py-3 text-sm bg-slate-50 border border-slate-100 text-slate-900 placeholder-slate-400 focus:border-[#4F8EF7] focus:bg-white rounded-xl outline-none transition-all"
          />
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full mt-2 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] hover:scale-[1.01] hover:shadow-lg hover:shadow-[#4F8EF7]/20 disabled:opacity-60 disabled:hover:scale-100 text-white font-bold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 transition-all flex items-center justify-center gap-2"
        >
          {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
          Sign Up
        </button>
      </form>

      <p className="text-center text-xs text-slate-500">
        Already have an account?{" "}
        <Link href="/login" className="text-[#4F8EF7] hover:underline font-bold">
          Sign In
        </Link>
      </p>
    </div>
  );
}
