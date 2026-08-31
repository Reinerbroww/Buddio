"""Rule-based AI fallback used when no Gemini API key is configured or the API call fails.

These generators produce plausible, topic-aware content so the full MVP remains testable
without any external AI dependency. The API responses include `mode: "mock"` so the UI
can clearly label generated content.
"""
import re


# ---------------------------------------------------------------------------
# Subject detection helpers
# ---------------------------------------------------------------------------

_PHYSICS_KW = {"relativitas", "fisika", "mekanika", "termo", "optik", "gelombang", "listrik", "magnet", "gravitasi", "kuantum", "newton", "kecepatan", "gaya", "energi", "kinetik", "potensial", "medan", "kemagnetan", "supra"}
_MATH_KW = {"aljabar", "geometri", "kalkulus", "integral", "turunan", "matriks", "vektor", "statistika", "probabilitas", "persamaan", "fungsi", "trigonometri", "logaritma", "limit", "deret", "combinatorics", "linear"}
_CS_KW = {"algoritma", "pemrograman", "struktur data", "database", "jaringan", "operating system", "os", "compiler", "software", "hardware", "internet", "web", "api", "oop", "object oriented", "binary", "sorting", "searching"}
_DATA_KW = {"machine learning", "data", "preprocessing", "feature", "deep learning", "neural", "regression", "classification", "clustering", "scikit", "tensorflow", "pandas", "dataset", "model", "training", "testing", "overfitting"}
_HISTORY_KW = {"sejarah", "peristiwa", "kerajaan", "kolonial", "kemerdekaan", "revolusi", "perang", "tokoh", "zaman", "abad", "masa"}
_LANG_KW = {"bahasa", "grammar", "tata bahasa", "sintaksis", "semantik", "morfologi", "pragmatik"}
_CHEM_KW = {"kimia", "reaksi", "atom", "molekul", "periodik", "asam", "bas", "larutan", "stoikiometri", "redoks", "elektrokimia"}
_ECON_KW = {"ekonomi", "mikro", "makro", "inflasi", "gdp", "pasar", "penawaran", "permintaan", "moneter", "fiskal", "investasi", "suku bunga"}
_BIO_KW = {"biologi", "sel", "dna", "rna", "protein", "evolusi", "ekosistem", "genetika", "metabolisme", "anatomi", "fisiologi", "fotosintesis"}
_PROG_KW = {"pemrograman", "python", "javascript", "typescript", "java", "c++", "rust", "golang", "php", "ruby", "swift", "kotlin", "react", "nextjs", "node", "django", "flask", "laravel"}


def _detect_subject(title: str) -> str:
    t = title.lower()
    # Programming (languages/frameworks) is the most specific — check first.
    for kw in _PROG_KW:
        if kw in t:
            return "programming"
    for kw in _PHYSICS_KW:
        if kw in t:
            return "physics"
    for kw in _MATH_KW:
        if kw in t:
            return "math"
    for kw in _CS_KW:
        if kw in t:
            return "cs"
    for kw in _DATA_KW:
        if kw in t:
            return "data"
    for kw in _CHEM_KW:
        if kw in t:
            return "chemistry"
    for kw in _HISTORY_KW:
        if kw in t:
            return "history"
    for kw in _LANG_KW:
        if kw in t:
            return "language"
    for kw in _ECON_KW:
        if kw in t:
            return "economics"
    for kw in _BIO_KW:
        if kw in t:
            return "biology"
    return "general"


# ---------------------------------------------------------------------------
# Roadmap generation
# ---------------------------------------------------------------------------

_ROADMAP_PATTERNS = {
    "physics": [
        ("Pengenalan {t}", "Konsep dasar, terminologi penting, dan prinsip utama {t}."),
        ("Hukum & Rumus Inti", "Rumus-rumus utama yang menjadi fondasi {t}, penurunan sederhana, dan makna setiap variabel."),
        ("Analisis Masalah", "Cara menerapkan rumus dan hukum {t} pada berbagai skenario fisika nyata."),
        ("Latihan Terpandu", "Soal-soal bertingkat tentang {t} dari mudah ke sulit dengan pembahasan langkah demi langkah."),
        ("Penerapan Nyata", "Studi kasus penggunaan {t} dalam teknologi atau kehidupan sehari-hari."),
        ("Evaluasi & Penguatan", "Kuis evaluasi dan ringkasan poin-poin kunci untuk menguji pemahaman {t} secara menyeluruh."),
    ],
    "math": [
        ("Konsep Dasar", "Definisi, notasi, dan intuisi di balik konsep {t}."),
        ("Aturan & Sifat", "Sifat-sifat matematika, aturan operasi, dan bukti sederhana terkait {t}."),
        ("Teknik Penyelesaian", "Langkah-langkah sistematis menyelesaikan masalah menggunakan {t}."),
        ("Contoh Kerja Lengkap", "Perhitungan tuntas dari awal hingga hasil akhir untuk berbagai tipe soal {t}."),
        ("Latihan & Tantangan", "Soal latihan bertingkat dari dasar hingga tantangan untuk mengasah keterampilan."),
        ("Ringkasan & Penguatan", "Poin-poin kunci, kesalahan umum, dan tips mengingat {t}."),
    ],
    "cs": [
        ("Pengenalan {t}", "Konsep dasar, terminologi, dan gambaran umum {t}."),
        ("Mekanisme Kerja", "Bagaimana {t} bekerja di balik layar, step-by-step."),
        ("Penerapan Praktis", "Contoh implementasi {t} dalam proyek nyata atau kode."),
        ("Latihan Coding", "Soal praktis dan tantangan coding terkait {t}."),
        ("Optimasi & Best Practice", "Tips menulis kode yang efisien, rapi, dan terstandarisasi untuk {t}."),
        ("Evaluasi", "Kuis dan review pemahaman tentang {t}."),
    ],
    "data": [
        ("Pengenalan {t}", "Konsep dasar, terminologi, dan gambaran besar {t}."),
        ("Metode & Algoritma", "Teknik dan algoritma inti yang digunakan dalam {t}."),
        ("Worked Example", "Contoh implementasi lengkap dari awal hingga hasil akhir menggunakan {t}."),
        ("Evaluasi Model", "Cara mengukur dan mengevaluasi performa model {t}."),
        ("Tantangan Umum", "Kesalahan sering terjadi dan cara mengatasinya dalam {t}."),
        ("Proyek Mini", "Proyek kecil praktis untuk menerapkan pengetahuan {t}."),
    ],
    "programming": [
        ("Setup & Pengenalan", "Cara menyiapkan lingkungan dan memahami konsep dasar {t}."),
        ("Syntax & Fitur Inti", "Syntax, tipe data, dan fitur-fitur utama {t}."),
        ("Kontrol Alur & Fungsi", "Percabangan, perulangan, dan pembuatan fungsi dalam {t}."),
        ("Struktur Data", "Struktur data dasar dan cara menggunakannya dalam {t}."),
        ("Proyek Mini", "Membangun aplikasi kecil untuk mempraktikkan {t}."),
        ("Best Practice", "Penulisan kode bersih, testing, dan konvensi dalam {t}."),
    ],
    "history": [
        ("Latar Belakang", "Konteks sejarah dan kondisi yang melatarbelakangi {t}."),
        ("Peristiwa Utama", "Urutan peristiwa penting dalam {t} secara kronologis."),
        ("Tokoh & Faktor Kunci", "Tokoh-tokoh berpengaruh dan faktor penyebab {t}."),
        ("Dampak & Akibat", "Pengaruh {t} terhadap perkembangan masyarakat/bangsa/dunia."),
        ("Analisis Kritis", "Berbagai perspektif dan pandangan sejarawan tentang {t}."),
        ("Penguatan & Evaluasi", "Rangkuman, peta konsep, dan kuis untuk menguji pemahaman {t}."),
    ],
    "chemistry": [
        ("Pengenalan {t}", "Konsep dasar, terminologi, dan model partikel terkait {t}."),
        ("Sifat & Golongan", "Karakteristik, golongan, dan sifat-sifat penting dalam {t}."),
        ("Reaksi & Persamaan", "Jenis-jenis reaksi kimia dan cara menyelesaikan persamaan reaksi {t}."),
        ("Contoh Kerja", "Perhitungan stoikiometri dan penerapan konsep {t} langkah demi langkah."),
        ("Penerapan Nyata", "Aplikasi {t} dalam industri, lingkungan, atau kehidupan sehari-hari."),
        ("Evaluasi", "Kuis dan latihan soal untuk menguji pemahaman {t}."),
    ],
    "biology": [
        ("Pengenalan {t}", "Konsep dasar, struktur, dan terminologi biologi terkait {t}."),
        ("Mekanisme Biologi", "Proses dan mekanisme yang terjadi dalam {t} secara step-by-step."),
        ("Penerapan & Observasi", "Cara mengamati dan menerapkan pengetahuan {t} dalam praktikum atau kehidupan."),
        ("Interaksi & Sistem", "Bagaimana {t} terhubung dengan sistem biologi lainnya."),
        ("Latihan & Soal", "Soal-soal biologi bertingkat dengan pembahasan lengkap."),
        ("Ringkasan", "Poin-poin kunci dan penguatan pemahaman tentang {t}."),
    ],
    "economics": [
        ("Pengenalan {t}", "Konsep dasar dan prinsip utama dalam {t}."),
        ("Model & Teori", "Model ekonomi dan teori yang menjelaskan {t}."),
        ("Data & Indikator", "Indikator ekonomi utama yang relevan dengan {t}."),
        ("Studi Kasus", "Penerapan teori {t} pada kondisi ekonomi nyata."),
        ("Latihan & Analisis", "Soal dan analisis kasus untuk mengasah pemahaman {t}."),
        ("Ringkasan", "Poin-poin kunci dan kesimpulan tentang {t}."),
    ],
    "language": [
        ("Pengenalan {t}", "Konsep dasar dan terminologi terkait {t}."),
        ("Aturan & Pola", "Aturan tata bahasa, pola kalimat, dan penggunaan {t}."),
        ("Contoh Penggunaan", "Contoh kalimat dan aplikasi {t} dalam konteks berbeda."),
        ("Latihan", "Latihan menulis, membaca, atau memahami {t}."),
        ("Penguatan", "Tips mengingat dan menerapkan {t} dalam komunikasi sehari-hari."),
        ("Evaluasi", "Kuis dan tes pemahaman tentang {t}."),
    ],
    "general": [
        ("Pengenalan {t}", "Konsep dasar, terminologi, dan gambaran umum tentang {t}."),
        ("Konsep Inti", "Prinsip dan ide utama yang menjadi fondasi {t}."),
        ("Teknik & Metode", "Teknik dan metode pendekatan untuk memahami {t}."),
        ("Contoh Kerja", "Contoh penerapan {t} dengan langkah-langkah yang jelas."),
        ("Latihan & Praktik", "Soal latihan dan aktivitas praktis terkait {t}."),
        ("Ringkasan & Evaluasi", "Rangkuman poin-poin kunci dan kuis untuk menguji pemahaman {t}."),
    ],
}


def mock_roadmap(topic_title: str, goal: str = "") -> dict:
    subject = _detect_subject(topic_title)
    templates = _ROADMAP_PATTERNS.get(subject, _ROADMAP_PATTERNS["general"])
    steps = []
    for i, (title_tpl, desc_tpl) in enumerate(templates, start=1):
        title = title_tpl.replace("{t}", topic_title)
        desc = desc_tpl.replace("{t}", topic_title)
        steps.append({"order_number": i, "title": title, "description": desc})

    roadmap_title = f"Roadmap {topic_title}"
    if goal:
        roadmap_title += f" — {goal}"
    return {
        "title": roadmap_title,
        "difficulty": "Menengah",
        "estimated_hours": len(steps) * 2,
        "steps": steps,
    }


# ---------------------------------------------------------------------------
# Quiz generation
# ---------------------------------------------------------------------------

def mock_quiz(topic_title: str, count: int = 5) -> dict:
    questions = []
    subject = _detect_subject(topic_title)

    _TEMPLATES = {
        "physics": [
            ("Konsep dasar apa yang menjadi fondasi utama {t}?",
             ["Hukum dan prinsip fisika yang menjelaskan fenomena terkait {t}",
              "Hanya definisi istilah tanpa pemahaman konsep",
              "Menghafal rumus tanpa memahami makna variabelnya",
              "Melompat ke topik lanjutan tanpa fondasi"],
             0, "Memahami konsep dasar adalah kunci sebelum menerapkan rumus {t}."),
            ("Kapan rumus terkait {t} boleh diterapkan?",
             ["Ketika kondisi dan asumsi rumus terpenuhi",
              "Selalu, tanpa memperhatikan kondisi",
              "Hanya untuk soal teori",
              "Tidak perlu mengecek asumsi"],
             0, "Setiap rumus fisika punya kondisi penerapan yang harus dipenuhi."),
            ("Apa yang terjadi jika asumsi sebuah model {t} tidak terpenuhi?",
             ["Hasil perhitungan menjadi tidak akurat atau tidak valid",
              "Tidak ada pengaruh",
              "Rumus tetap benar",
              "Hanya relevan untuk percobaan"],
             0, "Pelanggaran asumsi model menghasilkan kesalahan sistematis."),
            ("Cara terbaik memverifikasi pemahaman tentang {t} adalah...",
             ["Mengerjakan soal berbagai tingkat kesulitan dengan pembahasan",
              "Menghafal rumus saja",
              "Membaca sekali lalu menganggap paham",
              "Menghindari soal sulit"],
             0, "Latihan aktif dengan pembahasan memperkuat pemahaman konseptual."),
            ("Kesalahan paling umum saat mengerjakan soal {t} adalah...",
             ["Tidak memperhatikan satuan dan konversi",
              "Terlalu teliti memeriksa jawaban",
              "Selalu membaca soal dengan seksama",
              "Menggunakan kalkulator"],
             0, "Satuan yang salah adalah sumber kesalahan paling umum dalam soal fisika."),
        ],
        "math": [
            ("Langkah pertama yang benar saat menyelesaikan masalah {t} adalah...",
             ["Identifikasi jenis masalah dan tentukan pendekatan yang tepat",
              "Langsung mengerjakan tanpa memahami soal",
              "Menghafal rumus tanpa tahu kapan dipakai",
              "Melompat ke penyelesaian"],
             0, "Mengenali jenis masalah menentukan keberhasilan penyelesaian {t}."),
            ("Mengapa penting memahami penurunan rumus dalam {t}?",
             ["Agar bisa memahami dan mengingat rumus lebih dalam",
              "Tidak penting, cukup menghafal",
              "Hanya untuk ujian teori",
              "Untuk membuat soal lebih sulit"],
             0, "Penurunan rumus memberikan pemahaman konseptual yang lebih kuat."),
            ("Kapan sebuah teknik {t} tidak dapat diterapkan?",
             ["Ketika kondisi domain atau syarat konvergensi tidak terpenuhi",
              "Selalu bisa diterapkan",
              "Hanya untuk soal ujian",
              "Tidak ada batasan"],
             0, "Setiap teknik matematika punya batasan domain penerapan."),
            ("Cara terbaik menguji pemahaman {t} adalah...",
             ["Mengerjakan berbagai variasi soal dan menganalisis kesalahan",
              "Menghafal pola soal",
              "Membaca kunci jawaban",
              "Hanya mengerjakan soal mudah"],
             0, "Variasi soal memperluas pemahaman dan kemampuan generalisasi."),
            ("Kesalahan paling sering terjadi dalam {t} adalah...",
             ["Kesalahan aljabar dan manipulasi persamaan",
              "Terlalu teliti dalam penjumlahan",
              "Membaca soal dengan benar",
              "Menggunakan notasi yang benar"],
             0, "Kesalahan aljabar adalah penyebab utama jawaban salah dalam matematika."),
        ],
        "default": [
            ("Apa langkah pertama yang tepat saat mempelajari {t}?",
             ["Memahami konsep dasar dan istilah penting terlebih dahulu",
              "Langsung mengerjakan soal sulit",
              "Menghafal semua materi tanpa konteks",
              "Melompat ke topik lanjutan"],
             0, "Memahami konsep dasar membangun fondasi yang kuat sebelum masuk ke bagian lebih dalam."),
            ("Bagaimana cara mengecek pemahaman kamu setelah belajar {t}?",
             ["Mengerjakan kuis dan meninjau kesalahan",
              "Tidak perlu mengecek",
              "Mengulang soal yang sama tanpa umpan balik",
              "Menghafal jawaban orang lain"],
             0, "Kuis dengan umpan balik membantu menemukan topik yang masih lemah untuk diulang."),
            ("Metode terbaik untuk menguatkan pemahaman {t} adalah...",
             ["Latihan soal secara bertahap dari mudah ke sulit",
              "Membaca sekali lalu menyerah",
              "Menunda sampai ujian",
              "Hanya menonton video"],
             0, "Latihan bertahap adalah cara paling efektif untuk memperkuat pemahaman konsep."),
            ("Apa yang harus dilakukan jika ada konsep {t} yang belum dipahami?",
             ["Tanya ke mentor AI dan minta penjelasan ulang",
              "Mengabaikannya",
              "Pindah topik tanpa memahami",
              "Berhenti belajar"],
             0, "Mentor AI siap membantu menjelaskan ulang konsep yang sulit dengan bahasa yang sesuai."),
            ("Cara terbaik mengingat materi {t} dalam jangka panjang adalah...",
             ["Mengulang secara berkala dan menerapkan dalam latihan",
              "Menghafal malam sebelum ujian",
              "Membaca sekali dengan cepat",
              "Menyalin catatan tanpa memahami"],
             0, "Pengulangan spaced dan penerapan praktis memperkuat retensi jangka panjang."),
        ],
    }

    tpl_key = subject if subject in _TEMPLATES else "default"
    templates = (_TEMPLATES[tpl_key] * ((count // len(_TEMPLATES[tpl_key])) + 1))[:count]

    for question_tpl, options_tpl, answer_idx, explanation_tpl in templates:
        options = [o.replace("{t}", topic_title) for o in options_tpl]
        questions.append({
            "question": question_tpl.replace("{t}", topic_title),
            "options": options,
            "answer_index": answer_idx,
            "explanation": explanation_tpl.replace("{t}", topic_title),
        })

    return {"title": f"Kuis {topic_title}", "questions": questions}


# ---------------------------------------------------------------------------
# Chat fallback
# ---------------------------------------------------------------------------

MOCK_GREETING = (
    "Halo! Aku Kak Buddio, mentor belajarmu. "
    "Aku dalam mode demo (tanpa kunci API AI), jadi jawaban ini adalah contoh. "
    "Jika kamu ingin jawaban yang lebih pintar dan personal, tambahkan GEMINI_API_KEY di file .env."
)


def mock_chat(message: str, topic_title: str) -> str:
    subj = _detect_subject(topic_title or message)
    subject_map = {
        "physics": (
            f"Topik kita hari ini tentang **{topic_title}** — bagian penting dalam fisika!\n\n"
            "### Konsep Utama\n"
            f"**{topic_title}** merupakan salah satu konsep kunci yang perlu dipahami untuk membangun "
            "fondasi kuat dalam fisika.\n\n"
            "**Intuisi:** Bayangkan sebuah benda bergerak di ruang angkasa — terdapat hukum fisika "
            "yang mengatur setiap gerakannya. Memahami {t} membantu kita menjelaskan fenomena ini "
            "dengan tepat.\n\n"
            "Mau aku jelaskan lebih detail bagian mana dari topik ini? 🤔"
        ),
        "math": (
            f"Topik kita hari ini tentang **{topic_title}** — fondasi penting dalam matematika!\n\n"
            "### Konsep Utama\n"
            f"**{topic_title}** membutuhkan pemahaman yang kuat tentang notasi, definisi, dan "
            "sifat-sifat matematika yang mendasarinya.\n\n"
            "**Intuisi:** Matematika adalah bahasa alam semesta. {t} membantu kita memahami "
            "pola dan hubungan yang mungkin tidak terlihat secara kasat mata.\n\n"
            "Mau aku bantu jelaskan dengan contoh soal? 🤔"
        ),
        "cs": (
            f"Topik kita hari ini tentang **{topic_title}** — skill penting dalam ilmu komputer!\n\n"
            "### Konsep Utama\n"
            f"**{topic_title}** adalah konsep yang perlu dipahami untuk menulis kode yang efisien "
            "dan terstruktur.\n\n"
            "**Intuisi:** Komputer hanya mengikuti instruksi yang kita berikan. Memahami {t} "
            "membantu kita menulis instruksi yang benar dan optimal.\n\n"
            "Mau aku tunjukkan contoh kodenya? 💻"
        ),
        "data": (
            f"Topik kita hari ini tentang **{topic_title}** — keterampilan kunci dalam data science!\n\n"
            "### Konsep Utama\n"
            f"**{topic_title}** merupakan tahap krusial dalam pipeline data yang menentukan "
            "kualitas model machine learning.\n\n"
            "**Intuisi:** Seperti memasak — bahan mentah yang bersih dan terolah dengan baik "
            "menghasilkan masakan (model) yang jauh lebih enak (akurat).\n\n"
            "Mau aku jelaskan langkah-langkahnya secara detail? 🔍"
        ),
        "programming": (
            f"Topik kita hari ini tentang **{topic_title}** — kemampuan penting dalam pemrograman!\n\n"
            "### Konsep Utama\n"
            f"**{topic_title}** adalah konsep yang perlu dikuasai untuk menulis kode yang rapi, "
            "efisien, dan mudah dipelihara.\n\n"
            "**Intuisi:** Pemrograman seperti membangun rumah — setiap balok harus diletakkan "
            "dengan benar agar strukturnya kokoh.\n\n"
            "Mau aku kasih contoh kodenya? 💻"
        ),
        "history": (
            f"Topik kita hari ini tentang **{topic_title}** — peristiwa penting dalam sejarah!\n\n"
            "### Latar Belakang\n"
            f"Untuk memahami **{topic_title}**, kita perlu mengetahui kondisi sosial, politik, "
            "dan budaya yang melatarbelakanginya.\n\n"
            "**Intuisi:** Sejarah adalah guru kehidupan. Memahami {t} membantu kita belajar "
            "dari pengalaman masa lalu.\n\n"
            "Mau aku jelaskan urutan peristiwanya? 📜"
        ),
    }

    template = subject_map.get(subj, (
        f"Topik kita hari ini tentang **{topic_title}**!\n\n"
        "### Konsep Utama\n"
        f"**{topic_title}** adalah topik yang menarik untuk dipelajari.\n\n"
        "Mau aku jelaskan lebih detail bagian mana dari topik ini? 🤔"
    ))

    return template.replace("{t}", topic_title)



# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Full-length, tutorial-style lesson builder (mock fallback)
#
# Even when the AI API is unavailable, we still produce a long, teaching-like
# materi (not a short summary). A shared skeleton guarantees warm tutor tone,
# objectives, narrative sections, several fully-worked examples, misconceptions,
# practise with full solutions, a summary and "next step" guidance. Subject
# payloads inject the specific formulas/code/facts so content stays relevant.
#
# NOTE: All payload strings are PLAIN strings (not f-strings). They use the
# literal placeholders {step} / {topic} which are substituted by _fill(), so
# LaTeX braces (e.g. \frac{1}{2}, \text{ kg}, X_{min}) never collide with
# Python's f-string brace interpolation.
# ---------------------------------------------------------------------------

def _fill(s: str, step: str, topic: str) -> str:
    return s.replace("{step}", step).replace("{topic}", topic)


def _nm(s: str) -> str:
    """Multiline plain text -> single-line value used inside callouts."""
    return s.strip()


def _full_lesson_common(step: str, topic: str, subject: dict) -> str:
    def F(s: str) -> str:
        return _fill(s, step, topic)

    hook = F(subject["hook"])
    approach = F(subject["approach"])
    how1 = F(subject["how1"])
    how2 = F(subject["how2"])
    why = F(subject["why"])
    applied = F(subject["applied"])
    transition = F(subject["transition"])

    examples = []
    for ex in subject["examples"]:
        rows = ["> **" + F(ex["label"]) + "**\n>"]
        for i, l in enumerate(ex["body"], start=1):
            rows.append("> **Langkah {}.** {}".format(i, F(l)))
        examples.append("\n".join(rows))

    miscon = []
    for m in subject["misconceptions"]:
        miscon.append(
            "❌ **Salah:** {}\n✅ **Benar:** {}\n🧠 **Mengapa:** {}".format(
                F(m["wrong"]), F(m["right"]), F(m["why"])
            )
        )

    practice_q = F(subject["practice"]["q"])
    practice_steps = [F(l) for l in subject["practice"]["steps"]]
    practice_ans = F(subject["practice"]["ans"])

    summary_rows = "\n".join("| **{}** | {} |".format(k, F(v)) for k, v in subject["summary"])

    content_words = (
        "Pada langkah ini, kita berjalan pelan-pelan dari nol menuju pemahaman "
        "yang utuh. Jangan terburu-buru — setiap bagian dibangun di atas bagian "
        "sebelumnya, persis seperti cara guru menjelaskan di depan kelas."
    )

    result = (
        "### {}\n\n".format(step)
        + hook
        + "\n\n"
        + content_words
        + "\n\n---\n\n"
        + "> [!tujuan]\n"
        + "> Saat selesai mempelajari langkah **{}** ini, kamu akan mampu:\n".format(step)
        + "> - [ ] **Menjelaskan** {}\n".format(approach)
        + "> - [ ] **Mengidentifikasi** kapan dan bagaimana {}\n".format(why)
        + "> - [ ] **Mengerjakan** hitungan/contoh {} secara tuntas langkah demi langkah\n".format(step)
        + "> - [ ] **Menghindari** kesalahan umum yang sering membuat jawaban salah\n"
        + "> - [ ] **Menerapkan** {}\n\n".format(applied)
        + "---\n\n"
        + "## 1. Mengapa {} Penting?\n\n".format(step)
        + why
        + "\n\nIntuisi singkatnya: "
        + hook
        + "\n\n---\n\n"
        + "## 2. Konsep Inti: {}\n\n".format(step)
        + how1
        + "\n\n"
        + how2
        + "\n\n> [!hubung]\n> **Koneksi dalam {}:**\n".format(topic)
        + "> - {} menjadi lebih mudah dipahami ketika kita menguasai {}.\n".format(topic, step)
        + "> - Konsep ini menjadi prasyarat sebelum melangkah ke bagian lanjutan.\n"
        + "> - {}\n\n".format(transition)
        + "---\n\n"
        + "## 3. Contoh Kerja Lengkap (Worked Example)\n\n"
        + "Berikut beberapa contoh yang kita kerjakan bersama dari awal sampai hasil akhir. "
        + "Baca perlahan, coba ulangi sendiri di kertas, lalu cocokkan.\n\n"
        + "> [!contoh]\n"
        + "\n\n---\n\n".join(examples)
        + "\n\n---\n\n"
        + "## 4. Kesalahan Umum & Miskonsepsi\n\n"
        + "Banyak siswa tersandung di titik yang sama. Yuk kita periksa agar kamu tidak "
        + "mengalami hal yang sama.\n\n"
        + "> [!perhatian]\n"
        + "\n\n".join(miscon)
        + "\n\n---\n\n"
        + "## 5. Coba Sendiri (Latihan)\n\n"
        + "Sekarang giliranmu. Kerjakan dulu barulah buka pembahasannya.\n\n"
        + "> [!coba]\n"
        + "> **Soal:** {}\n".format(practice_q)
        + "> **Petunjuk:**\n"
        + "".join("> {}. {}\n".format(i, s) for i, s in enumerate(practice_steps, start=1))
        + "> ---\n> **Pembahasan:**\n"
        + "> {}\n\n".format(practice_ans)
        + "---\n\n"
        + "## 6. Ringkasan {}\n\n".format(step)
        + "> [!ingat]\n"
        + "> Poin-poin penting yang harus diingat:\n"
        + "\n".join("> - **{}:** {}.".format(k, F(v)) for k, v in subject["summary"])
        + "\n\n---\n\n"
        + "## 7. Langkah Berikutnya\n\n"
        + "Selamat! Kamu baru saja menyelesaikan langkah **{}**. Konsep ini akan kamu ".format(step)
        + "pakai lagi pada langkah-langkah lanjutan dalam **{}**. Jika ada bagian yang ".format(topic)
        + "masih terasa sulit, jangan ragu bertanya ke Buddio agar dijelaskan ulang dengan "
        + "cara yang berbeda. Lanjutkan ke langkah berikutnya ketika kamu sudah yakin "
        + "langkah ini benar-benar dikuasai. 🎯\n"
    )

    # The payload templates above were written with doubled braces (`{{`/`}}`)
    # so they could never collide with Python's `.format()`/f-string machinery.
    # Once interpolation is done, collapse them back to single LaTeX braces so
    # e.g. `\frac{{1}}{{2}}` becomes the valid `\frac{1}{2}`.
    return result.replace("{{", "{").replace("}}", "}")


def _physics_full(step: str, topic: str) -> str:
    subject = {
        "hook": ("Pernahkah kamu bertanya mengapa {step} begitu penting dalam {topic}? "
                 "Coba bayangkan sebuah benda yang {step} — di baliknya tersembunyi "
                 "hukum fisika yang bisa kita hitung dan prediksi. Hari ini kita bongkar "
                 "bersama, dari nol."),
        "approach": "konsep inti {step} dan variabel fisika yang terlibat di dalamnya.",
        "how1": ("**{step}** dalam {topic} berhubungan erat dengan besaran fisika seperti gaya, "
                 "massa, percepatan, dan energi. Kunci utamanya: setiap perubahan keadaan "
                 "sistem dapat dijelaskan oleh persamaan yang menghubungkan besaran-besaran ini."),
        "how2": ("Untuk memahami {step} dengan benar, kita mulai dari definisi intuitif, lalu "
                 "melihat rumusnya, lalu mencobanya pada angka nyata. Rumus inti yang sering "
                 "dipakai: $F = m \\times a$ (untuk gaya) dan $E_k = \\frac{{1}}{{2}} m v^2$ "
                 "(untuk energi kinetik)."),
        "why": ("Menguasai {step} adalah syarat mutlak sebelum masuk ke materi fisika yang "
                "lebih kompleks; tanpa fondasi ini, soal-soal lanjutan akan terasa membingungkan."),
        "applied": "langkah ini pada soal fisika sehari-hari.",
        "transition": "begitu kita paham {step}, kita bisa memecah masalah rumit menjadi bagian kecil yang lebih mudah.",
        "examples": [
            {
                "label": "**Soal:** Sebuah benda bermassa $m = 10 \\text{{ kg}}$ diberi gaya $F = 50 \\text{{ N}}$. Hitung percepatannya!",
                "body": [
                    "Tuliskan yang diketahui: $m = 10 \\text{{ kg}}$, $F = 50 \\text{{ N}}$.",
                    "Pilih rumus: $F = m \\times a$, sehingga $a = \\frac{{F}}{{m}}$.",
                    "Substitusi angkanya: $a = \\frac{{50}}{{10}}$.",
                    "Hitung: $a = 5 \\text{{ m/s}}^2$.",
                    "Beri kesimpulan fisik: benda dipercepat sebesar $5 \\text{{ m/s}}^2$ searah gaya.",
                ],
            },
            {
                "label": "**Soal:** Energi kinetik mobil bermassa $m = 1000 \\text{{ kg}}$ yang melaju $v = 20 \\text{{ m/s}}$?",
                "body": [
                    "Diketahui: $m = 1000 \\text{{ kg}}$, $v = 20 \\text{{ m/s}}$.",
                    "Rumus: $E_k = \\frac{{1}}{{2}} m v^2$.",
                    "Substitusi: $E_k = \\frac{{1}}{{2}} \\times 1000 \\times 20^2$.",
                    "Hitung: $E_k = 500 \\times 400 = 200000 \\text{{ J}}$.",
                    "Kesimpulan: energi kinetiknya $200 \\text{{ kJ}}$ (200.000 J).",
                ],
            },
        ],
        "misconceptions": [
            {"wrong": "Semakin besar gaya, kecepatan selalu bertambah sebanding.",
             "right": "Gaya menyebabkan percepatan, bukan langsung kecepatan.",
             "why": "Rumus $F = ma$ menghubungkan gaya dengan percepatan; kecepatan terus bertambah hanya selama gaya bekerja."},
            {"wrong": "Satuan tidak perlu dikonversi dulu.",
             "right": "Semua besaran harus dalam satuan SI sebelum substitusi.",
             "why": "Jika $m$ dalam gram dan $v$ dalam km/jam, hasilnya salah besar."},
        ],
        "practice": {
            "q": "Benda bermassa $m = 5 \\text{{ kg}}$ bergerak dengan kecepatan $v = 4 \\text{{ m/s}}$. Hitung energi kinetiknya!",
            "steps": ["Tulis yang diketahui.", "Pilih rumus.", "Substitusi.", "Hitung.", "Tulis satuan."],
            "ans": "$E_k = \\frac{{1}}{{2}} \\times 5 \\times 4^2 = \\frac{{1}}{{2}} \\times 5 \\times 16 = 40 \\text{{ J}}$. Jadi energi kinetik = 40 J.",
        },
        "summary": [
            ("Inti", "{step} menjelaskan hubungan antar besaran fisika dalam {topic}"),
            ("Rumus", "$F = ma$ dan $E_k = \\frac{{1}}{{2}} m v^2$ sering menjadi kunci"),
            ("Satuan", "selalu konversi ke SI sebelum menghitung"),
            ("Pola", "urangi masalah besar menjadi langkah kecil"),
            ("Berlatih", "ulangi hitungan sendiri untuk menguatkan pemahaman"),
        ],
    }
    return _full_lesson_common(step, topic, subject)


def _math_full(step: str, topic: str) -> str:
    subject = {
        "hook": ("Dari sekian banyak topik matematika, **{step}** adalah salah satu yang paling "
                 "sering muncul. Kabar baiknya: dengan pola yang benar, kamu bisa menyelesaikan "
                 "soalnya secara konsisten. Mari kita pelajari polanya satu per satu."),
        "approach": "definisi, notasi, dan kapan sebuah teknik {step} boleh dipakai.",
        "how1": ("**{step}** pada {topic} dibangun dari definisi yang jelas dan sifat-sifat "
                 "operasi. Kita perlu memahami *kenapa* sebuah aturan berlaku, bukan sekadar "
                 "menghafal rumusnya."),
        "how2": "Contoh bentuk yang sering kita temui: $f(x) = x^2 - 4x + 3$ atau $y = mx + c$. "
                "Langkah menyelesaikannya selalu: pahami soal → terapkan aturan → periksa kembali.",
        "why": "**{step}** menjadi alat bantu untuk menyelesaikan banyak permasalahan "
               "matematis dan terapan, sehingga wajib dikuasai sebelum lanjut ke materi berikutnya.",
        "applied": "teknik penyelesaian pada berbagai tipe soal {topic}.",
        "transition": "pola pikir sistematis ini bisa kamu bawa ke semua soal lain, tidak hanya {step}.",
        "examples": [
            {
                "label": "**Soal:** Diketahui $f(x) = 2x^2 + 3x - 5$. Hitung $f(2)$!",
                "body": [
                    "Tulis fungsi: $f(x) = 2x^2 + 3x - 5$.",
                    "Ganti $x$ dengan 2: $f(2) = 2(2)^2 + 3(2) - 5$.",
                    "Hitung pangkat: $2 \\times 4 + 6 - 5$.",
                    "Operasikan: $8 + 6 - 5 = 9$.",
                    "Jadi $f(2) = 9$.",
                ],
            },
            {
                "label": "**Soal:** Selesaikan persamaan $3x - 7 = 11$!",
                "body": [
                    "Persamaan: $3x - 7 = 11$.",
                    "Pindah konstanta: $3x = 11 + 7 = 18$.",
                    "Bagikan koefisien: $x = \\frac{{18}}{{3}}$.",
                    "Sederhanakan: $x = 6$.",
                    "Verifikasi: $3(6) - 7 = 18 - 7 = 11$ ✓ benar.",
                ],
            },
        ],
        "misconceptions": [
            {"wrong": "Menghafal rumus lebih penting daripada memahami konsep.",
             "right": "Memahami konsep membuat rumus mudah diingat dan diterapkan.",
             "why": "Jika paham penalarannya, kamu tidak akan lupa kapan rumus dipakai."},
            {"wrong": "Saat memindah ruas, tanda tidak dibalik.",
             "right": "Setiap pindah ruas disertai pembalikan operasi (tambah↔kurang, kali↔bagi).",
             "why": "Itu menjaga kesetaraan kedua ruas persamaan."},
        ],
        "practice": {
            "q": "Diketahui fungsi $g(x) = x^2 + 5x + 6$. Carilah nilai $g(-1)$!",
            "steps": ["Tulis fungsi.", "Substitusi nilai $x$.", "Hitung pangkat dan perkalian.", "Jumlahkan.", "Tulis hasil akhir."],
            "ans": "$g(-1) = (-1)^2 + 5(-1) + 6 = 1 - 5 + 6 = 2$. Jadi $g(-1) = 2$.",
        },
        "summary": [
            ("Definisi", "pahami notasi dan makna setiap variabel"),
            ("Langkah", "selalu baca soal → terapkan aturan → periksa ulang"),
            ("Verifikasi", "masukkan kembali hasil ke soal untuk cek kebenaran"),
            ("Latihan", "kerjakan variasi soal agar pola tertanam kuat"),
            ("Fondasi", "{step} adalah alat wajib untuk materi lanjutan"),
        ],
    }
    return _full_lesson_common(step, topic, subject)


def _data_full(step: str, topic: str) -> str:
    subject = {
        "hook": ("Dalam **{topic}**, kualitas hasil sangat ditentukan oleh kualitas data "
                 "awalnya. **{step}** adalah tahap yang memastikan data kita benar-benar siap "
                 "diolah model. Tanpa tahap ini, model rapi pun bisa menghasilkan prediksi "
                 "yang menyesatkan."),
        "approach": "tujuan {step} dan teknik yang dipakai agar data layak diolah model.",
        "how1": ("**{step}** mencakup membersihkan data (nilai hilang, duplikat, outlier), "
                 "transformasi nilai, dan encoding data kategori agar bisa dibaca algoritma."),
        "how2": ("Salah satu teknik kunci adalah Min-Max Scaling, dengan rumus:\n\n"
                 "$$X_{scaled} = \\frac{{X - X_{{min}}}}{{X_{{max}} - X_{{min}}}}$$"),
        "why": "Menguasai {step} mencegah masalah seperti data leakage dan performa model yang buruk.",
        "applied": "teknik scaling dan cleaning pada kumpulan data nyata.",
        "transition": "data yang bersih membuat seluruh pipeline machine learning lebih andal.",
        "examples": [
            {
                "label": "**Soal:** Dataset $X = [20, 30, 50]$. Terapkan Min-Max Scaling pada $X = 30$!",
                "body": [
                    "Tentukan nilai min dan max: $X_{min} = 20$, $X_{max} = 50$.",
                    "Hitung rentang: $X_{max} - X_{min} = 50 - 20 = 30$.",
                    "Substitusi ke rumus untuk $X = 30$: $\\frac{{30 - 20}}{{30}}$.",
                    "Hitung: $\\frac{{10}}{{30}} \\approx 0.33$.",
                    "Jadi nilai scaled untuk 30 adalah sekitar 0,33.",
                ],
            },
            {
                "label": "**Soal:** Dataset $X = [10, 20, 30, 40]$. Berapa nilai scaled untuk $X = 25$?",
                "body": [
                    "$X_{min} = 10$, $X_{max} = 40$, rentang = $40 - 10 = 30$.",
                    "Substitusi: $\\frac{{25 - 10}}{{30}}$.",
                    "Hitung: $\\frac{{15}}{{30}} = 0.5$.",
                    "Jadi nilai scaled = 0,5.",
                    "Interpretasi: 25 berada di tengah-tengah rentang data.",
                ],
            },
        ],
        "misconceptions": [
            {"wrong": "Fitur scaler pada seluruh dataset sekaligus sebelum split train/test.",
             "right": "Fit hanya pada data training, lalu transform pada train dan test.",
             "why": "Kalau scaler melihat data test, terjadi data leakage dan hasil evaluasi menyesatkan."},
            {"wrong": "Data kategori tidak perlu di-encode.",
             "right": "Data kategori harus diubah (one-hot/label) agar algoritma bisa membacanya.",
             "why": "Sebagian besar model hanya bekerja dengan bilangan."},
        ],
        "practice": {
            "q": "Dataset $Y = [5, 15, 25]$. Hitung nilai Min-Max Scaling untuk $Y = 15$!",
            "steps": ["Cari nilai min dan max.", "Hitung rentang.", "Substitusi ke rumus.", "Sederhanakan."],
            "ans": "$Y_{min} = 5$, $Y_{max} = 25$, rentang = 20. $\\frac{{15 - 5}}{{20}} = \\frac{{10}}{{20}} = 0.5$.",
        },
        "summary": [
            ("Peran", "{step} menentukan kualitas input model"),
            ("Min-Max", "$X_{scaled} = (X - X_{min})/(X_{max} - X_{min})$"),
            ("Leakage", "jangan pernah fit scaler pada data test"),
            ("Bersih dulu", "tangani nilai hilang sebelum scaling"),
            ("Kategori", "encode data kategori agar bisa diolah model"),
        ],
    }
    return _full_lesson_common(step, topic, subject)


def _programming_full(step: str, topic: str) -> str:
    subject = {
        "hook": ("Menulis kode yang benar itu seperti menyusun instruksi yang jelas. "
                 "**{step}** pada {topic} mengajarkan kita cara menyusun logika yang rapi, "
                 "mudah dibaca, dan mudah dipelihara."),
        "approach": "konsep {step} dan kapan waktu yang tepat menggunakannya.",
        "how1": "**{step}** membantu kita memecah masalah menjadi langkah kecil, menggunakan fungsi, perulangan, dan struktur data dengan tepat.",
        "how2": ("Contohnya, kita bisa menulis fungsi yang memproses sekumpulan data. "
                 "Perhatikan kode berikut (Python):\n\n"
                 "```python\n"
                 "def proses(data):\n"
                 "    hasil = []\n"
                 "    for item in data:\n"
                 "        hasil.append(item * 2)\n"
                 "    return hasil\n"
                 "\n"
                 "print(proses([1, 2, 3]))  # [2, 4, 6]\n"
                 "```"),
        "why": "Menguasai {step} membuat kode lebih bersih dan bug lebih mudah ditemukan.",
        "applied": "pola penulisan kode yang terstruktur pada proyek {topic}.",
        "transition": "struktur kode yang baik menjadi fondasi untuk fitur yang lebih besar.",
        "examples": [
            {
                "label": "**Soal:** Modifikasi fungsi agar hanya memproses bilangan genap!",
                "body": [
                    "Mulai dari fungsi `proses(data)` yang ada.",
                    "Tambahkan kondisi `if item % 2 == 0` di dalam perulangan.",
                    "Sertakan hanya item genap ke `hasil`.",
                    "Uji dengan `[1, 2, 3, 4]` → hasil `[2, 4]`.",
                    "Simpulkan: kode sekarang lebih spesifik dan tetap rapi.",
                ],
            },
            {
                "label": "**Soal:** Tulis list comprehension untuk mengkuadratkan tiap elemen!",
                "body": [
                    "Bentuk umum: `[ekspresi for item in data]`.",
                    "Tulis `[x**2 for x in data]`.",
                    "Uji dengan `[1, 2, 3]` → hasil `[1, 4, 9]`.",
                    "Bandingkan dengan versi perulangan biasa.",
                    "Simpulkan keuntungan: lebih ringkas dan mudah dibaca.",
                ],
            },
        ],
        "misconceptions": [
            {"wrong": "Semakin pendek kode selalu semakin baik.",
             "right": "Kode yang jelas dan mudah dibaca lebih baik daripada sekadar pendek.",
             "why": "Kode yang membingungkan sulit dipelihara dan rawan bug."},
            {"wrong": "Nama variabel singkat seperti `x` selalu boleh.",
             "right": "Gunakan nama deskriptif seperti `total_harga`.",
             "why": "Nama yang jelas membuat maksud kode langsung terbaca."},
        ],
        "practice": {
            "q": "Buat fungsi `kali_tiga(data)` yang mengalikan setiap elemen dengan 3, lalu panggil dengan `[1, 2, 3]`!",
            "steps": ["Tulis definisi fungsi.", "Buat perulangan atau list comprehension.", "Kembalikan hasil.", "Cetak hasil pemanggilan."],
            "ans": "`def kali_tiga(data): return [x * 3 for x in data]` → `print(kali_tiga([1,2,3]))` menghasilkan `[3, 6, 9]`.",
        },
        "summary": [
            ("Fungsi", "pecah masalah menjadi fungsi kecil yang jelas"),
            ("Struktur", "perulangan dan list comprehension untuk memproses data"),
            ("Bersih", "nama variabel deskriptif dan docstring"),
            ("Uji", "selalu uji dengan beberapa kasus"),
            ("Perawatan", "kode rapi mudah dipelihara dalam jangka panjang"),
        ],
    }
    return _full_lesson_common(step, topic, subject)


def _cs_full(step: str, topic: str) -> str:
    subject = {
        "hook": ("Komputer menyelesaikan masalah dengan mengikuti langkah yang jelas dan "
                 "terurut — tepat seperti **{step}** dalam {topic}. Memahami ini adalah "
                 "kunci untuk berpikir seperti seorang ilmuwan komputer."),
        "approach": "prinsip kerja {step} serta hubungannya dengan kompleksitas waktu dan ruang.",
        "how1": ("**{step}** menggambarkan bagaimana sebuah proses dijalankan langkah demi "
                 "langkah. Kita menuliskannya sebagai pseudocode atau diagram alur sebelum "
                 "mengubahnya menjadi kode nyata."),
        "how2": ("Contoh pseudocode sederhana:\n\n"
                 "```\n"
                 "ALGORITMA Proses(data):\n"
                 "    hasil = kosong\n"
                 "    UNTUK setiap elemen DALAM data:\n"
                 "        tambahkan elemen ke hasil\n"
                 "    KEMBALIKAN hasil\n"
                 "```"),
        "why": "Memahami {step} membantu kita memilih pendekatan yang efisien untuk masalah besar.",
        "applied": "perancangan algoritma pada masalah {topic}.",
        "transition": "cara berpikir algoritmik ini dipakai di hampir semua cabang ilmu komputer.",
        "examples": [
            {
                "label": "**Soal:** Hitung kompleksitas waktu dari proses di atas untuk input $n$!",
                "body": [
                    "Perhatikan ada satu perulangan yang melewati seluruh elemen.",
                    "Setiap elemen diproses satu kali.",
                    "Jadi banyak langkah sebanding dengan $n$.",
                    "Kompleksitasnya adalah $O(n)$ linear.",
                    "Simpulan: waktu bertambah lurus mengikuti ukuran input.",
                ],
            },
            {
                "label": "**Soal:** Bagaimana jika ada dua perulangan bersarang?",
                "body": [
                    "Perulangan luar berjalan $n$ kali.",
                    "Di dalamnya, perulangan dalam juga berjalan hingga $n$ kali.",
                    "Total operasi ≈ $n \\times n = n^2$.",
                    "Kompleksitasnya $O(n^2)$ kuadratik.",
                    "Simpulan: untuk $n$ besar, waktu tumbuh cepat — hindari bila bisa.",
                ],
            },
        ],
        "misconceptions": [
            {"wrong": "Algoritma yang benar pasti selalu efisien.",
             "right": "Benar dan efisien adalah dua hal berbeda.",
             "why": "Algoritma bisa benar tetapi lambat untuk data besar; efisiensi perlu dianalisis."},
            {"wrong": "Kasus tepi (edge case) tidak penting.",
             "right": "Menguji kasus tepi sangat penting untuk mencegah bug.",
             "why": "Banyak bug muncul justru pada input kosong, satu elemen, atau nilai ekstrem."},
        ],
        "practice": {
            "q": "Tulis pseudocode untuk mencari nilai terbesar dalam list $[3, 7, 2, 9]$, lalu sebutkan kompleksitasnya!",
            "steps": ["Inisialisasi variabel `maks` dengan elemen pertama.", "Bandingkan satu per satu.", "Perbarui `maks` bila lebih besar.", "Kembalikan `maks`.", "Sebutkan kompleksitas."],
            "ans": "`maks = 3`, bandingkan berturut-turut hingga ketemu 9, kompleksitas $O(n)$.",
        },
        "summary": [
            ("Algoritma", "langkah jelas dan berurutan untuk memecahkan masalah"),
            ("Pseudocode", "tulis logika dulu sebelum kode nyata"),
            ("Kompleksitas", "$O(n)$ linear, $O(n^2)$ kuadratik, dst."),
            ("Kasus tepi", "selalu uji input kosong dan ekstrem"),
            ("Efisiensi", "pilih algoritma sesuai ukuran dan jenis data"),
        ],
    }
    return _full_lesson_common(step, topic, subject)


def _history_full(step: str, topic: str) -> str:
    subject = {
        "hook": ("Setiap peristiwa besar tidak terjadi begitu saja. **{step}** dalam {topic} "
                 "memiliki latar belakang, tokoh, dan dampak yang saling berkaitan. Memahami "
                 "rangkaian ini membuat kita bisa membaca sejarah dengan lebih dalam."),
        "approach": "latar belakang, kronologi, tokoh, dan dampak dari {step}.",
        "how1": ("**{step}** terjadi karena kombinasi faktor politik, ekonomi, sosial, dan budaya. "
                 "Untuk memahaminya, kita memetakan kondisi sebelum, selama, dan sesudahnya."),
        "how2": ("Cara paling efektif: susun **kronologi** lengkap dari pemicu hingga akibatnya, "
                 "lalu identifikasi peran setiap tokoh penting."),
        "why": "Menguasai {step} membantu kita menarik pelajaran dari pengalaman masa lalu.",
        "applied": "cara menganalisis peristiwa sejarah secara kronologis dan kritis.",
        "transition": "pola sebab-akibat ini berlaku untuk hampir semua peristiwa sejarah lainnya.",
        "examples": [
            {
                "label": "**Analisis:** Bagaimana cara mengurai {step} menjadi rangkaian sebab-akibat?",
                "body": [
                    "Petakan kondisi awal: faktor-faktor yang ada sebelum peristiwa.",
                    "Identifikasi pemicu langsung yang membuat keadaan berubah.",
                    "Susun urutan kejadian utama secara kronologis.",
                    "Cari tokoh kunci dan peran masing-masing.",
                    "Tulis dampak jangka pendek dan jangka panjang.",
                ],
            },
            {
                "label": "**Analisis:** Mengapa satu peristiwa bisa punya banyak tafsir?",
                "body": [
                    "Setiap sumber ditulis dari sudut pandang tertentu.",
                    "Konteks sosial-politik memengaruhi cara penulisan.",
                    "Latar belakang sejarawan ikut mewarnai interpretasi.",
                    "Bandingkan beberapa sumber untuk melihat gambaran utuh.",
                    "Simpulan: sejarah dibaca secara kritis, tidak tunggal.",
                ],
            },
        ],
        "misconceptions": [
            {"wrong": "Sejarah hanya kumpulan tanggal dan nama.",
             "right": "Sejarah adalah analisis sebab-akibat dan perubahan sosial.",
             "why": "Menghafal tanggal saja tidak menjelaskan mengapa dan bagaimana."},
            {"wrong": "Satu sumber sejarah sudah cukup.",
             "right": "Idealnya membandingkan berbagai sumber yang berbeda.",
             "why": "Satu sumber bisa bias; konfirmasi silang membuat kesimpulan lebih kuat."},
        ],
        "practice": {
            "q": "Buat ringkasan tiga poin: (1) latar belakang, (2) satu peristiwa inti, (3) satu dampak dari {step}!",
            "steps": ["Tulis latar belakang singkat.", "Pilih satu peristiwa inti paling penting.", "Tulis satu dampak nyata.", "Hubungkan ketiganya dalam satu kalimat."],
            "ans": "Contoh: latar belakang = kondisi ketidakpuasan; peristiwa inti = momen kunci; dampak = perubahan struktur sosial-politik.",
        },
        "summary": [
            ("Latar", "setiap peristiwa punya akar kondisi sosial-politik"),
            ("Kronologi", "susun urutan untuk melihat benang merah"),
            ("Tokoh", "peran tokoh memengaruhi jalannya peristiwa"),
            ("Dampak", "bedakan pengaruh jangka pendek dan panjang"),
            ("Kritis", "bandingkan sumber agar kesimpulan lebih kuat"),
        ],
    }
    return _full_lesson_common(step, topic, subject)


def _general_full(step: str, topic: str) -> str:
    subject = {
        "hook": ("**{step}** adalah potongan penting dari topik **{topic}**. Bahkan jika topik "
                 "ini terasa luas, menguasai langkah ini selangkah demi selangkah akan membuat "
                 "gambaran besarnya jauh lebih jelas."),
        "approach": "konsep inti {step} dan penerapannya dalam {topic}.",
        "how1": ("**{step}** pada {topic} membangun pemahaman yang akan kamu pakai terus. "
                 "Kita mulai dari ide sederhana, lalu menambah lapisan detailnya pelan-pelan."),
        "how2": ("Intinya: pahami *apa*, *mengapa*, dan *bagaimana*. Setelah itu coba terapkan "
                 "pada satu contoh nyata agar konsep tidak hanya tertinggal di teori."),
        "why": "{step} menjadi dasar untuk memahami bagian lain dari {topic}.",
        "applied": "konsep {step} pada situasi nyata sehari-hari.",
        "transition": "setiap konsep baru pada {topic} akan lebih mudah karena fondasimu sudah kuat.",
        "examples": [
            {
                "label": "**Langkah berpikir:** Cara menerapkan {step} pada satu kasus nyata",
                "body": [
                    "Identifikasi masalah dan data yang kamu punya.",
                    "Tentukan pendekatan yang paling sesuai.",
                    "Terapkan konsep {step} langkah demi langkah.",
                    "Periksa hasilnya secara kritis.",
                    "Hubungkan kembali dengan teori dan simpulkan.",
                ],
            },
            {
                "label": "**Langkah berpikir:** Bagaimana memverifikasi bahwa pemahamanmu benar?",
                "body": [
                    "Jelaskan konsep dengan bahasamu sendiri.",
                    "Beri satu contoh penerapan nyata.",
                    "Timbulkan satu pertanyaan dan jawab sendiri.",
                    "Minta penjelasan ulang bila ada bagian yang belum jelas.",
                    "Kerjakan latihan untuk menguji ingatanmu.",
                ],
            },
        ],
        "misconceptions": [
            {"wrong": "Menghafal istilah sama dengan memahami.",
             "right": "Memahami berarti bisa menjelaskan dan menerapkan.",
             "why": "Hafalan tanpa pemahaman mudah lupa dan sulit diterapkan pada kasus baru."},
            {"wrong": "Membaca sekali cukup untuk menguasai.",
             "right": "Membaca + mencoba + mengulang adalah cara terkuat.",
             "why": "Pengulangan aktif memperkuat ingatan jangka panjang."},
        ],
        "practice": {
            "q": "Jelaskan dengan bahasamu sendiri apa itu {step}, lalu beri satu contoh penerapannya dalam {topic}!",
            "steps": ["Tulis definisi dengan kata sendiri.", "Beri satu contoh nyata.", "Sebutkan satu kesalahan umum."],
            "ans": "Rumuskan definisi sederhana tentang {step}, beri contoh nyata relevan, dan ingat definisi + contoh + latihan membuat pemahaman kokoh.",
        },
        "summary": [
            ("Fondasi", "{step} adalah dasar penting untuk memahami {topic}"),
            ("Paham vs hafal", "pemahaman lebih kuat daripada sekadar hafalan"),
            ("Praktik", "contoh nyata membuat konsep lebih mudah diingat"),
            ("Tanya", "bertanya ke mentor mempercepat pemahaman"),
            ("Ulang", "pengulangan aktif menguatkan ingatan"),
        ],
    }
    return _full_lesson_common(step, topic, subject)


def mock_lesson(step_title: str, topic_title: str) -> dict:
    subject = _detect_subject(f"{step_title} {topic_title}")
    generators = {
        "physics": _physics_full,
        "math": _math_full,
        "data": _data_full,
        "programming": _programming_full,
        "cs": _cs_full,
        "history": _history_full,
        "chemistry": _general_full,
        "biology": _general_full,
        "economics": _general_full,
        "language": _general_full,
    }
    gen = generators.get(subject, _general_full)
    return {"content": gen(step_title, topic_title), "videos": []}

