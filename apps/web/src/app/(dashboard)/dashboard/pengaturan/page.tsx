"use client";

import React, { useCallback, useEffect, useState } from "react";
import { Loader2, Settings as SettingsIcon, User as UserIcon, Lock, CheckCircle2, AlertCircle } from "lucide-react";
import api, { ApiError } from "@/services/api";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";
import { useLanguage } from "@/context/LanguageContext";
import type { Settings, User } from "@/lib/types";

export default function PengaturanPage() {
  const { user, loading } = useAuth();
  const { theme: currentTheme, setTheme: setCurrentTheme } = useTheme();
  const { lang: contextLang, setLang: setContextLang } = useLanguage();

  const [settingsLoading, setSettingsLoading] = useState(true);
  const [settingsInitial, setSettingsInitial] = useState<Settings | null>(null);
  const [theme, setTheme] = useState("light");
  const [notification, setNotification] = useState(true);
  const [language, setLanguage] = useState("id");
  const [dailyGoal, setDailyGoal] = useState(20);
  const [settingsSaving, setSettingsSaving] = useState(false);
  const [settingsError, setSettingsError] = useState<string | null>(null);
  const [settingsSuccess, setSettingsSuccess] = useState<string | null>(null);

  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordSaving, setPasswordSaving] = useState(false);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [passwordSuccess, setPasswordSuccess] = useState<string | null>(null);

  const loadSettings = useCallback(() => {
    api
      .get<Settings>("/settings/me")
      .then((s) => {
        setSettingsInitial(s);
        setTheme(s.theme);
        setNotification(s.notification);
        setLanguage(s.language);
        setDailyGoal(s.daily_goal);
      })
      .catch((err) => {
        setSettingsError(err instanceof ApiError ? err.message : "Gagal memuat pengaturan.");
      })
      .finally(() => setSettingsLoading(false));
  }, []);

  useEffect(() => {
    loadSettings();
  }, [loadSettings]);

  const handleSaveSettings = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!settingsInitial) return;
    setSettingsSaving(true);
    setSettingsError(null);
    setSettingsSuccess(null);
    const changes: Partial<Settings> = {};
    if (theme !== settingsInitial.theme) changes.theme = theme;
    if (notification !== settingsInitial.notification) changes.notification = notification;
    if (language !== settingsInitial.language) changes.language = language;
    if (dailyGoal !== settingsInitial.daily_goal) changes.daily_goal = dailyGoal;
    try {
      const updated = await api.put<Settings>("/settings/me", changes);
      setSettingsInitial(updated);
      setTheme(updated.theme);
      setNotification(updated.notification);
      setLanguage(updated.language);
      setDailyGoal(updated.daily_goal);
      setSettingsSuccess("Pengaturan tersimpan.");
    } catch (err) {
      setSettingsError(err instanceof ApiError ? err.message : "Gagal menyimpan pengaturan.");
    } finally {
      setSettingsSaving(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError(null);
    setPasswordSuccess(null);
    if (newPassword !== confirmPassword) {
      setPasswordError("Konfirmasi password tidak cocok.");
      return;
    }
    if (newPassword.length < 8) {
      setPasswordError("Password baru minimal 8 karakter.");
      return;
    }
    setPasswordSaving(true);
    try {
      await api.put<void>("/users/password", {
        old_password: oldPassword,
        new_password: newPassword,
      });
      setOldPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setPasswordSuccess("Password berhasil diganti.");
    } catch (err) {
      setPasswordError(err instanceof ApiError ? err.message : "Gagal mengganti password.");
    } finally {
      setPasswordSaving(false);
    }
  };

  const handleThemeChange = (newTheme: string) => {
    setTheme(newTheme);
    setCurrentTheme(newTheme as "light" | "dark");
  };

  const handleLanguageChange = (newLang: string) => {
    setLanguage(newLang);
    setContextLang(newLang as "id" | "en");
  };

  const inputClass =
    "w-full px-4 py-3 text-sm bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] focus:border-[#4F8EF7] focus:bg-white dark:focus:bg-[#0f172a] rounded-xl outline-none transition-all text-slate-900 dark:text-slate-200";
  const labelClass =
    "text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider";

  if (loading || settingsLoading || !user) {
    return (
      <div className="flex items-center justify-center py-24">
        <Loader2 className="w-8 h-8 text-[#4F8EF7] animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-6 sm:py-8 space-y-8 animate-in fade-in duration-300">
      <div className="space-y-1.5 border-b border-slate-100 dark:border-[#334155] pb-8">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight font-sans">
          Pengaturan
        </h2>
        <p className="text-sm sm:text-base text-slate-500 dark:text-slate-400 font-sans">
          Kelola preferensi aplikasi, informasi profil, dan keamanan akunmu.
        </p>
      </div>

      <section className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-6 space-y-6 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#4F8EF7]/10 flex items-center justify-center shrink-0">
            <SettingsIcon className="w-5 h-5 text-[#4F8EF7]" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">Pengaturan</h3>
            <p className="text-[11px] text-slate-500 dark:text-slate-400">Atur preferensi tampilan dan kebiasaan belajarmu.</p>
          </div>
        </div>

        {settingsError && (
          <div className="flex items-center gap-2 text-xs bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 text-rose-600 dark:text-rose-400 rounded-xl px-4 py-3">
            <AlertCircle className="w-4 h-4 shrink-0" />
            {settingsError}
          </div>
        )}
        {settingsSuccess && (
          <div className="flex items-center gap-2 text-xs bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/30 text-emerald-600 dark:text-emerald-400 rounded-xl px-4 py-3">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            {settingsSuccess}
          </div>
        )}

        <form onSubmit={handleSaveSettings} className="space-y-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className={labelClass}>Tema</label>
              <select value={theme} onChange={(e) => handleThemeChange(e.target.value)} className={inputClass}>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </select>
            </div>
            <div className="space-y-1.5">
              <label className={labelClass}>Bahasa</label>
              <select value={language} onChange={(e) => handleLanguageChange(e.target.value)} className={inputClass}>
                <option value="id">Indonesia</option>
                <option value="en">English</option>
              </select>
            </div>
          </div>

          <div className="space-y-1.5">
            <label className={labelClass}>Notifikasi</label>
            <label className="flex items-center justify-between bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] rounded-xl px-4 py-3 cursor-pointer">
              <span className="text-sm text-slate-600 dark:text-slate-300">Aktifkan notifikasi belajar</span>
              <input
                type="checkbox"
                checked={notification}
                onChange={(e) => setNotification(e.target.checked)}
                className="sr-only peer"
              />
              <span className="relative inline-flex w-11 h-6 bg-slate-200 rounded-full transition-colors duration-200 peer-checked:bg-[#4F8EF7] after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:w-5 after:h-5 after:bg-white after:rounded-full after:shadow-sm after:transition-transform after:duration-200 peer-checked:after:translate-x-5" />
            </label>
          </div>

          <div className="space-y-1.5">
            <label className={labelClass}>Target Belajar Harian (menit)</label>
            <input
              type="number"
              min={0}
              value={dailyGoal}
              onChange={(e) => setDailyGoal(e.target.value === "" ? 0 : Number(e.target.value))}
              className={inputClass}
            />
          </div>

          <button
            type="submit"
            disabled={settingsSaving}
            className="w-full sm:w-auto px-5 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:opacity-90 hover:scale-[1.01] transition-all flex items-center justify-center gap-2 disabled:opacity-60 disabled:pointer-events-none"
          >
            {settingsSaving && <Loader2 className="w-4 h-4 animate-spin" />}
            Simpan Pengaturan
          </button>
        </form>
      </section>

      <section className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-6 space-y-6 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#7C5CFF]/10 flex items-center justify-center shrink-0">
            <UserIcon className="w-5 h-5 text-[#7C5CFF]" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">Profil</h3>
            <p className="text-[11px] text-slate-500 dark:text-slate-400">Perbarui informasi dirimu agar pengalaman belajar lebih personal.</p>
          </div>
        </div>

        <ProfileForm key={user.id} user={user} />
      </section>

      <section className="bg-white dark:bg-[#1e293b] border border-slate-100 dark:border-[#334155] rounded-2xl p-6 space-y-6 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#F97316]/10 flex items-center justify-center shrink-0">
            <Lock className="w-5 h-5 text-[#F97316]" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm">Ganti Password</h3>
            <p className="text-[11px] text-slate-500 dark:text-slate-400">Amankan akunmu dengan password baru.</p>
          </div>
        </div>

        {passwordError && (
          <div className="flex items-center gap-2 text-xs bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 text-rose-600 dark:text-rose-400 rounded-xl px-4 py-3">
            <AlertCircle className="w-4 h-4 shrink-0" />
            {passwordError}
          </div>
        )}
        {passwordSuccess && (
          <div className="flex items-center gap-2 text-xs bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/30 text-emerald-600 dark:text-emerald-400 rounded-xl px-4 py-3">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            {passwordSuccess}
          </div>
        )}

        <form onSubmit={handleChangePassword} className="space-y-5">
          <div className="space-y-1.5">
            <label className={labelClass}>Password Lama</label>
            <input
              type="password"
              required
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              placeholder="Password lama kamu"
              className={inputClass}
            />
          </div>
          <div className="space-y-1.5">
            <label className={labelClass}>Password Baru</label>
            <input
              type="password"
              required
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Minimal 8 karakter"
              className={inputClass}
            />
          </div>
          <div className="space-y-1.5">
            <label className={labelClass}>Konfirmasi Password Baru</label>
            <input
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Ulangi password baru"
              className={inputClass}
            />
          </div>

          <button
            type="submit"
            disabled={passwordSaving}
            className="w-full sm:w-auto px-5 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:opacity-90 hover:scale-[1.01] transition-all flex items-center justify-center gap-2 disabled:opacity-60 disabled:pointer-events-none"
          >
            {passwordSaving && <Loader2 className="w-4 h-4 animate-spin" />}
            Ganti Password
          </button>
        </form>
      </section>
    </div>
  );
}

function ProfileForm({ user }: { user: User }) {
  const { refreshUser } = useAuth();
  const [fullName, setFullName] = useState(user.full_name ?? "");
  const [learningGoal, setLearningGoal] = useState(user.learning_goal ?? "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const inputClass =
    "w-full px-4 py-3 text-sm bg-slate-50 dark:bg-[#0f172a] border border-slate-100 dark:border-[#334155] focus:border-[#4F8EF7] focus:bg-white dark:focus:bg-[#0f172a] rounded-xl outline-none transition-all text-slate-900 dark:text-slate-200";
  const labelClass =
    "text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider";

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(null);
    const changes: { full_name?: string; learning_goal?: string } = {};
    if (fullName !== (user.full_name ?? "")) changes.full_name = fullName;
    if (learningGoal !== (user.learning_goal ?? "")) changes.learning_goal = learningGoal;
    try {
      await api.put<User>("/users/me", changes);
      await refreshUser();
      setSuccess("Profil berhasil disimpan.");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Gagal menyimpan profil.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      {error && (
        <div className="flex items-center gap-2 text-xs bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 text-rose-600 dark:text-rose-400 rounded-xl px-4 py-3">
          <AlertCircle className="w-4 h-4 shrink-0" />
          {error}
        </div>
      )}
      {success && (
        <div className="flex items-center gap-2 text-xs bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/30 text-emerald-600 dark:text-emerald-400 rounded-xl px-4 py-3">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          {success}
        </div>
      )}
      <form onSubmit={handleSaveProfile} className="space-y-5">
        <div className="space-y-1.5">
          <label className={labelClass}>Nama Lengkap</label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="Nama lengkap kamu"
            className={inputClass}
          />
        </div>
        <div className="space-y-1.5">
          <label className={labelClass}>Tujuan Belajar</label>
          <input
            type="text"
            value={learningGoal}
            onChange={(e) => setLearningGoal(e.target.value)}
            placeholder="Contoh: Lulus UTBK, menguasai pemrograman..."
            className={inputClass}
          />
        </div>

        <button
          type="submit"
          disabled={saving}
          className="w-full sm:w-auto px-5 py-3 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/15 hover:opacity-90 hover:scale-[1.01] transition-all flex items-center justify-center gap-2 disabled:opacity-60 disabled:pointer-events-none"
        >
          {saving && <Loader2 className="w-4 h-4 animate-spin" />}
          Simpan Profil
        </button>
      </form>
    </>
  );
}
