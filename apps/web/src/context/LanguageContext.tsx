"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";

export type Language = "id" | "en";

type Primitive = string | number;
interface Dict {
  [key: string]: Primitive | Dict;
}

const id: Dict = {
  common: {
    back: "Kembali",
    save: "Simpan",
    saved: "Tersimpan!",
    cancel: "Batal",
    loading: "Memuat...",
    close: "Tutup",
  },
  dashboard: {
    title: "Dashboard",
    topic: "Topik Belajar",
    roadmap: "Roadmap",
    mentor: "Mentor AI",
    assessment: "Assessment",
    progress: "Progress",
    settings: "Pengaturan",
    logout: "Logout",
    selamatDatang: "Halo",
    search: "Cari topik atau materi...",
    notifications: "Notifikasi",
    markAllRead: "Tandai dibaca semua",
    profile: "Profil Saya",
    accountSettings: "Pengaturan Akun",
    darkMode: "Mode Gelap",
    lightMode: "Mode Terang",
    grade: {
      sd: "SD",
      smp: "SMP",
      sma: "SMA",
      mahasiswa: "Mahasiswa",
      self_learner: "Self Learner",
    },
    popularTopics: "Topik Populer",
    searchResults: "Hasil Pencarian",
    noResults: "Tidak ada hasil untuk",
  },
  materi: {
    notReady: "Materi belum tersedia",
    notReadyDesc: "Klik tombol di bawah agar AI Buddio menyusun materi pembelajaran lengkap.",
    generate: "Generate Materi Sekarang",
    generating: "Menyusun materi...",
    generatingDesc: "AI Buddio sedang menyiapkan materi lengkap untukmu.",
    coreTitle: "Materi Inti",
    highlightActive: "Mode Aktif — Blok teks",
    highlightInactive: "Aktifkan Highlight",
    highlightOn: "Highlight On",
    highlight: "Highlight",
    videoTitle: "Belajar Lewat Video",
    videoDesc: "Video relevan untuk memperdalam pemahamanmu.",
    stillConfused: "Masih Bingung?",
    stillConfusedDesc: "Tanya Kak Buddio langsung tentang materi \"{step}\" ini.",
    askBuddio: "Tanya Kak Buddio",
    regenerate: "Regenerate Materi",
    exitStudyMode: "Keluar Mode Belajar",
    studyMode: "Mode Belajar",
    done: "Selesai",
    notes: "Catatan",
    notesTitle: "Catatan Belajar",
    notesPlaceholder: "Tulis catatan belajarmu di sini...\n\nContoh:\n- Poin penting yang harus diingat\n- Pertanyaan untuk ditanyakan ke Kak Buddio\n- Ringkasan versi sendiri",
    notesAuto: "Catatan tersimpan otomatis di browser ini ({count} karakter)",
    backToRoadmap: "Kembali ke Roadmap",
    topic: "Topik: {topic}",
    highlightLabel: "Highlight:",
  },
  settings: {
    title: "Pengaturan",
    desc: "Kelola preferensi aplikasi, informasi profil, dan keamanan akunmu.",
    sectionTitle: "Pengaturan",
    sectionDesc: "Atur preferensi tampilan dan kebiasaan belajarmu.",
    theme: "Tema",
    language: "Bahasa",
    notifications: "Notifikasi",
    notificationsLabel: "Aktifkan notifikasi belajar",
    dailyGoal: "Target Belajar Harian (menit)",
    saveSettings: "Simpan Pengaturan",
    saved: "Pengaturan tersimpan.",
    loadError: "Gagal memuat pengaturan.",
    saveError: "Gagal menyimpan pengaturan.",
    profileTitle: "Profil",
    profileDesc: "Perbarui informasi dirimu agar pengalaman belajar lebih personal.",
    changePassword: "Ganti Password",
    changePasswordDesc: "Amankan akunmu dengan password baru.",
    fullName: "Nama Lengkap",
    learningGoal: "Tujuan Belajar",
    learningGoalPlaceholder: "Contoh: Lulus UTBK, menguasai pemrograman...",
    oldPassword: "Password Lama",
    newPassword: "Password Baru",
    newPasswordPlaceholder: "Minimal 8 karakter",
    confirmPassword: "Konfirmasi Password Baru",
    saveProfile: "Simpan Profil",
    changePasswordBtn: "Ganti Password",
    passwordChanged: "Password berhasil diganti.",
    profileSaved: "Profil berhasil disimpan.",
  },
};

const en: Dict = {
  common: {
    back: "Back",
    save: "Save",
    saved: "Saved!",
    cancel: "Cancel",
    loading: "Loading...",
    close: "Close",
  },
  dashboard: {
    title: "Dashboard",
    topic: "Learning Topics",
    roadmap: "Roadmap",
    mentor: "AI Mentor",
    assessment: "Assessment",
    progress: "Progress",
    settings: "Settings",
    logout: "Logout",
    selamatDatang: "Hello",
    search: "Search topics or materials...",
    notifications: "Notifications",
    markAllRead: "Mark all read",
    profile: "My Profile",
    accountSettings: "Account Settings",
    darkMode: "Dark Mode",
    lightMode: "Light Mode",
    grade: {
      sd: "Elementary",
      smp: "Middle School",
      sma: "High School",
      mahasiswa: "College",
      self_learner: "Self Learner",
    },
    popularTopics: "Popular Topics",
    searchResults: "Search Results",
    noResults: "No results for",
  },
  materi: {
    notReady: "Material not ready",
    notReadyDesc: "Click the button below so AI Buddio can prepare a complete learning material.",
    generate: "Generate Material Now",
    generating: "Preparing material...",
    generatingDesc: "AI Buddio is preparing your complete material.",
    coreTitle: "Core Material",
    highlightActive: "Active Mode — Select text",
    highlightInactive: "Enable Highlight",
    highlightOn: "Highlight On",
    highlight: "Highlight",
    videoTitle: "Learn with Videos",
    videoDesc: "Relevant videos to deepen your understanding.",
    stillConfused: "Still Confused?",
    stillConfusedDesc: "Ask Buddio directly about this \"{step}\" material.",
    askBuddio: "Ask Buddio",
    regenerate: "Regenerate Material",
    exitStudyMode: "Exit Study Mode",
    studyMode: "Study Mode",
    done: "Done",
    notes: "Notes",
    notesTitle: "Study Notes",
    notesPlaceholder: "Write your study notes here...\n\nExample:\n- Key points to remember\n- Questions to ask Buddio\n- Your own summary",
    notesAuto: "Notes auto-saved in this browser ({count} characters)",
    backToRoadmap: "Back to Roadmap",
    topic: "Topic: {topic}",
    highlightLabel: "Highlights:",
  },
  settings: {
    title: "Settings",
    desc: "Manage app preferences, profile information, and account security.",
    sectionTitle: "Settings",
    sectionDesc: "Customize display preferences and study habits.",
    theme: "Theme",
    language: "Language",
    notifications: "Notifications",
    notificationsLabel: "Enable study notifications",
    dailyGoal: "Daily Study Goal (minutes)",
    saveSettings: "Save Settings",
    saved: "Settings saved.",
    loadError: "Failed to load settings.",
    saveError: "Failed to save settings.",
    profileTitle: "Profile",
    profileDesc: "Update your information for a more personal learning experience.",
    changePassword: "Change Password",
    changePasswordDesc: "Secure your account with a new password.",
    fullName: "Full Name",
    learningGoal: "Learning Goal",
    learningGoalPlaceholder: "Example: Pass UTBK, master programming...",
    oldPassword: "Old Password",
    newPassword: "New Password",
    newPasswordPlaceholder: "Minimum 8 characters",
    confirmPassword: "Confirm New Password",
    saveProfile: "Save Profile",
    changePasswordBtn: "Change Password",
    passwordChanged: "Password changed successfully.",
    profileSaved: "Profile saved successfully.",
  },
};

const dictionaries: Record<Language, Dict> = { id, en };

interface LanguageContextValue {
  lang: Language;
  setLang: (l: Language) => void;
  toggleLang: () => void;
  t: (key: string, vars?: Record<string, Primitive>) => string;
}

const LanguageContext = createContext<LanguageContextValue | undefined>(undefined);

function getPath(dict: Dict, key: string): Primitive {
  const parts = key.split(".");
  let cur: Dict | Primitive = dict;
  for (const p of parts) {
    if (cur && typeof cur === "object" && p in (cur as Dict)) {
      cur = (cur as Dict)[p];
    } else {
      return key;
    }
  }
  return typeof cur === "string" || typeof cur === "number" ? cur : key;
}

function getInitialLang(): Language {
  if (typeof window === "undefined") return "id";
  const stored = localStorage.getItem("buddio_lang");
  if (stored === "en" || stored === "id") return stored;
  return "id";
}

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLangState] = useState<Language>("id");

  useEffect(() => {
    setLangState(getInitialLang());
  }, []);

  const setLang = useCallback((l: Language) => {
    setLangState(l);
    localStorage.setItem("buddio_lang", l);
  }, []);

  const toggleLang = useCallback(() => {
    setLang(lang === "id" ? "en" : "id");
  }, [lang, setLang]);

  const t = useCallback(
    (key: string, vars?: Record<string, Primitive>) => {
      let value: Primitive = getPath(dictionaries[lang], key);
      if (typeof value === "string" && vars) {
        for (const [k, v] of Object.entries(vars)) {
          value = value.replaceAll(`{${k}}`, String(v));
        }
      }
      return typeof value === "string" ? value : key;
    },
    [lang]
  );

  return (
    <LanguageContext.Provider value={{ lang, setLang, toggleLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLanguage must be used within LanguageProvider");
  return ctx;
}
