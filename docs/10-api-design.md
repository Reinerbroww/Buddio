# Buddio — API Design

Versi: 1.0

Status: Locked

---

# Tujuan

Dokumen ini mendefinisikan seluruh REST API Buddio yang digunakan oleh Frontend (Next.js) untuk berkomunikasi dengan Backend (FastAPI).

Seluruh endpoint menggunakan format JSON.

Base URL

/api/v1

---

# Authentication

## Register

POST

/auth/register

Request

{
  "full_name": "Reiner",
  "email": "reiner@gmail.com",
  "password": "********"
}

Response

{
  "message": "User berhasil dibuat"
}

---

## Login

POST

/auth/login

Request

{
  "email":"reiner@gmail.com",
  "password":"********"
}

Response

{
  "access_token":"...",
  "refresh_token":"...",
  "token_type":"Bearer"
}

---

## Refresh Token

POST

/auth/refresh

---

## Logout

POST

/auth/logout

---

# User

## Profile

GET

/users/me

Response

{
    "id":"",
    "full_name":"",
    "email":"",
    "grade_level":"SMA",
    "learning_goal":"SNBT"
}

---

## Update Profile

PUT

/users/me

---

## Change Password

PUT

/users/password

---

# Onboarding

## Pilih Jenjang

POST

/onboarding/grade-level

Request

{
   "grade_level":"Mahasiswa"
}

---

## Pilih Tujuan Belajar

POST

/onboarding/learning-goal

Request

{
   "goal":"Belajar Machine Learning"
}

---

# Topics

## Buat Topik

POST

/topics

Request

{
   "title":"Machine Learning"
}

---

## Semua Topik

GET

/topics

---

## Detail Topik

GET

/topics/{id}

---

## Hapus Topik

DELETE

/topics/{id}

---

# Roadmap

## Generate Roadmap AI

POST

/roadmaps/generate

Request

{
   "topic_id":"..."
}

Response

{
   "roadmap":"..."
}

---

## Detail Roadmap

GET

/roadmaps/{id}

---

## Checklist Step

PATCH

/roadmaps/steps/{id}

Request

{
   "completed":true
}

---

# Lesson

## Ambil Materi

GET

/lessons/{id}

---

## Tandai Selesai

PATCH

/lessons/{id}/complete

---

# AI Mentor

## Chat

POST

/mentor/chat

Request

{
   "topic_id":"...",
   "message":"Apa itu supervised learning?"
}

Response

{
   "answer":"..."
}

---

## History Chat

GET

/mentor/history/{topic_id}

---

## Hapus History

DELETE

/mentor/history/{topic_id}

---

# Assessment

## Generate Quiz

POST

/assessment/generate

Request

{
    "topic_id":"..."
}

---

## Submit Quiz

POST

/assessment/submit

---

## Feedback AI

GET

/assessment/{attempt_id}

---

# Progress

## Progress User

GET

/progress

---

## Progress Topik

GET

/progress/{topic_id}

---

## Statistik

GET

/progress/statistics

Response

{
   "study_hours":25,
   "topics":4,
   "streak":12,
   "completion":74
}

---

# AI Usage

## Sisa Quota

GET

/usage

Response

{
   "chat_remaining":25,
   "roadmap_remaining":2,
   "quiz_remaining":4
}

---

## Riwayat Penggunaan

GET

/usage/history

---

# Settings

GET

/settings

PUT

/settings

---

# Notification

GET

/notifications

PUT

/notifications/read

---

# Health

GET

/health

Response

{
   "status":"healthy"
}

---

# Error Response

400

{
   "message":"Bad Request"
}

401

{
   "message":"Unauthorized"
}

403

{
   "message":"Forbidden"
}

404

{
   "message":"Data tidak ditemukan"
}

500

{
   "message":"Internal Server Error"
}

---

# Endpoint Summary

Authentication

POST   /auth/register

POST   /auth/login

POST   /auth/logout

POST   /auth/refresh

-----------------------------------

Users

GET    /users/me

PUT    /users/me

PUT    /users/password

-----------------------------------

Onboarding

POST   /onboarding/grade-level

POST   /onboarding/learning-goal

-----------------------------------

Topics

POST   /topics

GET    /topics

GET    /topics/{id}

DELETE /topics/{id}

-----------------------------------

Roadmaps

POST   /roadmaps/generate

GET    /roadmaps/{id}

PATCH  /roadmaps/steps/{id}

-----------------------------------

Lessons

GET    /lessons/{id}

PATCH  /lessons/{id}/complete

-----------------------------------

Mentor

POST   /mentor/chat

GET    /mentor/history/{topic_id}

DELETE /mentor/history/{topic_id}

-----------------------------------

Assessment

POST   /assessment/generate

POST   /assessment/submit

GET    /assessment/{attempt_id}

-----------------------------------

Progress

GET    /progress

GET    /progress/{topic_id}

GET    /progress/statistics

-----------------------------------

Usage

GET    /usage

GET    /usage/history

-----------------------------------

Settings

GET    /settings

PUT    /settings

-----------------------------------

Notification

GET    /notifications

PUT    /notifications/read

-----------------------------------

Health

GET    /health
