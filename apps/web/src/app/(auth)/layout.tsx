import { BuddioLogo } from "@/components/BuddioLogo";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 flex flex-col relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-[420px] bg-gradient-to-b from-[#4F8EF7]/10 via-[#7C5CFF]/5 to-transparent pointer-events-none" />
      <div className="absolute top-16 -left-24 w-72 h-72 bg-[#4F8EF7]/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-16 -right-24 w-72 h-72 bg-[#7C5CFF]/10 rounded-full blur-3xl pointer-events-none" />

      <header className="sticky top-0 z-50 border-b border-slate-100 bg-white/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center">
          <BuddioLogo />
        </div>
      </header>

      <main className="flex-1 w-full max-w-md mx-auto px-4 py-14 relative z-10">{children}</main>
    </div>
  );
}
