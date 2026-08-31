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
# Lesson generation
# ---------------------------------------------------------------------------

def _physics_lesson(step: str, topic: str) -> dict:
    return {
        "content": (
            f"### Alur Konseptual: {step}\n\n"
            f"Dalam topik **{topic}**, langkah **{step}** merupakan fondasi yang harus dikuasai "
            "sebelum melangkah ke konsep yang lebih kompleks.\n\n"
            "---\n\n"
            "> [!tujuan]\n"
            f"> **Tujuan Pembelajaran — {step}:**\n"
            f"> - [ ] **Menjelaskan** konsep inti {step} dan mengapa ini penting dalam {topic}.\n"
            f"> - [ ] **Mengidentifikasi** variabel, rumus, dan satuan yang terlibat dalam {step}.\n"
            f"> - [ ] **Menghitung** contoh soal terkait {step} secara mandiri langkah demi langkah.\n"
            f"> - [ ] **Menganalisis** kesalahan umum dan batasan penerapan {step}.\n\n"
            "---\n\n"
            f"## Konsep {step}\n\n"
            f"**{step}** dalam konteks {topic} menjelaskan bagaimana fenomena fisika ini bekerja "
            "secara kuantitatif. Mari kita pahami dari sisi intuisi lalu masuk ke formalisme matematika.\n\n"
            f"**Intuisi:** Bayangkan sebuah benda bergerak — untuk memahami {step}, kita perlu "
            f"melihat bagaimana besaran fisika berubah seiring waktu atau kondisi.\n\n"
            "**Formula Inti:**\n"
            f"Kita akan menggunakan rumus utama terkait {step} untuk menghitung besaran fisika yang dicari.\n\n"
            f"$$F = ma$$\n\n"
            "Dimana:\n"
            "- $F$ = Gaya (Newton)\n"
            "- $m$ = Massa benda (kg)\n"
            "- $a$ = Percepatan (m/s²)\n\n"
            "---\n\n"
            "> [!contoh]\n"
            f"> **Worked Example: Perhitungan {step} Tuntas**\n"
            ">\n"
            "> **Diketahui:**\n"
            "> - Massa benda: $m = 10 \\text{ kg}$\n"
            "> - Percepatan: $a = 5 \\text{ m/s}^2$\n"
            ">\n"
            "> **Hitungan Langkah demi Langkah:**\n"
            "> 1. **Identifikasi rumus:** $F = m \\times a$\n"
            "> 2. **Substitusi nilai:** $F = 10 \\times 5 = 50 \\text{ N}$\n"
            "> 3. **Interpretasi:** Benda dengan massa 10 kg yang dipercepat 5 m/s² membutuhkan gaya 50 Newton.\n"
            ">\n"
            "> **Hasil Akhir:** $F = 50 \\text{ N}$\n\n"
            "---\n\n"
            f"> [!coba]\n"
            f"> **Soal Latihan — {step}:**\n"
            "> Sebuah benda bermassa $m = 20 \\text{ kg}$ ditarik dengan gaya $F = 100 \\text{ N}$.\n"
            "> Hitunglah percepatan benda tersebut!\n"
            ">\n"
            "> ---\n"
            "> **Pembahasan:**\n"
            "> 1. Rumus: $F = ma \\rightarrow a = \\frac{F}{m}$\n"
            "> 2. Substitusi: $a = \\frac{100}{20} = 5 \\text{ m/s}^2$\n"
            "> 3. **Jawaban:** Percepatan benda adalah $5 \\text{ m/s}^2$\n\n"
            "---\n\n"
            "> [!ingat]\n"
            f"> **Ringkasan — {step}:**\n"
            f"> - {step} menjelaskan hubungan antara besaran fisika dalam {topic}.\n"
            "> - Selalu cek satuan sebelum menghitung agar tidak terjadi kesalahan konversi.\n"
            "> - Rumus $F = ma$ berlaku untuk sistem tertutup tanpa gesekan.\n"
            "> - Kesalahan paling umum: tidak mengonversi satuan ke SI sebelum substitusi.\n\n"
            "---\n\n"
            "> [!quiz]\n"
            f"> **Soal 1:** Apa yang terjadi jika massa benda diperbesar 2 kali dengan gaya yang sama?\n"
            "> **Soal 2:** Kapan rumus $F = ma$ tidak berlaku?\n"
            ">\n"
            "> ---\n"
            "> **Jawaban:**\n"
            "> 1. Percepatan menjadi setengahnya (invers proporsional terhadap massa).\n"
            "> 2. Untuk benda yang bergerak mendekati kecepatan cahaya atau dalam medan gravitasi kuat."
        ),
        "videos": [],
    }


def _math_lesson(step: str, topic: str) -> dict:
    return {
        "content": (
            f"### Alur Konseptual: {step}\n\n"
            f"Dalam topik **{topic}**, langkah **{step}** merupakan teknik yang harus dikuasai "
            "sebelum masuk ke topik yang lebih lanjut.\n\n"
            "---\n\n"
            "> [!tujuan]\n"
            f"> **Tujuan Pembelajaran — {step}:**\n"
            f"> - [ ] **Menjelaskan** definisi dan notasi {step} dalam konteks {topic}.\n"
            f"> - [ ] **Mengidentifikasi** kapan teknik {step} boleh dan tidak boleh diterapkan.\n"
            f"> - [ ] **Menghitung** contoh soal {step} secara tuntas dari awal hingga hasil akhir.\n"
            f"> - [ ] **Menganalisis** kesalahan umum saat menerapkan {step}.\n\n"
            "---\n\n"
            f"## Konsep {step}\n\n"
            f"**{step}** dalam {topic} membutuhkan pemahaman yang kuat tentang definisi, notasi, "
            "dan sifat-sifat matematika yang mendasarinya.\n\n"
            f"**Intuisi:** Bayangkan sebuah pola — {topic} membantu kita menemukan aturan tersembunyi "
            "yang mengatur pola tersebut.\n\n"
            "**Formula Utama:**\n\n"
            "$$f(x) = x^2 + 2x + 1$$\n\n"
            "Dimana:\n"
            "- $f(x)$ = fungsi yang akan dianalisis\n"
            "- $x$ = variabel input\n\n"
            "---\n\n"
            "> [!contoh]\n"
            f"> **Worked Example: Perhitungan {step} Tuntas**\n"
            ">\n"
            "> **Diketahui:** $f(x) = x^2 + 2x + 1$, hitung nilai $f(3)$\n"
            ">\n"
            "> **Langkah demi Langkah:**\n"
            "> 1. **Substitusi:** $f(3) = 3^2 + 2(3) + 1$\n"
            "> 2. **Hitung:** $f(3) = 9 + 6 + 1 = 16$\n"
            "> 3. **Hasil:** $f(3) = 16$\n\n"
            "---\n\n"
            "> [!coba]\n"
            f"> **Soal Latihan — {step}:**\n"
            "> Hitung nilai $f(x) = x^2 - 4x + 3$ untuk $x = 5$.\n"
            ">\n"
            "> ---\n"
            "> **Pembahasan:**\n"
            "> 1. Substitusi: $f(5) = 5^2 - 4(5) + 3$\n"
            "> 2. Hitung: $f(5) = 25 - 20 + 3 = 8$\n"
            "> 3. **Jawaban:** $f(5) = 8$\n\n"
            "---\n\n"
            "> [!ingat]\n"
            f"> **Ringkasan — {step}:**\n"
            f"> - {step} adalah teknik dasar dalam {topic} yang sering muncul di berbagai tipe soal.\n"
            "> - Selalu perhatikan domain dan asumsi sebelum menerapkan teknik.\n"
            "> - Kesalahan paling umum: kesalahan aljabar saat substitusi.\n\n"
            "---\n\n"
            "> [!quiz]\n"
            f"> **Soal 1:** Kapan teknik {step} tidak boleh diterapkan?\n"
            f"> **Soal 2:** Apa langkah verifikasi untuk memastikan hasil {step} benar?\n"
            ">\n"
            "> ---\n"
            "> **Jawaban:**\n"
            "> 1. Ketika syarat konvergensi atau domain tidak terpenuhi.\n"
            "> 2. Substitusi ulang hasil ke persamaan semula dan cek konsistensi."
        ),
        "videos": [],
    }


def _data_lesson(step: str, topic: str) -> dict:
    return {
        "content": (
            f"### Alur Konseptual: {step}\n\n"
            f"Dalam topik **{topic}**, langkah **{step}** merupakan tahap krusial yang menentukan "
            "kualitas model machine learning.\n\n"
            "---\n\n"
            "> [!tujuan]\n"
            f"> **Tujuan Pembelajaran — {step}:**\n"
            f"> - [ ] **Menjelaskan** tujuan dan mekanisme {step} dalam pipeline {topic}.\n"
            f"> - [ ] **Mengidentifikasi** jenis data yang membutuhkan {step}.\n"
            f"> - [ ] **Menghitung** hasil {step} pada dataset contoh secara tuntas.\n"
            f"> - [ ] **Menganalisis** dampak {step} terhadap performa model.\n"
            f"> - [ ] **Mencegah** data leakage saat menerapkan {step}.\n\n"
            "---\n\n"
            f"## Konsep {step}\n\n"
            f"**{step}** dalam konteks {topic} menjelaskan bagaimana data mentah diolah menjadi "
            "siap pakai untuk pemodelan.\n\n"
            "**Intuisi:** Bayangkan kamu membeli buah segar dari pasar. Sebelum dimasak, kamu harus "
            "membuang bagian yang busuk dan mencucinya terlebih dahulu. Begitu pula data mentah — "
            "perlu dibersihkan dan diolah sebelum masuk ke model.\n\n"
            "**Teknik Utama — Min-Max Scaling:**\n\n"
            "$$X_{scaled} = \\frac{X - X_{min}}{X_{max} - X_{min}}$$\n\n"
            "---\n\n"
            "> [!contoh]\n"
            f"> **Worked Example: Perhitungan {step} Tuntas**\n"
            ">\n"
            "> **Diketahui:** Dataset $X = [20, 30, 50]$\n"
            "> - $X_{min} = 20$, $X_{max} = 50$, Rentang = $30$\n"
            ">\n"
            "> **Langkah demi Langkah:**\n"
            "> 1. $X = 20$: $\\frac{20 - 20}{30} = 0$\n"
            "> 2. $X = 30$: $\\frac{30 - 20}{30} = \\frac{10}{30} \\approx 0.33$\n"
            "> 3. $X = 50$: $\\frac{50 - 20}{30} = \\frac{30}{30} = 1$\n"
            ">\n"
            "> **Hasil:** `[0, 0.33, 1]`\n\n"
            "---\n\n"
            "> [!coba]\n"
            f"> **Soal — {step}:**\n"
            "> Dataset $X = [10, 20, 30, 40]$. Hitung Min-Max Scaling untuk $X = 25$.\n"
            ">\n"
            "> ---\n"
            "> **Pembahasan:**\n"
            "> 1. $X_{min} = 10$, $X_{max} = 40$, Rentang = $30$\n"
            "> 2. $X_{scaled} = \\frac{25 - 10}{30} = \\frac{15}{30} = 0.5$\n"
            "> 3. **Jawaban:** $0.5$\n\n"
            "---\n\n"
            "> [!perhatian]\n"
            "> ❌ **Data Leakage:** Jangan fit scaler pada seluruh data sebelum split train/test!\n"
            "> ✅ **Benar:** Split → Fit pada train → Transform train & test.\n\n"
            "---\n\n"
            "> [!ingat]\n"
            f"> **Ringkasan — {step}:**\n"
            f"> - {step} menentukan kualitas input model dalam {topic}.\n"
            "> - Selalu fit transformer hanya pada data training.\n"
            "> - Pilih teknik scaling berdasarkan distribusi data.\n\n"
            "---\n\n"
            "> [!quiz]\n"
            f"> **Soal 1:** Mengapa kita tidak fit scaler pada seluruh data?\n"
            "> **Soal 2:** Kapan StandardScaler lebih baik dari MinMaxScaler?\n"
            ">\n"
            "> ---\n"
            "> **Jawaban:**\n"
            "> 1. Karena scaler akan melihat data test, mengakibatkan data leakage.\n"
            "> 2. Ketika data berdistribusi normal dan tidak ada outlier signifikan."
        ),
        "videos": [],
    }


def _programming_lesson(step: str, topic: str) -> dict:
    return {
        "content": (
            f"### Alur Konseptual: {step}\n\n"
            f"Dalam topik **{topic}**, langkah **{step}** merupakan konsep yang harus dikuasai "
            "untuk menulis kode yang efisien dan terstruktur.\n\n"
            "---\n\n"
            "> [!tujuan]\n"
            f"> **Tujuan Pembelajaran — {step}:**\n"
            f"> - [ ] **Menjelaskan** konsep {step} dan cara kerjanya dalam {topic}.\n"
            f"> - [ ] **Mengidentifikasi** kapan menggunakan {step} dan kapan tidak.\n"
            f"> - [ ] **Menerapkan** {step} dalam kode contoh secara langsung.\n"
            f"> - [ ] **Menganalisis** kesalahan umum saat implementasi {step}.\n\n"
            "---\n\n"
            f"## Konsep {step}\n\n"
            f"**{step}** dalam {topic} membantu kita menulis kode yang lebih rapi, efisien, "
            "dan mudah dipelihara.\n\n"
            "**Intuisi:** Pemrograman seperti membangun rumah — setiap balok harus diletakkan "
            f"dengan benar agar strukturnya kokoh. {topic} adalah salah satu balok penting itu.\n\n"
            "**Contoh Kode:**\n\n"
            "```python\n"
            "# Implementasi konsep langkah ini\n"
            "def langkah_initi(data):\n"
            '    """Fungsi untuk menerapkan konsep langkah ini"""\n'
            "    hasil = []\n"
            "    for item in data:\n"
            "        # Proses setiap item\n"
            "        hasil.append(item * 2)\n"
            "    return hasil\n"
            "```\n\n"
            "---\n\n"
            "> [!contoh]\n"
            f"> **Worked Example — {step}:**\n"
            ">\n"
            "> ```python\n"
            "> # Contoh penggunaan\n"
            "> data = [1, 2, 3, 4, 5]\n"
            "> hasil = langkah_initi(data)\n"
            "> print(hasil)  # [2, 4, 6, 8, 10]\n"
            "> ```\n"
            ">\n"
            "> **Penjelasan:**\n"
            "> 1. Input: list `[1, 2, 3, 4, 5]`\n"
            "> 2. Proses: setiap elemen dikalikan 2\n"
            "> 3. Output: `[2, 4, 6, 8, 10]`\n\n"
            "---\n\n"
            "> [!coba]\n"
            f"> **Tantangan — {step}:**\n"
            "> Modifikasi fungsi di atas agar hanya memproses bilangan genap.\n"
            ">\n"
            "> ---\n"
            "> **Solusi:**\n"
            "> ```python\n"
            "> def langkah_genap(data):\n"
            ">     return [x * 2 for x in data if x % 2 == 0]\n"
            "> ```\n\n"
            "---\n\n"
            "> [!ingat]\n"
            f"> **Ringkasan — {step}:**\n"
            f"> - {step} membantu menulis kode yang lebih terstruktur dalam {topic}.\n"
            "> - Selalu berikan docstring untuk menjelaskan tujuan fungsi.\n"
            "> - Gunakan list comprehension untuk kode yang lebih ringkas.\n\n"
            "---\n\n"
            "> [!quiz]\n"
            f"> **Soal 1:** Kapan kamu sebaiknya menggunakan {step} vs pendekatan lain?\n"
            "> **Soal 2:** Apa dampak performa dari penggunaan teknik ini pada data besar?\n"
            ">\n"
            "> ---\n"
            "> **Jawaban:**\n"
            f"> 1. Gunakan {step} ketika struktur data dan pola iterasi sudah jelas.\n"
            "> 2. Perlu optimasi dengan teknik memoisasi atau lazy evaluation."
        ),
        "videos": [],
    }


def _history_lesson(step: str, topic: str) -> dict:
    return {
        "content": (
            f"### Alur Konseptual: {step}\n\n"
            f"Dalam topik **{topic}**, langkah **{step}** merupakan bagian penting untuk memahami "
            "konteks sejarah secara utuh.\n\n"
            "---\n\n"
            "> [!tujuan]\n"
            f"> **Tujuan Pembelajaran — {step}:**\n"
            f"> - [ ] **Menjelaskan** latar belakang dan penyebab {step} dalam konteks {topic}.\n"
            f"> - [ ] **Mengidentifikasi** tokoh-tokoh kunci dan peran mereka dalam {step}.\n"
            f"> - [ ] **Menguraikan** urutan kronologis peristiwa dalam {step}.\n"
            f"> - [ ] **Menganalisis** dampak {step} terhadap perkembangan selanjutnya.\n\n"
            "---\n\n"
            f"## Latar Belakang {step}\n\n"
            f"**{step}** dalam konteks {topic} tidak terjadi secara tiba-tiba. Ada berbagai faktor "
            "sosial, politik, ekonomi, dan budaya yang mendorong terjadinya peristiwa ini.\n\n"
            "**Kondisi Sebelumnya:**\n"
            "- Faktor politik yang tidak stabil\n"
            "- Pengaruh pihak asing / kolonial\n"
            "- Ketidakpuasan masyarakat terhadap kondisi yang ada\n\n"
            "**Tokoh-Tokoh Kunci:**\n"
            f"Beberapa tokoh yang berperan penting dalam {step}:\n"
            "- Tokoh utama: peran sebagai pemimpin / penggerak\n"
            "- Tokoh pendukung: peran sebagai penyokong / pelaksana\n"
            "- Tokoh penentang: peran sebagai penentang / hambatan\n\n"
            "---\n\n"
            "> [!contoh]\n"
            f"> **Kronologi {step}:**\n"
            ">\n"
            "> 1. **Tahap Persiapan** — Kondisi yang mendahului peristiwa\n"
            "> 2. **Tahap Pelaksanaan** — Peristiwa utama terjadi\n"
            "> 3. **Tahap Akhir** — Hasil dan dampak langsung\n\n"
            "---\n\n"
            "> [!coba]\n"
            f"> **Analisis — {step}:**\n"
            f"> 1. Apa faktor utama yang menyebabkan {step} terjadi?\n"
            f"> 2. Bagaimana {step} mempengaruhi kehidupan masyarakat pada masa itu?\n"
            f"> 3. Apakah ada perspektif berbeda dari pihak yang berbeda tentang {step}?\n\n"
            "---\n\n"
            "> [!ingat]\n"
            f"> **Ringkasan — {step}:**\n"
            f"> - {step} dipengaruhi oleh berbagai faktor yang saling berkaitan.\n"
            "> - Setiap peristiwa sejarah memiliki penyebab dan akibat yang kompleks.\n"
            f"> - Memahami {step} membantu kita belajar dari pengalaman masa lalu.\n\n"
            "---\n\n"
            "> [!quiz]\n"
            f"> **Soal 1:** Apa dampak jangka panjang dari {step}?\n"
            f"> **Soal 2:** Bagaimana pandangan berbeda dari berbagai sejarawan tentang {step}?\n"
            ">\n"
            "> ---\n"
            "> **Jawaban:**\n"
            "> 1. Dampak jangka panjang mencakup perubahan struktur sosial dan politik.\n"
            "> 2. Setiap sejarawan memiliki sudut pandang yang dipengaruhi latar belakangnya."
        ),
        "videos": [],
    }


def _cs_lesson(step: str, topic: str) -> dict:
    return {
        "content": (
            f"### Alur Konseptual: {step}\n\n"
            f"Dalam topik **{topic}**, langkah **{step}** merupakan konsep dasar yang harus dikuasai "
            "sebelum melangkah ke implementasi yang lebih kompleks.\n\n"
            "---\n\n"
            "> [!tujuan]\n"
            f"> **Tujuan Pembelajaran — {step}:**\n"
            f"> - [ ] **Menjelaskan** prinsip kerja {step} dalam konteks {topic}.\n"
            f"> - [ ] **Mengidentifikasi** kapan menggunakan {step} dalam pemecahan masalah.\n"
            f"> - [ ] **Menerapkan** {step} dalam kode atau diagram alur.\n"
            f"> - [ ] **Menganalisis** kompleksitas waktu dan ruang dari {step}.\n\n"
            "---\n\n"
            f"## Konsep {step}\n\n"
            f"**{step}** dalam {topic} menjelaskan bagaimana komputer menyelesaikan masalah "
            "dengan pendekatan sistematis.\n\n"
            "**Intuisi:** Algoritma seperti resep masakan — langkah-langkah yang jelas, berurutan, "
            "dan menghasilkan output yang dapat diprediksi dari input tertentu.\n\n"
            "**Pseudocode:**\n\n"
            "```\n"
            "ALGORITMA Langkah_Initi(input):\n"
            "    hasil = []\n"
            "    UNTUK setiap elemen DALAM input:\n"
            "        proses(elemen)\n"
            "        tambahkan ke hasil\n"
            "    KEMBALIKAN hasil\n"
            "```\n\n"
            "---\n\n"
            "> [!contoh]\n"
            f"> **Worked Example — {step}:**\n"
            ">\n"
            "> **Input:** `[3, 1, 4, 1, 5]`\n"
            "> **Proses:**\n"
            "> 1. elemen 3 → proses → hasil `[3]`\n"
            "> 2. elemen 1 → proses → hasil `[3, 1]`\n"
            "> 3. elemen 4 → proses → hasil `[3, 1, 4]`\n"
            "> 4. elemen 1 → proses → hasil `[3, 1, 4, 1]`\n"
            "> 5. elemen 5 → proses → hasil `[3, 1, 4, 1, 5]`\n"
            ">\n"
            "> **Kompleksitas:** Waktu $O(n)$, Ruang $O(n)$\n\n"
            "---\n\n"
            "> [!coba]\n"
            f"> **Latihan — {step}:**\n"
            "> Implementasikan algoritma di atas dalam Python. Modifikasi agar hanya memproses "
            "> elemen yang lebih besar dari 2.\n"
            ">\n"
            "> ---\n"
            "> **Solusi:**\n"
            "> ```python\n"
            "> def langkah_initi(data):\n"
            ">     return [x for x in data if x > 2]\n"
            "> ```\n\n"
            "---\n\n"
            "> [!ingat]\n"
            f"> **Ringkasan — {step}:**\n"
            f"> - {step} adalah pendekatan sistematis dalam {topic}.\n"
            "> - Pertimbangkan kompleksitas waktu dan ruang saat memilih algoritma.\n"
            "> - Selalu uji dengan kasus tepi (edge cases).\n\n"
            "---\n\n"
            "> [!quiz]\n"
            f"> **Soal 1:** Bagaimana kompleksitas {step} berubah jika input berlipat ganda?\n"
            f"> **Soal 2:** Apakah ada kasus di mana pendekatan alternatif lebih baik dari {step}?\n"
            ">\n"
            "> ---\n"
            "> **Jawaban:**\n"
            "> 1. Untuk $O(n)$, waktu juga berlipat ganda. Untuk $O(n^2)$, waktu naik 4x lipat.\n"
            "> 2. Ya, untuk data terurut, pendekatan $O(n \\log n)$ bisa lebih optimal."
        ),
        "videos": [],
    }


def _general_lesson(step: str, topic: str) -> dict:
    return {
        "content": (
            f"### Alur Konseptual: {step}\n\n"
            f"Dalam topik **{topic}**, langkah **{step}** merupakan bagian penting yang harus "
            "dipahami untuk membangun fondasi yang kuat.\n\n"
            "---\n\n"
            "> [!tujuan]\n"
            f"> **Tujuan Pembelajaran — {step}:**\n"
            f"> - [ ] **Menjelaskan** konsep inti {step} dalam konteks {topic}.\n"
            f"> - [ ] **Mengidentifikasi** penerapan {step} dalam situasi nyata.\n"
            f"> - [ ] **Menerapkan** teknik {step} pada contoh kasus secara step-by-step.\n"
            f"> - [ ] **Menganalisis** batasan dan kesalahan umum dalam {step}.\n\n"
            "---\n\n"
            f"## Konsep {step}\n\n"
            f"**{step}** dalam konteks {topic} menjelaskan prinsip-prinsip dasar yang perlu "
            "dikuasai untuk memahami topik ini secara menyeluruh.\n\n"
            f"**Intuisi:** {topic} adalah konsep yang bisa kita temukan dalam kehidupan sehari-hari, "
            "meskipun sering kali tidak disadari.\n\n"
            "**Contoh Konkret:**\n"
            f"Bayangkan situasi sehari-hari yang melibatkan {step} — dari sinilah kita bisa "
            "melihat betapa relevannya konsep ini dalam kehidupan nyata.\n\n"
            "---\n\n"
            "> [!contoh]\n"
            f"> **Worked Example — {step}:**\n"
            ">\n"
            "> **Langkah 1:** Identifikasi masalah dan tentukan data yang tersedia.\n"
            "> **Langkah 2:** Pilih pendekatan yang sesuai berdasarkan karakteristik data.\n"
            "> **Langkah 3:** Terapkan teknik dan periksa hasilnya secara kritis.\n"
            "> **Langkah 4:** Interpretasikan hasil dan hubungkan dengan teori.\n\n"
            "---\n\n"
            "> [!coba]\n"
            f"> **Latihan — {step}:**\n"
            f"> 1. Jelaskan dengan bahasamu sendiri apa itu {step}.\n"
            f"> 2. Berikan satu contoh penerapan {step} dalam kehidupan nyata.\n"
            f"> 3. Sebutkan satu kesalahan umum yang sering terjadi saat menerapkan {step}.\n\n"
            "---\n\n"
            "> [!ingat]\n"
            f"> **Ringkasan — {step}:**\n"
            f"> - {step} adalah fondasi penting dalam {topic}.\n"
            "> - Pemahaman konsep lebih penting dari sekadar menghafal.\n"
            "> - Latihan dan penerapan nyata memperkuat pemahaman.\n\n"
            "---\n\n"
            "> [!quiz]\n"
            f"> **Soal 1:** Apa yang terjadi jika {step} tidak diterapkan dengan benar?\n"
            f"> **Soal 2:** Bagaimana cara memverifikasi pemahaman tentang {step}?\n"
            ">\n"
            "> ---\n"
            "> **Jawaban:**\n"
            "> 1. Dampaknya bisa berupa kesalahan analisis atau hasil yang tidak akurat.\n"
            "> 2. Mengerjakan soal berbagai tingkat dan mendiskusikan dengan orang lain."
        ),
        "videos": [],
    }


def mock_lesson(step_title: str, topic_title: str) -> dict:
    subject = _detect_subject(f"{step_title} {topic_title}")
    generators = {
        "physics": _physics_lesson,
        "math": _math_lesson,
        "data": _data_lesson,
        "programming": _programming_lesson,
        "cs": _cs_lesson,
        "history": _history_lesson,
    }
    gen = generators.get(subject, _general_lesson)
    return gen(step_title, topic_title)
