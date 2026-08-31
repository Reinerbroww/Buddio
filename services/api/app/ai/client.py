"""Unified AI entry point for Buddio.

Uses Google Gemini when GEMINI_API_KEY is configured, otherwise falls back to the
rule-based mock generators so the app always works end-to-end.
"""
import json
import logging
from typing import List, Dict, Optional, Tuple

from app.core.config import settings
from app.ai import mock_ai

logger = logging.getLogger("buddio.ai")

# Tutor behavior applied when a chat comes from a lesson context (the materi page).
# It makes the mentor act like a tutor continuing the lesson rather than a generic chatbot.
TUTOR_PROMPT = (
    "\n\nJika pengguna datang dari halaman materi (pesan mengandung konteks seperti "
    "'sedang belajar materi', 'topik', atau meminta dijelaskan/memberi contoh), "
    "berperilakulah seperti TUTOR yang melanjutkan pelajaran, bukan chatbot yang menjawab "
    "pertanyaan lepas.\n\n"
    "Cara sebagai tutor:\n"
    "1. Identifikasi kebingungan spesifik yang disebutkan pengguna.\n"
    "2. Jelaskan pada tingkat yang sesuai, dengan mengacu pada materi yang sedang dipelajari.\n"
    "3. Beri satu contoh singkat bila membantu.\n"
    "4. Jangan langsung membuang penjelasan umum yang sangat panjang — jelaskan fokus dulu.\n"
    "5. Akhiri dengan satu pertanyaan lanjutan kecil untuk mengecek pemahaman, atau satu soal "
    "latihan singkat bila berguna.\n"
    "6. Lanjutkan berdasarkan jawaban pengguna berikutnya.\n\n"
    "Saat pengguna meng-highlight teks tertentu dan meminta 'jelaskan bagian ini', jawab SPESIFIK "
    "untuk bagian/teks yang disorot dalam konteks materi tersebut, bukan jawaban umum yang "
    "berlaku untuk topik lain.\n"
    "Jaga kebenaran teknis. Jangan mengarang fakta atau rumus. Bila ragu, beri penjelasan yang hati-hati."
)

SYSTEM_PROMPT = (
    "Kamu adalah Buddio, mentor belajar AI yang ramah, sabar, dan pedagogis. "
    "Selalu jawab dalam Bahasa Indonesia. Sesuaikan tingkat bahasa dengan jenjang pengguna "
    "(SD, SMP, SMA, mahasiswa, self learner). "
    "Beri penjelasan bertahap, gunakan analogi sederhana, dan jangan langsung memberi jawaban "
    "final untuk soal latihan ujian — bimbing pengguna untuk sampai ke jawaban sendiri."
)


def get_system_prompt(grade_level: str = "sma") -> str:
    level = (grade_level or "sma").lower().strip()
    
    base_instruction = (
        "Kamu adalah Buddio, mentor belajar AI yang sangat ramah, sabar, dan interaktif. "
        "Selalu jawab dalam Bahasa Indonesia. Tulis penjelasan secara bersih, terstruktur, tidak bertele-tele, "
        "dan hindari dinding teks yang membosankan. Gunakan markdown dengan baik (bullet points, kata kunci penting ditebalkan) "
        "serta jaga agar format jawaban terlihat rapi dan memiliki spasi antar paragraf yang cukup.\n\n"
    )
    
    if level == "sd":
        specific = (
            "GAYA BAHASA & TONE (Jenjang SD - Sekolah Dasar):\n"
            "- Bertindaklah sebagai 'Kak Buddio', kakak mentor yang super ceria, hangat, penuh semangat, dan sabar.\n"
            "- Gunakan kalimat-kalimat pendek, ramah, dan sangat mudah dipahami anak kecil. Panggil pengguna dengan 'Adik' atau 'Kamu'.\n"
            "- Sering gunakan emoji yang lucu dan berwarna (seperti 🌟, 🚀, 🎉, 🎈, 🧸) untuk menyemangati, tapi pastikan tulisan tetap rapi.\n"
            "- Berikan penjelasan yang bersih, visual, dan gunakan analogi dunia anak-anak (misal: membagi kue, petualangan di luar angkasa, mainan).\n"
            "- Jangan pernah memberikan jawaban langsung untuk tugas sekolah. Bimbing mereka selangkah demi selangkah dengan pertanyaan kecil pemantik agar mereka bangga menemukan jawabannya sendiri.\n"
            "- Jika mereka menjawab benar, berikan pujian yang sangat positif dan meriah!"
        )
    elif level == "smp":
        specific = (
            "GAYA BAHASA & TONE (Jenjang SMP - Sekolah Menengah Pertama):\n"
            "- Bertindaklah sebagai mentor belajar yang seru, keren, bersahabat, dan gaul tapi tetap sopan.\n"
            "- Gunakan bahasa yang komunikatif dan santai (misalnya menggunakan 'kamu', kata-kata yang interaktif, tanpa terlalu formal).\n"
            "- Gunakan analogi yang relevan dengan kehidupan remaja masa kini (seperti game, hobi, teknologi, olahraga, atau media sosial).\n"
            "- Gunakan emoji yang aktif dan memotivasi (seperti 💡, 🔥, 👍, 🧠) untuk membuat obrolan terasa dinamis dan tidak kaku.\n"
            "- Penjelasan harus bersih dan terstruktur: tebalkan istilah penting dan batasi paragraf maksimal 3 kalimat.\n"
            "- Dorong rasa ingin tahu mereka. Bantu mereka menyelesaikan soal dengan memberikan petunjuk/hint logis dan membiarkan mereka menyelesaikannya sendiri."
        )
    elif level == "sma":
        specific = (
            "GAYA BAHASA & TONE (Jenjang SMA - Sekolah Menengah Atas):\n"
            "- Bertindaklah sebagai mentor belajar yang cerdas, inspiratif, suportif, dan profesional.\n"
            "- Gunakan gaya bahasa semi-formal yang ramah dan hangat. Gunakan sapaan yang sopan dan mendukung.\n"
            "- Gunakan analogi konseptual yang menghubungkan teori dengan penerapan nyata di dunia sains, teknologi, atau kehidupan sehari-hari.\n"
            "- Struktur tulisan harus sangat bersih dan rapi: gunakan heading jika penjelasan panjang, gunakan poin-poin teratur, dan pisahkan antar ide dengan baris baru.\n"
            "- Berikan pemahaman konsep yang kokoh (mengapa rumus/konsep ini ada, bukan sekadar menghafalnya). Tuntun logika berpikir mereka ketika mendiskusikan soal latihan."
        )
    elif level in ("mahasiswa", "self_learner"):
        specific = (
            "GAYA BAHASA & TONE (Jenjang Perguruan Tinggi / Pembelajar Mandiri):\n"
            "- Bertindaklah sebagai partner diskusi akademis dan profesional yang berwawasan luas, analitis, mendalam, namun tetap ramah.\n"
            "- Gunakan bahasa Indonesia ilmiah yang baik dan benar (semi-formal/formal), dengan istilah-istilah teknis atau akademis yang tepat sesuai bidang studi.\n"
            "- Sajikan penjelasan yang komprehensif, logis, dan mendalam. Fokus pada konseptualisasi, metodologi, dan studi kasus/aplikasi praktis di dunia nyata atau industri.\n"
            "- Penulisan harus sangat bersih, profesional, dan efisien. Gunakan heading, blok kode (code blocks) jika relevan, tabel, atau diagram berbasis teks (markdown), serta spasi yang baik.\n"
            "- Berikan saran metode belajar mandiri atau referensi literatur jika relevan. Hormati kemandirian berpikir mereka dan ajak berdiskusi secara mendalam."
        )
    else:
        specific = (
            "GAYA BAHASA & TONE (Umum):\n"
            "- Jadilah mentor belajar yang ramah, komunikatif, dan sabar.\n"
            "- Gunakan bahasa yang mudah dipahami, bersih, terstruktur dengan markdown, dan gunakan emoji secara proporsional.\n"
            "- Jelaskan secara bertahap dengan analogi sederhana dan tuntun pengguna ke pemecahan masalah."
        )
        
    return base_instruction + specific


def _is_gemini_available() -> bool:
    return bool(settings.GEMINI_API_KEY) and not settings.FORCE_MOCK_AI


_gemini_client_instance = None


def _gemini_client():
    global _gemini_client_instance
    if _gemini_client_instance is None:
        from google import genai
        _gemini_client_instance = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _gemini_client_instance


def _generate_json(prompt: str, max_tokens: int = 2048, temperature: float = 0.6, system_instruction: Optional[str] = None) -> dict:
    """Call Gemini and parse a JSON object from the response."""
    client = _gemini_client()
    from google.genai import types
    resp = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction or SYSTEM_PROMPT,
            response_mime_type="application/json",
            max_output_tokens=max_tokens,
            temperature=temperature,
        ),
    )
    text = (resp.text or "").strip()
    # Some models wrap JSON in markdown fences.
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


class BuddioAI:
    """Facade over Gemini with graceful mock fallback."""

    @property
    def mode(self) -> str:
        return "gemini" if _is_gemini_available() else "mock"

    def chat(
        self,
        message: str,
        history: Optional[List[Dict]] = None,
        grade_level: str = "sma",
        topic_title: str = "",
    ) -> Tuple[str, int, str]:
        """Returns (answer, token_usage, mode)."""
        if not _is_gemini_available():
            return mock_ai.mock_chat(message, topic_title), 0, "mock"

        parts = []
        parts.append(
            "Berikut riwayat percakapan sebelumnya (jika ada). Gunakan untuk menjaga konteks.\n"
            + json.dumps(history[-10:] if history else [], ensure_ascii=False)
        )
        parts.append(
            f"Jenjang pengguna: {grade_level or 'umum'}. Topik aktif: {topic_title or '-'}.\n"
            f"Pertanyaan user: {message}"
        )
        prompt = "\n".join(parts)

        sys_prompt = get_system_prompt(grade_level)
        # If the message carries lesson context, add tutor behavior so the mentor continues
        # the lesson instead of acting like a generic chatbot.
        lesson_context_markers = (
            "sedang belajar materi",
            "bagian ini",
            "tolong jelaskan",
            "tolong berikan contoh",
            "materi ini",
        )
        if any(m in message.lower() for m in lesson_context_markers):
            sys_prompt = sys_prompt + TUTOR_PROMPT
        try:
            from google.genai import types
            resp = _gemini_client().models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt, max_output_tokens=2048, temperature=0.6
                ),
            )
            answer = (resp.text or "").strip()
            usage = getattr(resp, "usage_metadata", None)
            token_usage = int(getattr(usage, "total_token_count", 0)) if usage else 0
            if not answer:
                raise ValueError("Empty Gemini response")
            return answer, token_usage, "gemini"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini chat failed, falling back to mock: %s", exc)
            return mock_ai.mock_chat(message, topic_title), 0, "mock"

    def generate_roadmap(self, topic_title: str, grade_level: str = "sma", goal: str = "") -> Tuple[dict, str]:
        """Returns (roadmap_dict, mode)."""
        if not _is_gemini_available():
            return mock_ai.mock_roadmap(topic_title, goal), "mock"

        prompt = (
            f"Buatkan roadmap belajar untuk topik '{topic_title}' untuk jenjang {grade_level or 'sma'}. "
            + (f"Tujuan akhir belajar pengguna: {goal}. " if goal else "")
            + "Kembalikan JSON dengan format: "
            + '{"title": "...", "difficulty": "Mudah|Menengah|Sulit", "estimated_hours": <angka>, '
            + '"steps": [{"order_number": 1, "title": "...", "description": "..."}]}. '
            + "Buat 5-7 langkah yang berurutan, ditulis dalam Bahasa Indonesia.\n\n"
            + "PENTING UNTUK DESKRIPSI TIAP LANGKAH (description):\n"
            + "Tulis deskripsi secara mendetail, bersih, terstruktur, dan tidak membosankan. "
            + "Gunakan pemformatan teks yang rapi dengan baris baru (newline) dan poin-poin agar mudah dibaca.\n"
            + "Di dalam tiap deskripsi langkah, cantumkan:\n"
            + "1. Apa yang dipelajari: penjelasan konsep inti secara sederhana.\n"
            + "2. Mengapa ini penting: manfaat konsep ini.\n"
            + "3. Aktivitas belajar: cara praktis mempelajarinya.\n\n"
            + f"Sesuaikan tingkat kesulitan, analogi, dan kedetailan penjelasan dengan jenjang pendidikan pengguna: {grade_level or 'sma'}.\n"
            + "- Jenjang SD: penjelasan super sederhana, ramah, penuh semangat, gunakan analogi menyenangkan, tanpa rumus rumit.\n"
            + "- Jenjang SMP: komunikatif, seru, tantang rasa ingin tahu, hubungkan dengan hal terdekat di sekitarnya.\n"
            + "- Jenjang SMA: penjelasan konseptual yang jelas, seimbangkan teori dan praktek.\n"
            + "- Jenjang Mahasiswa/Self Learner: mendalam, logis, terperinci, gunakan istilah standar industri/akademik."
        )
        
        roadmap_sys_prompt = (
            "Kamu adalah Buddio, mentor belajar AI yang ahli menyusun kurikulum dan peta belajar (roadmap) yang personal, terstruktur, dan pedagogis. "
            "Tugasmu adalah menyusun langkah belajar yang jelas, berurutan, dan terperinci dalam Bahasa Indonesia."
        )
        
        try:
            data = _generate_json(prompt, max_tokens=4096, system_instruction=roadmap_sys_prompt)
            data.setdefault("steps", [])
            return data, "gemini"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini roadmap failed, falling back to mock: %s", exc)
            return mock_ai.mock_roadmap(topic_title, goal), "mock"

    def generate_quiz(self, topic_title: str, grade_level: str = "sma", count: int = 5) -> Tuple[dict, str]:
        """Returns (quiz_dict, mode)."""
        if not _is_gemini_available():
            return mock_ai.mock_quiz(topic_title, count), "mock"

        prompt = (
            f"Buatkan kuis {count} soal pilihan ganda untuk topik '{topic_title}' jenjang {grade_level or 'umum'}. "
            "Setiap soal harus memiliki 4 pilihan jawaban. Kembalikan JSON dengan format: "
            '{"title": "...", "questions": [{"question": "...", "options": ["a","b","c","d"], '
            '"answer_index": <indeks benar>, "explanation": "..."}]}. '
            "Tulis semua dalam Bahasa Indonesia."
        )
        try:
            data = _generate_json(prompt, max_tokens=4096)
            data.setdefault("questions", [])
            data["questions"] = data["questions"][:count]
            return data, "gemini"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini quiz failed, falling back to mock: %s", exc)
            return mock_ai.mock_quiz(topic_title, count), "mock"

    def generate_lesson(
        self,
        step_title: str,
        topic_title: str,
        grade_level: str = "sma",
        step_description: str = "",
    ) -> Tuple[dict, str]:
        """Generate rich lesson content (materi) with YouTube video suggestions.

        Returns (lesson_dict, mode) where lesson_dict has:
            content: str   -- rich markdown materi
            videos: list   -- [{"title": "...", "url": "...", "description": "..."}]
        """
        if not _is_gemini_available():
            return mock_ai.mock_lesson(step_title, topic_title), "mock"

        prompt = (
            f'Buatkan materi pembelajaran untuk langkah "{step_title}" '
            f'dalam topik "{topic_title}" untuk jenjang {grade_level or "sma"}.\n\n'
            f"Deskripsi langkah: {step_description or '-'}\n\n"
            "Kembalikan JSON dengan format:\n"
            "{\n"
            '  "content": "...",\n'
            '  "videos": [\n'
            '    {"title": "Judul Video", "url": "https://www.youtube.com/watch?v=VIDEO_ID", "description": "Deskripsi singkat"}\n'
            "  ]\n"
            "}\n\n"
            "=================================================================\n"
            " TUJUAN UTAMA\n"
            "=================================================================\n\n"
            "Tujuanmu BUKAN menghasilkan catatan yang terlihat edukatif. Tujuanmu adalah "
            "MENGAJAR dengan benar sehingga siswa benar-benar menguasai materi ini.\n\n"
            "Mulai dengan pertanyaan inti:\n"
            "\"Apa yang siswa PERLU TAHUI dan PERLU BISA LAKUKAN setelah mempelajari topik ini?\"\n"
            "Lalu bangun seluruh materi di sekitar jawabannya.\n\n"
            "Prioritas isi (urut dari terpenting):\n"
            "  1. Keakuratan (accuracy)  →  fakta, rumus, sintaks, mekanisme harus BENAR\n"
            "  2. Pengetahuan (knowledge) → konsep, istilah, mekanisme inti benar-benar diajarkan\n"
            "  3. Pemahaman (understanding) → siswa paham APA, MENGAPA, BAGAIMANA\n"
            "  4. Penerapan (application) → bisa dipakai untuk masalah nyata\n"
            "  5. Latihan (practice) → soal yang menguji penerapan\n"
            "  6. Keterlibatan (engagement) → membuat belajar menyenangkan, TAPI hanya sebagai pendukung\n\n"
            "UJI INTERNAL (WAJIB dipakai pada setiap kalimat):\n"
            "\"Jika kalimat ini dihapus, apakah siswa kehilangan pengetahuan atau pemahaman yang berguna?\"\n"
            "Jika tidak → hapus kalimat tersebut.\n\n"
            "=================================================================\n"
            " FILOSOFI: 'AJAR DULU, HIBUR KEMUDIAN'\n"
            "=================================================================\n\n"
            "- Konten teknis adalah konten UTAMA. Analogi dan penyemangat hanyalah alat bantu.\n"
            "- JANGAN mengorbankan kedalaman atau kebenaran teknis demi terdengar lebih santai.\n"
            "- NADA: Indonesia yang jelas, ringkas, dan tepat secara akademis. Boleh hangat, "
            "tapi JANGAN bertele-tele atau menggurui.\n"
            "- JANGAN memakai analogi sebagai pengganti penjelasan teknis. Gunakan maksimal 0-1 "
            "analogi kuat per konsep sulit, dan SELALU ikuti dengan penjelasan teknis yang sebenarnya.\n\n"
            "HINDARI 'filler edukatif' yang berulang seperti:\n"
            "  'Semua orang memulai dari nol', 'Kamu pasti bisa!', 'Jangan menyerah',\n"
            "  'Bayangkan ini seperti game', 'Jelaskan ke kucingmu', 'Belajar seperti naik sepeda',\n"
            "  'Ini fondasi segalanya', 'Ayo kita mulai!', 'Jangan khawatir, akan kita buat mudah!'\n"
            "Ungkapan seperti itu TIDAK BOLEH menjadi pola yang berulang. Setiap paragraf harus "
            "memberikan nilai edukatif yang nyata.\n\n"
            "=================================================================\n"
            " STRUKTUR: PILIH SESUAI JENIS TOPIK (TIDAK BISA SATU TEMPLATE UNTUK SEMUA)\n"
            "=================================================================\n\n"
            "Tentukan jenis topik ini, lalu pilih struktur yang paling tepat. JANGAN memaksakan\n"
            "semua bagian yang sama untuk setiap topik. Gunakan bagian yang relevan saja.\n\n"
            "Data/ML (data mining, machine learning, data science, statistik):\n"
            "  Konsep → Workflow → Algoritma → Intuisi matematis → Contoh terhitung → "
            "Penerapan praktis → Batasan/asumsi → Kesalahan umum → Latihan\n"
            "Pemrograman (programming):\n"
            "  Konsep → Sintaks → Kode benar → Output yang diharapkan → Penjelasan per baris "
            "(jika berguna) → Edge case & error umum → Latihan pemrograman\n"
            "Matematika/Fisika:\n"
            "  Definisi → Rumus (dengan arti tiap variabel) → Intuisi → Turunan (jika sesuai) → "
            "Contoh hitungan bertahap → Kesalahan umum → Soal latihan\n"
            "Ilmu Komputer (komputer sains, arsitektur, sistem operasi, algoritma):\n"
            "  Definisi → Arsitektur/Proses → Mekanisme internal → Kompleksitas (jika relevan) → "
            "Trade-off → Contoh praktis → Kesalahan umum\n"
            "Sains (biologi, kimia, fisika murni):\n"
            "  Konsep formal → Mekanisme → Proses → Sebab-akibat → Persamaan (jika ada) → "
            "Aplikasi dunia nyata\n"
            "Sejarah/Humaniora:\n"
            "  Konteks → Kronologi → Penyebab → Peristiwa → Akibat → Perspektif → Berpikir kritis\n"
            "Umum:\n"
            "  Kombinasi logis dari bagian di atas sesuai kebutuhan topik.\n\n"
            "PENTING: Adaptasikan kedalaman ke kompleksitas topik dan jenjang. Topik universitas "
            "yang kompleks BOLEH dan HARUS dalam. Topik sederhana cukup ringkas. Jangan membuat "
            "topik tingkat universitas menjadi dangkal demi ringkas.\n\n"
            "=================================================================\n"
            " BAGIAN-BAGIAN YANG MUNGKIN DIGUNAKAN\n"
            "=================================================================\n\n"
            "Pilih dan susun bagian-bagian berikut dengan bijak sesuai jenis topik. "
            "Wajib ada: Tujuan Pembelajaran dan Ringkasan serta Latihan/Self-Check. Lainnya sesuai kebutuhan.\n\n"
            "---\n\n"
            "### Tujuan Pembelajaran (WAJIB, JANGAN PERNAH KOSONG)\n"
            "> [!tujuan]\n"
            "> Setelah mempelajari materi ini, kamu akan bisa:\n"
            "> - [ ] [tujuan terukur]\n"
            "> - [ ] [tujuan terukur]\n\n"
            "Tujuan harus TERUKUR dan sesuai isi materi. Mulai dengan kata kerja konkret:\n"
            "Menjelaskan, Mengidentifikasi, Menghitung, Mengimplementasikan, Membandingkan, "
            "Menerapkan, Menganalisis.\n"
            "Contoh BAIK: 'Menghitung hasil Min-Max Scaling pada dataset kecil'.\n"
            "Contoh BURUK: 'Memahami feature scaling'.\n\n"
            "---\n\n"
            "### Prasyarat (HANYA jika benar-benar diperlukan)\n"
            "> [!prasyarat]\n"
            "> Sebelum mempelajari materi ini, pastikan kamu sudah memahami:\n"
            "> - [konsep A] — [penjelasan singkat]\n\n"
            "Sertakan HANYA jika topik ini butuh pengetahuan sebelumnya yang nyata. "
            "Jika tidak ada prasyarat yang bermakna, BUANG bagian ini. Jangan mengarang prasyarat.\n\n"
            "---\n\n"
            "### Peta Besar / Alur (untuk topik kompleks)\n"
            "Jika topik memiliki beberapa tahap, berikan peta konsep ringkas lalu jelaskan hubungannya.\n"
            "Contoh:\n"
            "<pre>\n"
            "Raw Data → Cleaning → Transformasi → Feature Engineering → Model\n"
            "</pre>\n"
            "Jangan membuat diagram hanya untuk hiasan — pastikan berguna untuk memahami alur.\n\n"
            "---\n\n"
            "### Penjelasan Konsep Inti (bagian utama)\n"
            "Untuk setiap konsep penting, jelaskan secara teknis:\n"
            "- APA itu (definisi yang tepat dan akurat)\n"
            "- MENGAPA penting (masalah apa yang dipecahkan)\n"
            "- BAGAIMANA cara kerjanya (mekanisme/rumus/prosedur sebenarnya)\n"
            "- KAPAN digunakan (kasus penggunaan nyata)\n"
            "- KAPAN TIDAK COCOK (batasan, asumsi, trade-off bila relevan)\n"
            "- Contoh konkret\n\n"
            "Gunakan pola Ajar → Lihat → Coba → Cek untuk konsep penting:\n"
            "  🧠 Ajar: jelaskan konsep dengan benar.\n"
            "  👀 Lihat: tunjukkan contoh nyata / contoh yang dikerjakan.\n"
            "  ✍️ Coba: beri tugas kecil pada siswa.\n"
            "  🧠 Cek: periksa pemahaman.\n"
            "Terapkan pola ini secara natural, jangan diulang secara kaku untuk setiap konsep kecil.\n\n"
            "Gunakan callout penunjang tanpa berlebihan:\n"
            "> [!ingat] — poin krusial yang harus diingat\n"
            "> [!tip] — cara mengingat/teknis yang berguna\n"
            "> [!perhatian] — kesalahan teknis umum\n\n"
            "---\n\n"
            "### Contoh Terhitung / Worked Example (WAJIB untuk konsep terukur)\n"
            "Contoh harus SANGAT MENGAJAR, bukan sekadar hiasan.\n"
            "Berikan data/angka nyata, tulis rumus, jelaskan arti tiap variabel, hitung langkah "
            "demi langkah, tunjukkan hasil akhir, lalu jelaskan arti hasilnya.\n"
            "Siswa harus bisa mengulang prosesnya secara mandiri.\n"
            "Bentuk:\n"
            "> [!contoh]\n"
            "> **Judul contoh**\n"
            "> Diketahui: [data/soal]\n"
            "> Rumus: [rumus]\n"
            "> Langkah: 1)... 2)... 3)...\n"
            "> Hasil: [hasil akhir]\n\n"
            "---\n\n"
            "### Coba Sendiri / Latihan Terpandu (SANGAT DISARANKAN)\n"
            "Setelah contoh, tawarkan latihan pendek. Pisahkan soal dan pembahasan dengan '---' "
            "agar siswa mencoba dulu:\n"
            "> [!coba]\n"
            "> **Coba Sendiri:** [soal singkat]\n"
            "> ---\n"
            "> **Pembahasan:** [langkah demi langkah]\n\n"
            "---\n\n"
            "### Penerapan di Dunia Nyata (HANYA jika bermakna secara teknis)\n"
            "Gunakan pola: Konsep → Masalah → Teknik → Hasil.\n"
            "Jelaskan BAGAIMANA konsep benar-benar dipakai. Jangan menyebut perusahaan/produk "
            "hanya untuk terdengar realistis.\n\n"
            "---\n\n"
            "### Kesalahan Umum / Miskonsepsi (HARUS teknis dan spesifik)\n"
            "Kesalahan harus spesifik pada topik, bukan nasihat motivasi. Bila perlu gunakan:\n"
            "> [!perhatian]\n"
            "> ❌ [kesalahan teknis] → ✅ [cara benar]\n\n"
            "Contoh yang benar (data preprocessing): fitting scaler pada data train+test, "
            "data leakage, memperlakukan kategori nominal sebagai ordinal, mengabaikan nilai hilang.\n"
            "(Pemrograman: off-by-one, scope variabel, mutable default argument, dsb.)\n\n"
            "---\n\n"
            "### Hubungkan Antar Konsep / Connect the Dots (perkaya bila berguna)\n"
            "> [!hubung]\n"
            "> **Kaitannya dengan konsep lain:** ...\n"
            "Jelaskan bagaimana konsep ini berhubungan dengan konsep lain, dan MENGAPA urutannya "
            "demikian. Bantu siswa melihat peta besar.\n\n"
            "---\n\n"
            "### Ringkasan & Poin Kunci (WAJIB, JANGAN PERNAH KOSONG)\n"
            "Ringkas 3-7 poin yang benar-benar penting. Sertakan rumus penting, perbedaan penting, "
            "dan peringatan penting bila ada. JANGAN hanya 'kamu telah belajar tentang X' — "
            "ringkas benar apa arti X.\n"
            "> [!ingat]\n"
            "> **Poin Kunci:**\n"
            "> - [poin]\n"
            "> - [rumus/pembedaan penting]\n\n"
            "---\n\n"
            "### Latihan & Self-Check (WAJIB)\n"
            "Akhiri dengan soal yang menguji PEMAHAMAN, PENERAPAN, dan PENALARAN — bukan hafalan "
            "definisi saja. Gunakan 2-3 level:\n"
            "  Mudah: pemahaman dasar.\n"
            "  Sedang: penerapan.\n"
            "  Tantangan: penalaran, perbandingan, atau skenario nyata.\n"
            "Contoh soal BAIK (bukan 'apa itu feature scaling?'):\n"
            "  'Umur berkisar 18–60, Pendapatan berkisar 3.000.000–500.000.000. Mengapa scaling "
            "penting untuk KNN?'\n"
            "Bentuk:\n"
            "> [!quiz]\n"
            "> **Soal 1 (Mudah):** ...\n"
            "> **Soal 2 (Sedang):** ...\n"
            "> **Soal 3 (Tantangan):** ...\n"
            "Lalu '---' dan '**Jawaban & Pembahasan:**' yang menjelaskan ALASAN jawabannya — "
            "bukan sekadar jawaban satu baris.\n\n"
            "=================================================================\n"
            " HINDARI BAGIAN YANG TIDAK BERGUNA\n"
            "=================================================================\n\n"
            "- Jangan membuka dengan pertanyaan kosong yang tidak mengajarkan apa pun.\n"
            "- Jangan menulis 'kita akan belajar...' sebagai pengganti isi.\n"
            "- Jangan akhiri dengan satu kalimat motivasi wajib. Penutup boleh singkat, faktual, "
            "dan langsung menunjuk ke langkah berikutnya, bukan slogan.\n"
            "- Jangan menampilkan isi yang generik sehingga bisa berlaku untuk topik apa pun.\n\n"
            "=================================================================\n"
            " KEAKURATAN FAKTA (SANGAT PENTING)\n"
            "=================================================================\n\n"
            "JANGAN mengarang: rumus, istilah teknis, algoritma, sintaks pemrograman, fakta "
            "sejarah, klaim ilmiah, statistik, URL, ID YouTube, perilaku API, atau fitur perangkat lunak.\n"
            "Jika ragu, berikan penjelasan yang hati-hati (cautious) daripada terkesan yakin tapi salah.\n"
            "Kebenaran teknis lebih penting daripada terdengar percaya diri.\n\n"
            "=================================================================\n"
            " VIDEO YOUTUBE\n"
            "=================================================================\n\n"
            "Sertakan HANYA video yang benar, relevan, dan ID-nya PASTI valid.\n"
            "ATURAN VIDEO (SANGAT PENTING):\n"
            "- URL harus format video sungguhan: https://www.youtube.com/watch?v=VIDEO_ID\n"
            "  ATAU https://youtu.be/VIDEO_ID (VIDEO_ID = 11 karakter).\n"
            "- DILARANG memakai search URL (https://www.youtube.com/results?...).\n"
            "- DILARANG mengarang ID Video. Jika tidak yakin dengan ID yang benar, KEMBALIKAN "
            "daftar kosong: \"videos\": [].\n"
            "- Jangan menampilkan video yang judul/isinya tidak benar-benar membahas topik ini.\n"
            "- Lebih baik videos kosong daripada video yang menyesatkan.\n\n"
            "=================================================================\n"
            " ATURAN FORMAT MARKDOWN (WAJIB PATUH)\n"
            "=================================================================\n\n"
            "- JANGAN PERNAH menulis karakter escape seperti \\* atau \\** atau \\[. Cukup tulis **bold**\n"
            "  dan *italic* biasa — jangan pakai backslash di depan karakter markdown.\n"
            "- Hanya gunakan sintaks markdown yang didukung: ## / ### heading, **bold**, *italic*,\n"
            "  - list, 1. list, ```code block```, `kode inline`, tabel, dan callout (>[!tipe]).\n"
            "- Setiap callout harus dalam format blok kutipan:\n"
            "  > [!tip]\n"
            "  > isi callout...\n"
            "- Gunakan tabel untuk data/rumus yang berpasangan, dan blok kode untuk kode program.\n"
            "- DILARANG menampilkan sintaks mentah ke siswa. Hasil akhir harus bersih dan dapat "
            "dirender sempurna.\n\n"
            "Sesuaikan kedalaman materi dengan jenjang: "
            f"{grade_level or 'sma'}."
        )

        lesson_sys_prompt = (
            "Kamu adalah Buddio, AI mentor belajar yang TUJUAN UTAMANYA MENGAJAR DENGAN BENAR.\n\n"
            "Filosofimu: 'Ajarkan dulu, hibur kemudian' (teach first, engage second).\n"
            "Prioritas: Keakuratan → Pengetahuan → Pemahaman → Penerapan → Latihan → Keterlibatan.\n\n"
            "Kamu BUKAN generator catatan yang terlihat edukatif. Kamu adalah pengajar yang "
            "membawa siswa dari tidak tahu menjadi mampu memahami dan menerapkan.\n\n"
            "Aturan inti:\n"
            "- Konten teknis yang benar adalah yang utama. Jangan pernah mengorbankan kedalaman "
            "atau kebenaran demi terdengar ramah.\n"
            "- Mulailah dari struktur pengetahuan topik, bukan dari motivasi atau analogi.\n"
            "- Pilih struktur khusus sesuai jenis topik (programming, matematika, data/ML, CS, "
            "sains, sejarah, atau gabungan); jangan memaksakan satu template untuk semua.\n"
            "- Gunakan analogi maksimal 0-1 yang kuat per konsep sulit, dan SELALU ikuti dengan "
            "penjelasan teknis yang sebenarnya.\n"
            "- Contoh (worked example) harus dapat diikuti siswa langkah demi langkah, lengkap "
            "dengan perhitungan.\n"
            "- Latihan harus menguji pemahaman, penerapan, dan penalaran — bukan hafalan definisi.\n"
            "- Setiap kalimat harus punya nilai edukatif. Hapus filler dan penyemangat kosong.\n"
            "- Jangan mengarang fakta, rumus, atau video. Bila ragu, jujur dan hati-hati.\n"
            "- Menghasilkan materi dalam Bahasa Indonesia yang jelas, ringkas, dan tepat secara akademis."
        )

        try:
            data = _generate_json(prompt, max_tokens=8192, system_instruction=lesson_sys_prompt)
            data.setdefault("content", "")
            data.setdefault("videos", [])
            return data, "gemini"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini lesson failed, falling back to mock: %s", exc)
            return mock_ai.mock_lesson(step_title, topic_title), "mock"


buddio_ai = BuddioAI()
