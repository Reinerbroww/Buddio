# Buddio — AI Design

Versi: 1.0

Status: Locked

---

# Tujuan

Dokumen ini menjelaskan bagaimana sistem AI Buddio bekerja.

Buddio bukan sekadar AI chatbot, tetapi AI Learning Companion yang mendampingi pengguna dari awal hingga menguasai suatu materi.

---

# Filosofi AI Buddio

Sebagian besar AI berkata:

"Silakan bertanya apa saja."

Buddio berkata:

"Mari kita belajar bersama."

Perbedaan utama Buddio adalah AI selalu berusaha membimbing proses belajar, bukan hanya menjawab pertanyaan.

---

# AI Pipeline

User

↓

Login

↓

Pilih Jenjang

↓

Pilih Tujuan Belajar

↓

Pilih Topik

↓

Generate Roadmap

↓

Belajar

↓

Assessment

↓

Analisis Kelemahan

↓

Rekomendasi Selanjutnya

↓

Belajar Lagi

---

# AI Modules

Buddio terdiri dari beberapa AI Module.

1. Roadmap Generator

2. AI Mentor

3. Assessment Generator

4. Understanding Evaluator

5. Weakness Analyzer

6. Recommendation Engine

Semua modul saling terhubung.

---

# 1. Roadmap Generator

Input

Jenjang

Topik

Tujuan belajar

Output

Roadmap belajar bertahap.

Contoh

Machine Learning

↓

1. Python Dasar

2. Numpy

3. Statistik

4. Regression

5. Classification

6. Clustering

7. Project

---

Roadmap selalu disesuaikan dengan:

- Jenjang

- Tujuan belajar

- Progress pengguna

---

# 2. AI Mentor

AI Mentor bertugas menjadi teman belajar.

Bukan sekadar menjawab.

Tetapi juga:

✔ memberi analogi

✔ memberi contoh

✔ bertanya balik

✔ memotivasi

✔ membantu ketika bingung

---

AI Mentor memiliki persona.

Ramah.

Sabar.

Tidak menghakimi.

Selalu mendorong pengguna berpikir.

---

# 3. Adaptive Response

Semua jawaban AI berubah sesuai jenjang.

Contoh pertanyaan:

Apa itu fotosintesis?

SD

↓

Bahasa sederhana

Banyak analogi

Kalimat pendek

---

SMP

↓

Penjelasan lebih rinci

Mulai mengenalkan istilah ilmiah

---

SMA

↓

Menggunakan istilah biologi

Proses kimia dijelaskan

---

Mahasiswa

↓

Lebih akademik

Lebih mendalam

Boleh menggunakan referensi ilmiah

---

Self Learner

↓

Fleksibel

Menyesuaikan tujuan pengguna

---

# 4. Assessment Generator

Setelah belajar AI membuat evaluasi.

Jenis soal

Essay

Pilihan ganda

Studi kasus

Open-ended question

Prioritas utama adalah soal konseptual.

---

# 5. Understanding Evaluator

Berbeda dengan chatbot biasa.

AI tidak hanya memeriksa benar atau salah.

AI mengevaluasi:

Pemahaman konsep

Cara berpikir

Kesalahan logika

Kelengkapan jawaban

Contoh Feedback

✔ Sudah memahami konsep dasar.

⚠ Masih keliru membedakan Regression dan Classification.

---

# 6. Weakness Analyzer

Setiap hasil assessment disimpan.

AI mencari pola.

Misalnya:

Quiz 1

Nilai rendah

Statistik

Quiz 2

Masih salah

Statistik

Quiz 3

Masih salah

Statistik

↓

AI menyimpulkan

"Kamu masih kesulitan pada konsep Statistik."

---

# 7. Recommendation Engine

Setelah AI mengetahui kelemahan pengguna.

AI menentukan langkah berikutnya.

Misalnya

Belajar ulang

↓

Video

↓

Latihan

↓

Quiz

↓

Naik level

---

# AI Memory

AI mengingat:

Topik yang dipelajari

Roadmap

Progress

Nilai quiz

Riwayat chat

Kesalahan yang sering muncul

Tujuan belajar

Namun AI tidak menyimpan data sensitif di dalam prompt.

---

# Prompt Builder

Setiap request ke AI dibangun dari beberapa bagian.

System Prompt

+

Jenjang

+

Tujuan Belajar

+

Roadmap

+

Progress

+

Pertanyaan User

↓

LLM

↓

Jawaban

---

# Guardrails

AI tidak boleh:

Memberikan jawaban berbahaya

Menghina pengguna

Menyelesaikan ujian secara curang

Memberikan informasi yang tidak sesuai usia

Mengabaikan jenjang pengguna

---

# AI Usage Flow

Chat

↓

Hitung quota

↓

Bangun Prompt

↓

Kirim ke Gemini

↓

Terima Response

↓

Simpan History

↓

Update Progress

↓

Kirim ke Frontend

---

# Future AI

Flashcard Generator

Mind Map Generator

Learning Style Detection

Voice Tutor

OCR Homework

PDF Learning

Image Understanding

Adaptive Quiz Difficulty

Spaced Repetition

Gamification AI

---

# Success Metrics

Roadmap berhasil dibuat

Response < 5 detik

Assessment akurat

Feedback relevan

Rekomendasi sesuai progress

Pengguna merasa didampingi selama belajar

---

# Visi AI Buddio

AI bukan pengganti guru.

AI bukan mesin pencari.

AI adalah teman belajar yang memahami setiap perjalanan belajar penggunanya.

"No one should have to learn alone."