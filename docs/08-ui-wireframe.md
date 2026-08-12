# Buddio — UI Wireframe

Versi: 1.0

Status: Locked

---

# Tujuan

Dokumen ini menjadi acuan tata letak (layout) seluruh halaman Buddio.

Fokus utama adalah membuat pengalaman belajar terasa sederhana, menyenangkan, dan terarah.

Prinsip utama:

> Satu halaman = satu tujuan utama.

---

# 1. Landing Page

```
+-----------------------------------------------------------+
| Logo Buddio                     Login   Mulai Belajar     |
+-----------------------------------------------------------+

        Teman Belajar AI untuk Semua Jenjang

      Belajar lebih terarah bersama AI Mentor

        [ Mulai Belajar ]  [ Pelajari Fitur ]

------------------------------------------------------------

📚 Roadmap Belajar

🤖 Mentor AI

📝 Cek Pemahaman

📊 Analisis Kelemahan

------------------------------------------------------------

Cara Kerja

1. Pilih Jenjang

↓

2. Pilih Topik

↓

3. AI Membuat Roadmap

↓

4. Belajar

↓

5. Evaluasi

↓

6. Naik Level

------------------------------------------------------------

Footer
```

---

# 2. Login

```
+------------------------------+

      Logo Buddio

Masuk ke akunmu

Email

_____________

Password

_____________

[Lupa Password]

[ Masuk ]

Belum punya akun?

Daftar

+------------------------------+
```

---

# 3. Register

```
+------------------------------+

      Logo

Buat Akun

Nama

Email

Password

Konfirmasi Password

[ Daftar ]

Sudah punya akun?

Masuk

+------------------------------+
```

---

# 4. Onboarding

```
+------------------------------------------------+

Selamat Datang 👋

Mari kenali tujuan belajarmu.

--------------------------------------------------

Pilih Jenjang

( ) SD

( ) SMP

( ) SMA

( ) Mahasiswa

( ) Self Learner

--------------------------------------------------

[ Lanjut ]

+------------------------------------------------+
```

---

# 5. Pilih Tujuan Belajar

```
+---------------------------------------------+

Apa tujuan belajarmu?

○ Persiapan Ujian

○ Memahami Mata Pelajaran

○ Persiapan Kuliah

○ Persiapan Kerja

○ Belajar Skill Baru

○ Lainnya

-----------------------------------------------

[ Lanjut ]

+---------------------------------------------+
```

---

# 6. Dashboard (Belum Ada Topik)

```
+--------------------------------------------------------------+

Navbar

---------------------------------------------------------------

Sidebar

🏠 Dashboard

📚 Topik

📈 Progress

👤 Profile

---------------------------------------------------------------

Halo Reiner 👋

Apa yang ingin kamu pelajari hari ini?

[ + Buat Topik Baru ]

---------------------------------------------------------------

Belum ada topik.

Mari mulai perjalanan belajarmu.

+--------------------------------------------------------------+
```

---

# 7. Dashboard (Sudah Ada Topik)

```
+--------------------------------------------------------------+

Navbar

---------------------------------------------------------------

Sidebar

🏠 Dashboard

📚 Topik

📈 Progress

👤 Profile

---------------------------------------------------------------

Halo Reiner 👋

Lanjutkan Belajar

██████████░░

Machine Learning

72%

[Lanjutkan]

---------------------------------------------------------------

Topik Aktif

Python

Kriptografi

Machine Learning

---------------------------------------------------------------

Target Minggu Ini

3 Jam

---------------------------------------------------------------

Streak

🔥 12 Hari

---------------------------------------------------------------

Quota AI

Chat

23 / 30

Roadmap

2 / 3

Quiz

5 / 5

+--------------------------------------------------------------+
```

---

# 8. Tambah Topik

```
+--------------------------------------------+

Topik Baru

Apa yang ingin kamu pelajari?

______________________

Contoh:

Python

Aljabar

Fisika

Machine Learning

Kriptografi

--------------------------------------------

Apa tujuanmu?

○ Ujian

○ Tugas

○ Skill Baru

○ Karier

--------------------------------------------

[ Buat Roadmap ]

+--------------------------------------------+
```

---

# 9. AI Sedang Membuat Roadmap

```
+-----------------------------------------------+

🤖

Sedang menyusun roadmap belajar...

██████████░░

Mohon tunggu beberapa detik.

+-----------------------------------------------+
```

---

# 10. Workspace Belajar

```
+--------------------------------------------------------------+

Navbar

---------------------------------------------------------------

Sidebar

🏠 Dashboard

📚 Topik

📈 Progress

👤 Profile

---------------------------------------------------------------

Machine Learning

---------------------------------------------------------------

Roadmap

Materi

Mentor AI

Quiz

Feedback

Catatan

---------------------------------------------------------------

Bab 1

Pengenalan Machine Learning

[Lanjut Belajar]

---------------------------------------------------------------

Progress

25%

+--------------------------------------------------------------+
```

---

# 11. Mentor AI

```
+--------------------------------------------------------------+

Machine Learning

---------------------------------------------------------------

Roadmap | Materi | Mentor AI | Quiz

---------------------------------------------------------------

🤖 Mentor AI

Halo!

Apa yang ingin kamu pelajari hari ini?

---------------------------------------------------------------

User

Apa itu supervised learning?

---------------------------------------------------------------

AI

Supervised Learning adalah...

---------------------------------------------------------------

_________________________

Ketik pertanyaan...

[ Kirim ]

+--------------------------------------------------------------+
```

---

# 12. Check Understanding

```
+--------------------------------------------------------------+

Cek Pemahaman

---------------------------------------------------------------

1.

Jelaskan apa yang dimaksud dengan Machine Learning.

_____________________

2.

Mengapa data penting?

_____________________

---------------------------------------------------------------

[ Kirim Jawaban ]

+--------------------------------------------------------------+
```

---

# 13. Feedback AI

```
+--------------------------------------------------------------+

Skor

85%

---------------------------------------------------------------

Yang sudah dipahami

✔ Dataset

✔ Model

✔ Training

---------------------------------------------------------------

Yang perlu dipelajari lagi

⚠ Evaluation

⚠ Overfitting

---------------------------------------------------------------

[ Pelajari Lagi ]

+--------------------------------------------------------------+
```

---

# 14. Progress

```
+--------------------------------------------------------------+

Progress Belajar

---------------------------------------------------------------

Jam Belajar

24 Jam

---------------------------------------------------------------

Topik

5

---------------------------------------------------------------

Quiz

21

---------------------------------------------------------------

Streak

12 Hari

---------------------------------------------------------------

Grafik Belajar

██████████

+--------------------------------------------------------------+
```

---

# 15. Profile

```
+--------------------------------------------------------------+

Foto

Nama

Email

Jenjang

Tujuan Belajar

---------------------------------------------------------------

[ Simpan ]

+--------------------------------------------------------------+
```

---

# Responsive

Desktop

Sidebar + Navbar

Tablet

Sidebar Collapse

Mobile

Bottom Navigation

Floating AI Button

---

# Design Notes

Seluruh halaman menggunakan:

- Card putih
- Background abu terang
- Radius besar
- Shadow lembut
- Ikon Lucide
- Font Plus Jakarta Sans

---

# UX Rules

Selalu tampilkan:

✔ Progress

✔ Langkah berikutnya

✔ Status belajar

✔ Sisa kuota AI

Pengguna tidak boleh bingung harus melakukan apa setelah membuka Buddio.

Setiap halaman wajib memiliki CTA utama yang jelas.