"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";
import { useLanguage } from "@/context/LanguageContext";
import {
  LayoutDashboard,
  BookOpen,
  Map,
  Sparkles,
  ClipboardCheck,
  BarChart3,
  Settings,
  LogOut,
  Bell,
  Search,
  Menu,
  X,
  User,
  Sun,
  Moon,
} from "lucide-react";

const GRADE_LABELS: Record<string, string> = {
  sd: "SD",
  smp: "SMP",
  sma: "SMA",
  mahasiswa: "Mahasiswa",
  self_learner: "Self Learner",
};

// Buddio Logo Component (B + Smile + Speech Bubble concept)
const Logo = ({ collapsed = false }: { collapsed?: boolean }) => (
  <div className="flex items-center gap-3">
    <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white shadow-md shadow-[#4F8EF7]/20 shrink-0 select-none">
      {/* Speech bubble outline */}
      <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C7.02944 3 3 7.02944 3 12C3 13.9021 3.59393 15.6605 4.60501 17.102L3.5 20.5L6.898 19.395C8.33953 20.4061 10.0979 21 12 21Z"
          fill="white"
        />
        {/* Stylized B inside that has smiling face */}
        <path
          d="M8.5 7.5H11.8C12.8 7.5 13.5 8.1 13.5 9C13.5 9.7 13.0 10.2 12.3 10.4C13.1 10.6 13.7 11.2 13.7 12C13.7 12.9 12.9 13.5 11.8 13.5H8.5V7.5Z"
          fill="none"
          stroke="url(#buddio-logo-grad)"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {/* Smiling eyes */}
        <circle cx="10.2" cy="9.2" r="0.6" fill="url(#buddio-logo-grad)" />
        <circle cx="11.8" cy="9.2" r="0.6" fill="url(#buddio-logo-grad)" />
        <path
          d="M10.2 12.0C10.5 12.5 11.5 12.5 11.8 12.0"
          stroke="url(#buddio-logo-grad)"
          strokeWidth="0.8"
          strokeLinecap="round"
        />
        <defs>
          <linearGradient id="buddio-logo-grad" x1="8.5" y1="7.5" x2="13.7" y2="13.5" gradientUnits="userSpaceOnUse">
            <stop stopColor="#4F8EF7" />
            <stop offset="1" stopColor="#7C5CFF" />
          </linearGradient>
        </defs>
      </svg>
    </div>
    {!collapsed && (
      <span className="text-xl font-bold text-slate-900 dark:text-slate-100 tracking-tight font-sans">
        Buddio
      </span>
    )}
  </div>
);

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, loading, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { lang, toggleLang, t } = useLanguage();
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearchFocused, setIsSearchFocused] = useState(false);
  const [isMobileSearchOpen, setIsMobileSearchOpen] = useState(false);

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [loading, user, router]);

  if (loading || !user) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#0f172a] flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-[#4F8EF7] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const initials = (user.full_name || user.email)
    .split(" ")
    .map((p) => p[0]?.toUpperCase() ?? "")
    .slice(0, 2)
    .join("");

  const displayName = user.full_name || user.email.split("@")[0];
  const gradeLabel = user.grade_level ? (lang === "en" ? t(`dashboard.grade.${user.grade_level}`) : GRADE_LABELS[user.grade_level] ?? user.grade_level) : "â€”";

  const branding = [
    { label: t("dashboard.title"), href: "/dashboard", icon: LayoutDashboard },
    { label: t("dashboard.topic"), href: "/dashboard/topik", icon: BookOpen },
    { label: t("dashboard.roadmap"), href: "/dashboard/roadmap", icon: Map },
    { label: t("dashboard.mentor"), href: "/dashboard/mentor", icon: Sparkles },
    { label: t("dashboard.assessment"), href: "/dashboard/assessment", icon: ClipboardCheck },
    { label: t("dashboard.progress"), href: "/dashboard/progress", icon: BarChart3 },
    { label: t("dashboard.settings"), href: "/dashboard/pengaturan", icon: Settings },
  ];

  const trendingSearches = ["Machine Learning", "Python Dasar", "Aljabar Linear", "Fisika Termodinamika"];
  const filteredSearches = searchQuery
    ? trendingSearches.filter((item) =>
        item.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : trendingSearches;

  // Helper to determine page title
  const getPageTitle = () => {
    const current = branding.find((item) => item.href === pathname);
    return current ? current.label : t("dashboard.title");
  };

  // Nav item rendering logic
  const renderNavItems = (collapsed = false) => {
    return (
      <nav className="flex-1 space-y-1.5 px-4 py-6">
        {branding.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group relative ${
                isActive
                  ? "bg-[#4F8EF7]/8 dark:bg-[#60a5fa]/12 text-[#4F8EF7] dark:text-[#60a5fa] font-semibold"
                  : "text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#1e293b] hover:text-slate-900 dark:hover:text-slate-100"
              } ${collapsed ? "justify-center px-0" : ""}`}
              onClick={() => setIsMobileOpen(false)}
            >
              <Icon
                className={`w-5 h-5 shrink-0 transition-transform duration-200 group-hover:scale-105 ${
                  isActive ? "text-[#4F8EF7] dark:text-[#60a5fa]" : "text-slate-400 dark:text-slate-500 group-hover:text-slate-600 dark:group-hover:text-slate-300"
                }`}
              />
              {!collapsed && <span>{item.label}</span>}

              {/* Tooltip for tablet collapse */}
              {collapsed && (
                <div className="absolute left-full ml-3 px-2.5 py-1.5 bg-slate-900 dark:bg-[#0f172a] text-white text-xs rounded-lg opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-50 shadow-md">
                  {item.label}
                </div>
              )}
            </Link>
          );
        })}
      </nav>
    );
  };

  // Profile bottom bar rendering logic
  const renderProfileSection = (collapsed = false) => {
    return (
      <div className={`p-4 border-t border-slate-100 dark:border-[#334155] ${collapsed ? "flex flex-col items-center gap-4" : ""}`}>
        {/* User Card */}
        <div className={`flex items-center gap-3 ${collapsed ? "justify-center" : ""}`}>
          {/* Circular Avatar */}
          <div className="relative flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-tr from-[#4F8EF7] to-[#7C5CFF] text-white font-semibold text-sm shadow-sm shrink-0 select-none">
            {initials}
            <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-emerald-500 rounded-full border-2 border-white" />
          </div>

          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-slate-950 dark:text-slate-100 truncate">{displayName}</p>
              <p className="text-xs text-slate-500 dark:text-slate-400 truncate">{gradeLabel}</p>
            </div>
          )}
        </div>

        {/* Logout Button */}
        <button
          onClick={logout}
          className={`mt-3 w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium text-rose-500 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-500/10 transition-colors ${
            collapsed ? "justify-center px-0 mt-0 hover:bg-rose-50 rounded-full w-10 h-10" : ""
          }`}
          title="Keluar"
        >
          <LogOut className="w-5 h-5 shrink-0" />
          {!collapsed && <span>Logout</span>}
        </button>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 flex font-sans antialiased transition-colors">
      {/* 1. Sidebar - Desktop & Tablet */}
      <aside className="fixed top-0 bottom-0 left-0 z-30 bg-white dark:bg-[#1e293b] border-r border-slate-100 dark:border-[#334155] flex flex-col justify-between transition-all duration-300 hidden sm:flex sm:w-20 lg:w-64">
        {/* Top Header */}
        <div className="h-16 flex items-center px-6 border-b border-slate-100 dark:border-[#334155] shrink-0">
          {/* On tablet show only the icon */}
          <div className="lg:hidden block">
            <Logo collapsed={true} />
          </div>
          {/* On desktop show full logo */}
          <div className="hidden lg:block">
            <Logo collapsed={false} />
          </div>
        </div>

        {/* Navigation list */}
        <div className="flex-1 overflow-y-auto">
          {/* Hide/Show labels based on breakpoint */}
          <div className="lg:block hidden">
            {renderNavItems(false)}
          </div>
          <div className="lg:hidden block">
            {renderNavItems(true)}
          </div>
        </div>

        {/* Bottom Profile */}
        <div className="lg:block hidden">
          {renderProfileSection(false)}
        </div>
        <div className="lg:hidden block">
          {renderProfileSection(true)}
        </div>
      </aside>

      {/* 2. Mobile Drawer Sidebar */}
      {isMobileOpen && (
        <>
          {/* Backdrop overlay */}
          <div
            className="fixed inset-0 bg-slate-900/40 dark:bg-black/60 backdrop-blur-xs z-40 sm:hidden transition-opacity"
            onClick={() => setIsMobileOpen(false)}
          />
          {/* Sliding drawer */}
          <aside className="fixed top-0 bottom-0 left-0 w-64 bg-white dark:bg-[#1e293b] z-50 shadow-xl flex flex-col justify-between sm:hidden animate-in slide-in-from-left duration-300">
            <div className="h-16 flex items-center justify-between px-6 border-b border-slate-100 dark:border-[#334155] shrink-0">
              <Logo collapsed={false} />
              <button
                onClick={() => setIsMobileOpen(false)}
                className="p-1 rounded-lg text-slate-400 dark:text-slate-500 hover:bg-slate-50 dark:hover:bg-[#334155] hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto">
              {renderNavItems(false)}
            </div>
            {renderProfileSection(false)}
          </aside>
        </>
      )}

      {/* Click-away backdrop overlay for dropdowns */}
      {(isNotificationOpen || isProfileMenuOpen || isSearchFocused) && (
        <div
          className="fixed inset-0 z-10"
          onClick={() => {
            setIsNotificationOpen(false);
            setIsProfileMenuOpen(false);
            setIsSearchFocused(false);
          }}
        />
      )}

      {/* 3. Main Content Container */}
      <div className="flex-1 flex flex-col min-w-0 sm:pl-20 lg:pl-64 min-h-screen">
        {/* Sticky Header */}
        <header className="sticky top-0 z-20 h-16 bg-white/80 dark:bg-[#0f172a]/80 backdrop-blur-md border-b border-slate-100 dark:border-[#334155] flex items-center justify-between px-4 sm:px-6 transition-colors">
          {isMobileSearchOpen ? (
            <div className="flex-1 flex items-center gap-3 animate-in fade-in duration-200">
              <button
                onClick={() => {
                  setIsMobileSearchOpen(false);
                  setSearchQuery("");
                  setIsSearchFocused(false);
                }}
                className="p-2 rounded-xl text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#334155] hover:text-slate-800 dark:hover:text-slate-200 shrink-0 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
              <div className="relative flex-1">
                <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search className="h-4.5 w-4.5 text-slate-400" />
                </span>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onFocus={() => setIsSearchFocused(true)}
                  placeholder={t("dashboard.search")}
                  className="w-full pl-9 pr-4 py-2 text-sm bg-slate-50 dark:bg-[#1e293b] text-slate-800 dark:text-slate-200 border border-slate-100 dark:border-[#334155] rounded-xl outline-none focus:border-[#4F8EF7] focus:bg-white dark:focus:bg-[#0f172a] transition-all duration-200"
                  autoFocus
                />

                {isSearchFocused && (
                  <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-100 dark:border-[#334155] shadow-lg py-3 z-30 animate-in fade-in slide-in-from-top-1 duration-200">
                    <div className="px-4 pb-2 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
                      {searchQuery ? t("dashboard.searchResults") : t("dashboard.popularTopics")}
                    </div>
                    <div className="space-y-1">
                      {filteredSearches.length > 0 ? (
                        filteredSearches.map((item) => (
                          <button
                            key={item}
                            onMouseDown={() => {
                              setSearchQuery(item);
                              setIsSearchFocused(false);
                              setIsMobileSearchOpen(false);
                            }}
                            className="w-full text-left px-4 py-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-[#334155] transition-colors flex items-center gap-2"
                          >
                            <Search className="w-4 h-4 text-slate-400 dark:text-slate-500" />
                            {item}
                          </button>
                        ))
                      ) : (
                        <div className="px-4 py-2 text-sm text-slate-500 italic">
                          {t("dashboard.noResults")} &quot;{searchQuery}&quot;
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <>
              <div className="flex items-center gap-3">
                {/* Hamburger button for mobile */}
                <button
                  onClick={() => setIsMobileOpen(true)}
                  className="p-2 rounded-xl text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#334155] hover:text-slate-800 dark:hover:text-slate-200 sm:hidden shrink-0 transition-colors"
                >
                  <Menu className="w-5 h-5" />
                </button>
                
                {/* Dynamic Page Title */}
                <h1 className="text-lg font-bold text-slate-900 dark:text-slate-100 font-sans tracking-tight">
                  {getPageTitle()}
                </h1>
              </div>

              {/* Right Header Area */}
              <div className="flex items-center gap-3 sm:gap-4">
                {/* Desktop Search Bar Container */}
                <div className="relative hidden sm:block w-48 sm:w-60 md:w-72">
                  <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="h-4.5 w-4.5 text-slate-400" />
                  </span>
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onFocus={() => {
                      setIsSearchFocused(true);
                      setIsNotificationOpen(false);
                      setIsProfileMenuOpen(false);
                    }}
                    placeholder={t("dashboard.search")}
                    className="w-full pl-9 pr-4 py-2 text-sm bg-slate-50 dark:bg-[#1e293b] hover:bg-slate-100/70 dark:hover:bg-[#334155] focus:bg-white dark:focus:bg-[#0f172a] text-slate-800 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 border border-slate-100 dark:border-[#334155] focus:border-[#4F8EF7] rounded-xl outline-none transition-all duration-200"
                  />

                  {isSearchFocused && (
                    <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-100 dark:border-[#334155] shadow-lg py-3 z-30 animate-in fade-in slide-in-from-top-1 duration-200">
                      <div className="px-4 pb-2 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
                        {searchQuery ? t("dashboard.searchResults") : t("dashboard.popularTopics")}
                      </div>
                      <div className="space-y-1">
                        {filteredSearches.length > 0 ? (
                          filteredSearches.map((item) => (
                            <button
                              key={item}
                              onMouseDown={() => {
                                setSearchQuery(item);
                                setIsSearchFocused(false);
                              }}
                              className="w-full text-left px-4 py-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-[#334155] transition-colors flex items-center gap-2"
                            >
                              <Search className="w-4 h-4 text-slate-400 dark:text-slate-500" />
                              {item}
                            </button>
                          ))
                        ) : (
                          <div className="px-4 py-2 text-sm text-slate-500 italic">
                            {t("dashboard.noResults")} &quot;{searchQuery}&quot;
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                {/* Mobile Search Button */}
                <button
                  onClick={() => setIsMobileSearchOpen(true)}
                  className="sm:hidden p-2 rounded-xl text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#334155] transition-colors"
                >
                  <Search className="w-5 h-5" />
                </button>

                {/* Theme Toggle */}
                <button
                  onClick={toggleTheme}
                  className="p-2.5 rounded-xl text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#334155] hover:text-slate-800 dark:hover:text-slate-200 transition-colors"
                  title={theme === "dark" ? t("dashboard.lightMode") : t("dashboard.darkMode")}
                >
                  {theme === "dark" ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                </button>

                {/* Language Toggle */}
                <button
                  onClick={toggleLang}
                  className="px-2.5 py-1.5 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#334155] hover:text-slate-800 dark:hover:text-slate-200 transition-colors"
                  title={lang === "id" ? "Switch to English" : "Ganti ke Bahasa Indonesia"}
                >
                  {lang === "id" ? "EN" : "ID"}
                </button>

                {/* Notification Bell */}
                <div className="relative">
                  <button
                    onClick={() => {
                      setIsNotificationOpen(!isNotificationOpen);
                      setIsProfileMenuOpen(false);
                      setIsSearchFocused(false);
                    }}
                    className={`relative p-2.5 rounded-xl transition-colors group ${
                      isNotificationOpen
                        ? "bg-[#4F8EF7]/10 dark:bg-[#60a5fa]/15 text-[#4F8EF7] dark:text-[#60a5fa]"
                        : "text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#334155] hover:text-slate-800 dark:hover:text-slate-200"
                    }`}
                  >
                    <Bell className="w-5 h-5 transition-transform group-hover:rotate-12 duration-200" />
                    {/* Badge dot */}
                    <span className="absolute top-2 right-2.5 w-2 h-2 bg-[#7C5CFF] rounded-full border border-white dark:border-[#1e293b]" />
                  </button>

                  {isNotificationOpen && (
                    <div className="absolute right-0 top-full mt-2 w-80 bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-100 dark:border-[#334155] shadow-lg py-3 z-30 animate-in fade-in slide-in-from-top-1 duration-200">
                      <div className="px-4 py-2 border-b border-slate-50 dark:border-[#334155] flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-900 dark:text-slate-100 uppercase tracking-wider">{t("dashboard.notifications")}</span>
                        <button 
                          onClick={() => alert("Tandai semua dibaca (Dummy)")}
                          className="text-[10px] text-[#4F8EF7] hover:underline font-semibold"
                        >
                          {t("dashboard.markAllRead")}
                        </button>
                      </div>
                      <div className="max-h-72 overflow-y-auto divide-y divide-slate-50 dark:divide-[#334155]">
                        <div className="p-4 hover:bg-slate-50 dark:hover:bg-[#334155] transition-colors flex gap-3">
                          <div className="w-8 h-8 rounded-full bg-[#4F8EF7]/10 text-[#4F8EF7] flex items-center justify-center shrink-0">
                            <Sparkles className="w-4 h-4" />
                          </div>
                          <div className="space-y-1">
                            <p className="text-xs text-slate-800 dark:text-slate-200 leading-normal">
                              <strong>Roadmap Baru!</strong> AI Mentor menyusun peta belajar untuk Machine Learning. ðŸ¤–
                            </p>
                            <span className="text-[10px] text-slate-400 dark:text-slate-500">10 menit yang lalu</span>
                          </div>
                        </div>
                        <div className="p-4 hover:bg-slate-50 dark:hover:bg-[#334155] transition-colors flex gap-3">
                          <div className="w-8 h-8 rounded-full bg-[#22C55E]/10 text-[#22C55E] flex items-center justify-center shrink-0">
                            <ClipboardCheck className="w-4 h-4" />
                          </div>
                          <div className="space-y-1 flex-1">
                            <p className="text-xs text-slate-800 dark:text-slate-200 leading-normal">
                              <strong>Kuis Selesai!</strong> Kamu menyelesaikan Kuis Python Dasar dengan skor 90%. ðŸŽ‰
                            </p>
                            <span className="text-[10px] text-slate-400 dark:text-slate-500">2 jam yang lalu</span>
                          </div>
                        </div>
                        <div className="p-4 hover:bg-slate-50 dark:hover:bg-[#334155] transition-colors flex gap-3">
                          <div className="w-8 h-8 rounded-full bg-[#7C5CFF]/10 text-[#7C5CFF] flex items-center justify-center shrink-0">
                            <BarChart3 className="w-4 h-4" />
                          </div>
                          <div className="space-y-1">
                            <p className="text-xs text-slate-800 dark:text-slate-200 leading-normal">
                              <strong>Pertahankan Streak!</strong> Belajar hari ini untuk menjaga 12 hari streak belajarmu. ðŸ”¥
                            </p>
                            <span className="text-[10px] text-slate-400 dark:text-slate-500">5 jam yang lalu</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Profile Button (Avatar) */}
                <div className="relative">
                  <button
                    onClick={() => {
                      setIsProfileMenuOpen(!isProfileMenuOpen);
                      setIsNotificationOpen(false);
                      setIsSearchFocused(false);
                    }}
                    className={`flex items-center justify-center p-0.5 rounded-full border-2 transition-colors shrink-0 ${
                      isProfileMenuOpen ? "border-[#4F8EF7]" : "border-slate-100 dark:border-[#334155] hover:border-[#4F8EF7]"
                    }`}
                  >
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-slate-100 dark:bg-[#334155] text-slate-600 dark:text-slate-300 font-medium text-xs select-none">
                      <User className="w-4 h-4" />
                    </div>
                  </button>

                  {isProfileMenuOpen && (
                    <div className="absolute right-0 top-full mt-2 w-56 bg-white dark:bg-[#1e293b] rounded-2xl border border-slate-100 dark:border-[#334155] shadow-lg py-2 z-30 animate-in fade-in slide-in-from-top-1 duration-200">
                      <div className="px-4 py-3 border-b border-slate-50 dark:border-[#334155] flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-[#4F8EF7] to-[#7C5CFF] text-white flex items-center justify-center font-bold text-sm select-none shrink-0">
                          {initials}
                        </div>
                        <div className="min-w-0">
                          <p className="text-xs font-bold text-slate-900 dark:text-slate-100 truncate">{displayName}</p>
                          <p className="text-[10px] text-slate-500 dark:text-slate-400 truncate">{gradeLabel}</p>
                        </div>
                      </div>
                      <div className="py-1">
                        <Link
                          href="/dashboard/profile"
                          onClick={() => setIsProfileMenuOpen(false)}
                          className="w-full flex items-center gap-3 px-4 py-2.5 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-[#334155] transition-colors"
                        >
                          <User className="w-4 h-4 text-slate-400 dark:text-slate-500" />
                          {t("dashboard.profile")}
                        </Link>
                        <Link
                          href="/dashboard/pengaturan"
                          onClick={() => setIsProfileMenuOpen(false)}
                          className="w-full flex items-center gap-3 px-4 py-2.5 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-[#334155] transition-colors"
                        >
                          <Settings className="w-4 h-4 text-slate-400 dark:text-slate-500" />
                          {t("dashboard.accountSettings")}
                        </Link>
                      </div>
                      <div className="border-t border-slate-50 dark:border-[#334155] pt-1">
                        <button
                          onClick={() => {
                            setIsProfileMenuOpen(false);
                            logout();
                          }}
                          className="w-full flex items-center gap-3 px-4 py-2.5 text-xs font-medium text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-500/10 transition-colors text-left"
                        >
                          <LogOut className="w-4 h-4 text-rose-500" />
                          Logout
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </>
          )}
        </header>

        {/* Content body wrapper */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}

