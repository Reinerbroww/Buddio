# Buddio — Information Architecture

Versi: 1.0

Status: Locked

---

# Tujuan

Dokumen ini menjelaskan struktur halaman (Information Architecture) Buddio.

Setiap halaman memiliki fungsi yang jelas sehingga pengguna selalu mengetahui posisi dan langkah belajar berikutnya.

---

# Struktur Aplikasi

Landing Page

├── Login

├── Register

├── Dashboard

│

├── Workspace Belajar

│ ├── Roadmap

│ ├── Materi

│ ├── Mentor AI

│ ├── Quiz

│ ├── Feedback

│ └── Catatan

│

├── Progress

│

├── Riwayat Belajar

│

├── Profile

│

└── Settings

---

# Landing Page

Tujuan

Mengenalkan Buddio kepada pengguna.

Menu

- Home
- Fitur
- Cara Kerja
- Tentang
- Login
- Mulai Belajar

CTA

Mulai Belajar

---

# Authentication

Halaman:

Login

Register

Forgot Password (Future)

Reset Password (Future)

---

# Onboarding

Halaman ini hanya muncul sekali.

Informasi yang dikumpulkan:

Nama

Jenjang

Tujuan Belajar

Minat

---

# Dashboard

Dashboard merupakan pusat aktivitas pengguna.

Widget yang ditampilkan:

- Greeting
- Continue Learning
- Progress Mingguan
- AI Quota
- Learning Streak
- Topik Aktif
- Aktivitas Terakhir
- Rekomendasi Topik

---

# Workspace

Workspace adalah tempat seluruh proses belajar berlangsung.

Workspace terdiri dari beberapa tab.

Roadmap

Materi

Mentor AI

Quiz

Feedback

Catatan

Progress

---

# Roadmap

Berisi:

Daftar Bab

Status

Persentase

Estimasi waktu

Target selesai

---

# Materi

Berisi:

Judul

Isi Materi

Ringkasan

Contoh

Ilustrasi

Referensi

---

# Mentor AI

Berisi:

Chat

Riwayat

Prompt

Saran pertanyaan

---

# Quiz

Berisi:

Soal

Jawaban

Pembahasan

Nilai

---

# Feedback

Berisi:

Skor

Analisis AI

Kelebihan

Kelemahan

Rekomendasi

---

# Progress

Berisi:

Jam belajar

Topik selesai

Roadmap selesai

Quiz selesai

Streak

Target Mingguan

Grafik belajar

---

# Riwayat Belajar

Menampilkan:

Topik yang pernah dipelajari

Tanggal

Durasi

Progress

---

# Profile

Data pengguna

Foto

Nama

Email

Jenjang

Tujuan Belajar

---

# Settings

Pengaturan aplikasi.

Dark Mode (Future)

Bahasa (Future)

Notifikasi

Privasi

Logout

---

# Navigation

Desktop

Navbar

Sidebar

Workspace Tabs

---

Mobile

Bottom Navigation

Hamburger Menu

---

# Global Components

Navbar

Sidebar

Search

Notification

Avatar

Toast

Modal

Loading

Breadcrumb

---

# Footer

Tentang

Kebijakan Privasi

Syarat Penggunaan

Kontak

Media Sosial

---

# AI Components

Generate Roadmap

Chat Mentor

Generate Quiz

Check Understanding

Weakness Analysis

Learning Recommendation

---

# Database Modules

Authentication

Users

Subjects

Roadmaps

Lessons

Quizzes

Chats

Progress

Quotas

---

# Future Modules

Achievement

Leaderboard

Study Group

Gamification

Marketplace Materi

Teacher Dashboard

Parent Dashboard

---

# Navigation Rules

Landing Page tidak memiliki Sidebar.

Dashboard memiliki Sidebar.

Workspace memiliki Sidebar + Tab Navigation.

Semua halaman memiliki Breadcrumb.

---

# Search

Search global hanya tersedia setelah login.

Search dapat mencari:

Topik

Materi

Roadmap

Riwayat

---

# Notification

Menampilkan:

Roadmap selesai

Quiz selesai

Target mingguan

Pengingat belajar

---

# Design Rules

Setiap halaman maksimal memiliki satu tujuan utama.

Tidak ada halaman yang menampilkan terlalu banyak informasi.

Selalu ada CTA yang jelas.

---

# Goal

Pengguna selalu tahu:

Di mana posisinya.

Apa yang sedang dipelajari.

Apa langkah berikutnya.

Berapa progresnya.

Berapa sisa kuota AI.