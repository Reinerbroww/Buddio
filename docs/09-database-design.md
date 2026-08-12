# Buddio — Database Design

Versi: 1.0

Status: Locked

---

# Tujuan

Dokumen ini mendefinisikan struktur database Buddio menggunakan PostgreSQL.

Seluruh data pengguna, roadmap, progress belajar, chat AI, hingga penggunaan quota disimpan pada database ini.

---

# Entity Relationship Overview

User
│
├── Topics
│     ├── Roadmaps
│     │      └── Roadmap Steps
│     │
│     ├── Lessons
│     │
│     ├── Quiz
│     │      └── Quiz Attempt
│     │
│     └── Chat Session
│             └── Chat Message
│
├── Progress
│
├── AI Usage
│
└── User Settings

---

# Tabel

## users

Menyimpan akun pengguna.

Kolom

- id (UUID)
- full_name
- email
- password_hash
- grade_level
- learning_goal
- avatar
- created_at
- updated_at

---

## topics

Topik belajar yang dibuat user.

Contoh:

- Python
- Matematika
- Machine Learning

Kolom

- id
- user_id
- title
- description
- status
- created_at

Relasi

Many Topics → One User

---

## roadmaps

Roadmap AI.

Kolom

- id
- topic_id
- title
- difficulty
- estimated_hours
- created_at

---

## roadmap_steps

Isi roadmap.

Contoh

Step 1

Belajar Variabel

Step 2

Belajar Loop

Step 3

Function

Kolom

- id
- roadmap_id
- order_number
- title
- description
- completed

---

## lessons

Materi belajar.

Kolom

- id
- roadmap_step_id
- content
- source
- created_at

---

## chat_sessions

Riwayat chat.

Kolom

- id
- topic_id
- title
- created_at

---

## chat_messages

Semua percakapan AI.

Kolom

- id
- session_id
- role

(user / assistant)

- message
- token_usage
- created_at

---

## quizzes

Quiz AI.

Kolom

- id
- topic_id
- title
- generated_by_ai
- created_at

---

## quiz_questions

Daftar soal.

Kolom

- id
- quiz_id
- question
- answer_key
- explanation

---

## quiz_attempts

Jawaban user.

Kolom

- id
- quiz_id
- user_id
- score
- feedback
- created_at

---

## progress

Progress belajar.

Kolom

- id
- user_id
- topic_id

completion_percentage

study_minutes

last_access

current_step

---

## ai_usage

Quota AI.

Kolom

- id

user_id

chat_used

quiz_used

roadmap_used

reset_date

---

## user_settings

Pengaturan akun.

Kolom

- id

user_id

theme

notification

language

daily_goal

---

# Relationship

User

1

↓

Topics

1

↓

Roadmap

1

↓

Roadmap Steps

1

↓

Lessons

Quiz

Chat

Progress

---

# Index

users.email

topics.user_id

roadmaps.topic_id

chat_messages.session_id

quiz_attempts.user_id

---

# Future Tables

documents

embeddings

flashcards

achievements

leaderboard

badges

subscription

payments