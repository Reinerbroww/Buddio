import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 font-sans flex flex-col items-center justify-center gap-4 px-4 text-center">
      <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#4F8EF7] to-[#7C5CFF] text-white flex items-center justify-center text-2xl font-extrabold shadow-md shadow-[#4F8EF7]/20">
        404
      </div>
      <p className="text-sm text-slate-500 max-w-xs leading-relaxed">
        Halaman yang kamu cari tidak ditemukan.
      </p>
      <Link
        href="/"
        className="mt-2 inline-flex items-center px-5 py-2.5 text-sm font-bold bg-gradient-to-r from-[#4F8EF7] to-[#7C5CFF] hover:scale-[1.02] text-white rounded-xl shadow-md shadow-[#4F8EF7]/15 transition-all"
      >
        Kembali ke Beranda
      </Link>
    </div>
  );
}
