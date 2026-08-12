# Buddio — User Flow

Versi: 1.0

Status: Locked

---

# Tujuan

Dokumen ini menjelaskan perjalanan pengguna (User Journey) dari pertama kali membuka Buddio hingga berhasil menyelesaikan proses belajar.

Tujuan utama Buddio bukan hanya menjawab pertanyaan, tetapi membimbing pengguna melalui proses belajar yang terarah.

---

# User Journey

Landing Page

↓

Register / Login

↓

Pilih Jenjang

↓

Dashboard

↓

Pilih Topik Belajar

↓

Workspace Belajar

↓

Belajar Materi

↓

Chat Mentor AI

↓

Check Understanding

↓

AI Feedback

↓

Weakness Analysis

↓

Rekomendasi Selanjutnya

↓

Lanjut Belajar

---

# Flow 1 — Pengguna Baru

Landing Page

↓

Klik "Mulai Belajar"

↓

Register

↓

Verifikasi akun (opsional MVP)

↓

Login

↓

Masuk ke Onboarding

↓

Pilih Jenjang

↓

Masuk Dashboard

---

# Flow 2 — Login

Landing Page

↓

Klik Login

↓

Masukkan Email

↓

Password

↓

Berhasil Login

↓

Dashboard

---

# Flow 3 — Onboarding

Tujuan onboarding adalah memahami kebutuhan belajar pengguna.

Langkah:

1. Pilih Jenjang

- SD
- SMP
- SMA
- Mahasiswa
- Self Learner

↓

2. Pilih Tujuan Belajar

Contoh:

- Persiapan Ujian
- Memahami Mata Pelajaran
- Belajar Skill Baru
- Persiapan Kuliah
- Persiapan Kerja

↓

3. Selesai

↓

Dashboard

---

# Dashboard

Dashboard menjadi pusat aktivitas belajar.

Informasi utama:

- Sapaan personal
- Progress belajar
- Topik yang sedang dipelajari
- Riwayat belajar
- Sisa kuota AI
- Target belajar minggu ini
- Streak belajar

Dashboard tidak menampilkan chat AI secara langsung.

---

# Flow Memulai Belajar

Dashboard

↓

Klik

"Belajar Topik Baru"

↓

Masukkan nama topik

Contoh:

- Aljabar
- Python
- Machine Learning
- Kriptografi

↓

AI membuat roadmap belajar

↓

Roadmap tersimpan

↓

Masuk Workspace

---

# Workspace Belajar

Workspace adalah halaman utama proses belajar.

Terdiri dari:

- Roadmap
- Materi
- Chat Mentor
- Quiz
- Catatan
- Progress

Workspace hanya berfokus pada satu topik belajar.

---

# Flow Belajar

Pilih Bab

↓

Baca Materi

↓

Tanya Mentor AI

↓

Lanjut Bab Berikutnya

↓

Selesai

↓

Update Progress

---

# Flow Chat Mentor

Masuk Workspace

↓

Klik Mentor AI

↓

Tulis Pertanyaan

↓

AI menjawab sesuai jenjang

↓

Pengguna dapat bertanya kembali

↓

Riwayat chat disimpan

---

# Flow Check Understanding

Selesai belajar materi

↓

Klik

"Cek Pemahaman"

↓

AI membuat beberapa pertanyaan

↓

Pengguna menjawab

↓

AI mengevaluasi jawaban

↓

Skor pemahaman

↓

Feedback

↓

Weakness Analysis

---

# Flow Weakness Analysis

AI menganalisis:

- Konsep yang belum dipahami
- Kesalahan berpikir
- Materi yang perlu diulang

↓

Menampilkan rekomendasi

↓

Pengguna dapat mengulang materi

---

# Flow Progress

Setiap aktivitas akan memperbarui:

- Persentase roadmap
- Jam belajar
- Streak
- Target mingguan
- Quiz yang telah selesai

---

# Flow AI Quota

Setiap penggunaan AI akan mengurangi kuota.

Jenis kuota:

- Chat Mentor
- Generate Roadmap
- Generate Quiz

Dashboard selalu menampilkan sisa kuota.

Jika habis:

Pengguna tetap dapat membuka materi yang telah dimiliki.

Namun tidak dapat menggunakan AI hingga kuota kembali.

---

# Flow Profile

Dashboard

↓

Profile

↓

Edit Nama

↓

Edit Foto

↓

Ganti Password

↓

Pilih Jenjang (opsional)

↓

Simpan

---

# Flow Logout

Klik Avatar

↓

Logout

↓

Kembali ke Landing Page

JWT dihapus dari browser.

---

# Error Flow

Tidak ada koneksi internet

↓

Tampilkan pesan ramah

↓

"Coba lagi"

---

Quota AI habis

↓

Tampilkan informasi

↓

Kuota akan kembali besok.

---

Server Error

↓

Tampilkan pesan

↓

Ups!

Terjadi kendala pada server.

Silakan coba beberapa saat lagi.

---

# Prinsip User Experience

Buddio selalu membantu pengguna mengetahui langkah belajar berikutnya.

Pengguna tidak boleh merasa bingung harus melakukan apa.

Setiap halaman harus memiliki CTA yang jelas.

Contoh:

"Lanjut Belajar"

"Kerjakan Quiz"

"Pelajari Bab Berikutnya"

"Cek Pemahaman"

---

# Goal

Setelah menggunakan Buddio, pengguna harus merasa:

✔ Aku tahu harus belajar apa.

✔ Aku tahu sudah sejauh mana.

✔ Aku tahu bagian mana yang masih kurang.

✔ Aku tahu langkah berikutnya.

✔ Aku tidak belajar sendirian.