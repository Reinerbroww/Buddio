"""Rule-based AI fallback used when no Gemini API key is configured or the API call fails.

These generators produce plausible, topic-aware content so the full MVP remains testable
without any external AI dependency. The API responses include `mode: "mock"` so the UI
can clearly label generated content.
"""

ROADMAP_TEMPLATES = [
    ("Pengenalan {t}", "Pahami konsep dasar, istilah penting, dan gambaran umum tentang {t}."),
    ("Konsep Inti {t}", "Pelajari prinsip dan ide utama yang menjadi fondasi {t}."),
    ("Latihan Terpandu", "Kerjakan latihan bertahap untuk menguji pemahaman dasar kamu tentang {t}."),
    ("Studi Kasus & Penerapan", "Terapkan pengetahuan {t} pada contoh nyata dan studi kasus sederhana."),
    ("Evaluasi & Penguatan", "Ukur pemahamanmu dengan kuis singkat dan ulangi bagian yang masih lemah."),
]

QUIZ_TEMPLATES = [
    {
        "question": "Apa langkah pertama yang tepat saat mempelajari {t}?",
        "options": ["Memahami konsep dasar dan istilah penting", "Langsung mengerjakan soal sulit", "Menghafal semua rumus tanpa konteks", "Melompat ke materi lanjutan"],
        "answer_index": 0,
        "explanation": "Memahami konsep dasar dulu membangun fondasi yang kuat sebelum masuk ke bagian yang lebih dalam.",
    },
    {
        "question": "Apa manfaat utama membuat roadmap belajar untuk {t}?",
        "options": ["Belajar lebih terarah dan terukur", "Menghilangkan kebutuhan latihan", "Menghindari praktik sama sekali", "Menghafal tanpa memahami"],
        "answer_index": 0,
        "explanation": "Roadmap memberi jalur yang jelas sehingga progres belajarmu terarah dan mudah diukur.",
    },
    {
        "question": "Metode terbaik untuk menguatkan pemahaman {t} adalah…",
        "options": ["Latihan soal secara bertahap", "Membaca sekali lalu menyerah", "Menunda sampai ujian", "Hanya menonton video"],
        "answer_index": 0,
        "explanation": "Latihan bertahap adalah cara paling efektif untuk memperkuat pemahaman konsep.",
    },
    {
        "question": "Bagaimana cara mengecek pemahaman kamu setelah belajar {t}?",
        "options": ["Mengerjakan kuis dan meninjau kesalahan", "Tidak perlu mengecek", "Mengulang soal yang sama tanpa umpan balik", "Menghafal jawaban orang lain"],
        "answer_index": 0,
        "explanation": "Kuis dengan umpan balik membantu menemukan topik yang masih lemah untuk diulang.",
    },
    {
        "question": "Apa yang harus dilakukan jika ada konsep {t} yang belum dipahami?",
        "options": ["Tanya ke mentor AI dan minta penjelasan ulang", "Mengabaikannya", "Pindah topik tanpa memahami", "Berhenti belajar"],
        "answer_index": 0,
        "explanation": "Mentor AI siap membantu menjelaskan ulang konsep yang sulit dengan bahasa yang sesuai jenjangmu.",
    },
]

MOCK_GREETING = "Halo! Aku Kak Buddio, mentor belajarmu. Aku dalam mode demo (tanpa kunci API AI), jadi jawaban ini adalah contoh. Jika kamu ingin jawaban yang lebih pintar dan personal, tambahkan GEMINI_API_KEY di file .env."


def _expand(template: str, topic: str) -> str:
    return template.replace("{t}", topic)


def mock_roadmap(topic_title: str, goal: str = "") -> dict:
    steps = [
        {"order_number": i + 1, "title": _expand(t[0], topic_title), "description": _expand(t[1], topic_title)}
        for i, t in enumerate(ROADMAP_TEMPLATES)
    ]
    title = f"Roadmap {topic_title}"
    if goal:
        title = f"Roadmap {topic_title} — {goal}"
    return {
        "title": title,
        "difficulty": "Menengah",
        "estimated_hours": len(steps) * 2,
        "steps": steps,
    }


def mock_quiz(topic_title: str, count: int = 5) -> dict:
    questions = []
    templates = (QUIZ_TEMPLATES * ((count // len(QUIZ_TEMPLATES)) + 1))[:count]
    for i, tpl in enumerate(templates, start=1):
        q = dict(tpl)
        q["question"] = _expand(q["question"], topic_title)
        q["explanation"] = _expand(q["explanation"], topic_title)
        questions.append(q)
    return {
        "title": f"Kuis {topic_title}",
        "questions": questions,
    }


def mock_chat(message: str, topic_title: str) -> str:
    return (
        f"Hmm, pertanyaan bagus tentang {topic_title}! (Mode demo)\n\n"
        f"Kamu bertanya: \"{message}\"\n\n"
        f"Sebagai panduan umum: coba pecah masalahmu menjadi bagian kecil, pelajari konsep dasarnya dulu, "
        f"lalu berlatih dengan contoh soal. Untuk jawaban yang lebih spesifik dan personal, "
        f"aktifkan GEMINI_API_KEY di file .env — nanti aku bisa jelaskan sesuai jenjang dan materimu."
    )
