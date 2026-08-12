import Link from "next/link";
import {
  Map,
  Sparkles,
  ClipboardCheck,
  BarChart3,
  GraduationCap,
  ArrowRight,
  CheckCircle2,
  MessageCircle,
  Target,
  Star,
  Rocket,
} from "lucide-react";
import { BuddioLogo } from "@/components/BuddioLogo";

const FEATURES = [
  {
    icon: Map,
    title: "Peta Belajar AI",
    desc: "AI menyusun roadmap langkah demi langkah sesuai jenjang dan tujuan belajarmu.",
    gradient: "from-[#4F8EF7] to-[#7C5CFF]",
  },
  {
    icon: MessageCircle,
    title: "Mentor AI 24/7",
    desc: "Tanya apa saja, kapan saja. Mentor Buddio menjelaskan pelan-pelan dengan analogi yang mudah dipahami.",
    gradient: "from-[#7C5CFF] to-[#FACC15]",
  },
  {
    icon: ClipboardCheck,
    title: "Kuis Adaptif",
    desc: "Uji pemahamanmu dengan soal yang dibuat khusus. Langsung dapat pembahasan setelah menjawab.",
    gradient: "from-[#22C55E] to-[#4F8EF7]",
  },
  {
    icon: BarChart3,
    title: "Progress Terarah",
    desc: "Pantau perkembangan belajarmu. Kamu selalu tahu langkah berikutnya untuk terus maju.",
    gradient: "from-[#F59E0B] to-[#FACC15]",
  },
];

const STEPS = [
  {
    number: "1",
    title: "Tentukan Topik",
    desc: "Pilih topik yang ingin kamu pelajari, mulai dari matematika hingga pemrograman.",
  },
  {
    number: "2",
    title: "Dapatkan Roadmap",
    desc: "AI menyusun peta belajar personal berdasarkan jenjang dan tujuanmu.",
  },
  {
    number: "3",
    title: "Belajar Bersama AI",
    desc: "Ikuti langkah demi langkah, tanya mentor, dan kerjakan kuis untuk menguasai materi.",
  },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 flex flex-col overflow-x-hidden">
      {/* Sticky Navbar */}
      <header className="sticky top-0 z-50 border-b border-slate-100 bg-white/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <BuddioLogo />

          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-500">
            <a href="#fitur" className="hover:text-slate-900 transition-colors">
              Fitur
            </a>
            <a href="#cara-kerja" className="hover:text-slate-900 transition-colors">
              Cara Kerja
            </a>
            <a href="#tentang" className="hover:text-slate-900 transition-colors">
              Tentang
            </a>
          </nav>

          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="text-sm font-semibold text-slate-600 hover:text-slate-900 px-3 py-2 transition-colors"
            >
              Masuk
            </Link>
            <Link
              href="/register"
              className="inline-flex items-center gap-1.5 text-sm font-semibold text-white bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] hover:scale-[1.02] hover:shadow-lg hover:shadow-[#4F8EF7]/25 rounded-xl px-4 py-2.5 shadow-md shadow-[#4F8EF7]/15 transition-all duration-300"
            >
              Daftar Gratis
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="flex-1">
        <section className="relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-[480px] bg-gradient-to-b from-[#4F8EF7]/10 via-[#7C5CFF]/5 to-transparent pointer-events-none" />
          <div className="absolute top-24 -left-24 w-72 h-72 bg-[#4F8EF7]/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute top-40 -right-24 w-72 h-72 bg-[#7C5CFF]/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative max-w-6xl mx-auto px-4 py-16 sm:py-24 flex flex-col lg:flex-row items-center gap-12 lg:gap-16">
            {/* Hero copy */}
            <div className="flex-1 space-y-7 text-center lg:text-left">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 bg-white border border-slate-100 rounded-full text-xs font-semibold text-[#4F8EF7] shadow-sm">
                <Sparkles className="w-3.5 h-3.5" />
                Teman Belajar AI-mu
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.1] text-slate-900">
                Belajar Bersama.
                <span className="block mt-2 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] bg-clip-text text-transparent">
                  Bertumbuh Bersama.
                </span>
              </h1>

              <p className="text-base sm:text-lg text-slate-500 max-w-xl mx-auto lg:mx-0 leading-relaxed">
                Buddio menyusun peta belajar yang sesuai levelmu, menemani dengan mentor AI,
                dan membantumu memahami materi tanpa merasa sendirian.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-3">
                <Link
                  href="/register"
                  className="inline-flex items-center justify-center gap-2 w-full sm:w-auto px-7 py-3.5 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white font-bold text-sm rounded-xl shadow-md shadow-[#4F8EF7]/20 hover:scale-[1.02] hover:shadow-lg transition-all duration-300 group"
                >
                  Mulai Belajar
                  <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1 duration-200" />
                </Link>
                <a
                  href="#fitur"
                  className="inline-flex items-center justify-center gap-2 w-full sm:w-auto px-7 py-3.5 bg-white border border-slate-200 text-slate-700 font-bold text-sm rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-all duration-300"
                >
                  Lihat Cara Kerja
                </a>
              </div>

              <div className="flex flex-wrap items-center justify-center lg:justify-start gap-x-6 gap-y-2 text-xs text-slate-500">
                <span className="inline-flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-[#22C55E]" />
                  Gratis untuk memulai
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-[#22C55E]" />
                  Bahasa Indonesia
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-[#22C55E]" />
                  Adaptif sesuai jenjang
                </span>
              </div>
            </div>

            {/* Hero mock chat card */}
            <div className="flex-1 w-full max-w-md lg:max-w-none">
              <div className="bg-white border border-slate-100 rounded-3xl shadow-xl shadow-slate-200/60 p-5 sm:p-6 space-y-4">
                <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
                  <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white flex items-center justify-center text-lg font-bold shadow-md shadow-[#4F8EF7]/20">
                    B
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900">Kak Buddio</p>
                    <p className="text-[11px] text-emerald-600 font-semibold flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
                      Mentor AI online
                    </p>
                  </div>
                  <span className="ml-auto inline-flex items-center gap-1 text-[10px] font-bold text-[#7C5CFF] bg-[#7C5CFF]/8 border border-[#7C5CFF]/20 rounded-full px-2.5 py-1">
                    <GraduationCap className="w-3 h-3" />
                    SMA
                  </span>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-end">
                    <div className="max-w-[80%] px-4 py-2.5 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white text-sm rounded-2xl rounded-br-md shadow-sm">
                      Jelaskan konsep fotosintesis dong!
                    </div>
                  </div>
                  <div className="flex items-end gap-2">
                    <div className="h-7 w-7 rounded-full bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white text-[10px] font-bold flex items-center justify-center shrink-0">
                      B
                    </div>
                    <div className="max-w-[85%] px-4 py-3 bg-slate-50 border border-slate-100 text-slate-700 text-sm leading-relaxed rounded-2xl rounded-bl-md shadow-sm">
                      Bayangkan daun itu seperti dapur mini: matahari jadi kompornya, air dan udara jadi
                      bahannya, dan glukosa adalah makanannya! 🍃
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 border-t border-slate-100 pt-4">
                  <div className="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-100 rounded-xl text-slate-400 text-xs">
                    Tanya tentang materi atau minta peta belajar...
                  </div>
                  <button className="inline-flex items-center justify-center w-10 h-10 shrink-0 bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] text-white rounded-xl shadow-md shadow-[#4F8EF7]/15 transition-transform hover:scale-105">
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Trust bar */}
        <section className="border-y border-slate-100 bg-white">
          <div className="max-w-6xl mx-auto px-4 py-6 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div className="space-y-0.5">
              <p className="text-2xl font-extrabold text-slate-900">4.8/5</p>
              <p className="text-[11px] text-slate-500 flex items-center justify-center gap-1">
                <Star className="w-3.5 h-3.5 text-[#FACC15] fill-[#FACC15]" /> Kepuasan pengguna
              </p>
            </div>
            <div className="space-y-0.5">
              <p className="text-2xl font-extrabold text-slate-900">SD → Profesional</p>
              <p className="text-[11px] text-slate-500">Semua jenjang</p>
            </div>
            <div className="space-y-0.5">
              <p className="text-2xl font-extrabold text-slate-900">24/7</p>
              <p className="text-[11px] text-slate-500">Mentor AI siap bantu</p>
            </div>
            <div className="space-y-0.5">
              <p className="text-2xl font-extrabold text-slate-900">100%</p>
              <p className="text-[11px] text-slate-500">Roadmap personal</p>
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="fitur" className="max-w-6xl mx-auto px-4 py-20 sm:py-24">
          <div className="text-center space-y-3 max-w-2xl mx-auto">
            <span className="inline-flex items-center gap-1.5 text-xs font-bold text-[#4F8EF7] uppercase tracking-wider">
              <Rocket className="w-4 h-4" />
              Fitur Buddio
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">
              Semua yang kamu butuhkan untuk belajar lebih terarah
            </h2>
            <p className="text-sm text-slate-500 leading-relaxed">
              Dari menyusun peta belajar hingga berlatih soal — semuanya ditemani mentor AI yang
              memahami level belajarmu.
            </p>
          </div>

          <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {FEATURES.map((feature) => {
              const Icon = feature.icon;
              return (
                <div
                  key={feature.title}
                  className="bg-white border border-slate-100 rounded-3xl p-6 hover:shadow-lg hover:shadow-slate-200/60 hover:-translate-y-1 transition-all duration-300 group"
                >
                  <div
                    className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${feature.gradient} text-white flex items-center justify-center shadow-md transition-transform duration-300 group-hover:scale-110`}
                  >
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="mt-5 font-bold text-slate-900">{feature.title}</h3>
                  <p className="mt-2 text-xs text-slate-500 leading-relaxed">{feature.desc}</p>
                </div>
              );
            })}
          </div>
        </section>

        {/* How it works */}
        <section id="cara-kerja" className="bg-white border-y border-slate-100">
          <div className="max-w-6xl mx-auto px-4 py-20 sm:py-24">
            <div className="text-center space-y-3 max-w-2xl mx-auto">
              <span className="inline-flex items-center gap-1.5 text-xs font-bold text-[#7C5CFF] uppercase tracking-wider">
                <Target className="w-4 h-4" />
                Cara Kerja
              </span>
              <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">
                Mulai belajar dalam 3 langkah mudah
              </h2>
            </div>

            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
              {STEPS.map((step, i) => (
                <div key={step.number} className="relative bg-[#F8FAFC] border border-slate-100 rounded-3xl p-7">
                  <div className="flex items-center gap-3">
                    <span className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white text-sm font-extrabold flex items-center justify-center shadow-md shadow-[#4F8EF7]/20">
                      {step.number}
                    </span>
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                      Langkah {step.number}
                    </span>
                  </div>
                  <h3 className="mt-4 font-bold text-slate-900 text-lg">{step.title}</h3>
                  <p className="mt-2 text-sm text-slate-500 leading-relaxed">{step.desc}</p>
                  {i < STEPS.length - 1 && (
                    <ArrowRight className="hidden md:block absolute -right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-300" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] pointer-events-none" />
          <div className="absolute top-0 right-0 w-72 h-72 bg-white/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 left-0 w-72 h-72 bg-white/10 rounded-full blur-3xl pointer-events-none" />
          <div className="relative max-w-3xl mx-auto px-4 py-20 text-center">
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
              Tidak ada lagi yang belajar sendirian
            </h2>
            <p className="mt-3 text-sm sm:text-base text-white/85 leading-relaxed">
              Mulai sekarang, kamu punya teman belajar yang siap membantumu kapan saja.
            </p>
            <Link
              href="/register"
              className="mt-8 inline-flex items-center gap-2 px-8 py-4 bg-white text-[#4F8EF7] font-bold text-sm rounded-xl shadow-lg hover:scale-[1.02] hover:shadow-2xl transition-all duration-300 group"
            >
              Mulai Belajar Gratis
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1 duration-200" />
            </Link>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer id="tentang" className="bg-white border-t border-slate-100">
        <div className="max-w-6xl mx-auto px-4 py-12 flex flex-col items-center gap-6 text-center">
          <BuddioLogo size="sm" />
          <p className="text-sm text-slate-500 max-w-md">
            Buddio adalah teman belajar berbasis AI yang menemani setiap langkah perjalanan belajarmu.
          </p>
          <div className="flex items-center gap-6 text-xs font-semibold text-slate-400">
            <span className="hover:text-slate-700 transition-colors cursor-default">
              &ldquo;No one should have to learn alone.&rdquo;
            </span>
          </div>
          <div className="w-full border-t border-slate-100 pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400">
            <span>&copy; 2026 Buddio. Semua hak dilindungi.</span>
            <span>Belajar Bersama. Bertumbuh Bersama.</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
