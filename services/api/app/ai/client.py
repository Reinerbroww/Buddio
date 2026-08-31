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
            " ATURAN UTAMA: MATERI INI HARUS TERASA SEPERTI PANDUAN DARI GURU\n"
            "=================================================================\n\n"
            "BAYANGKAN kamu adalah guru privat yang sedang duduk bersebelahan dengan siswa, "
            "menjelaskan topik ini untuk pertama kalinya. Materi yang kamu hasilkan HARUS:\n"
            "- BUKAN dump informasi seperti Wikipedia\n"
            "- BUKAN rangkuman kering dari buku teks\n"
            "- TAPI panduan personal yang membimbing siswa dari nol sampai paham\n\n"
            "PRINSIP PROGRESSIVE LEARNING (alur wajib):\n"
            "  Kenalan → Fondasi → Konsep Inti → Contoh → Penerapan → Latihan → Pemahaman Mendalam\n\n"
            "Jangan semua informasi diberikan sekaligus. Pecah konsep sulit menjadi "
            "bagian-bagian kecil. Jelaskan dengan bahasa sederhana dulu, baru perkenalkan "
            "istilah teknis dan penjelasan lebih dalam.\n\n"
            "=================================================================\n"
            " PENYESUAIAN PER MATA PELAJARAN / JENIS TOPIK\n"
            "=================================================================\n\n"
            "Kenali dulu jenis topiknya lalu sesuaikan cara mengajarnya:\n"
            "- Matematika & Fisika: selalu sertakan contoh soal yang dikerjakan langkah demi\n"
            "  langkah (worked example) dari mudah ke menantang, lengkap dengan alasan tiap langkah.\n"
            "- Pemrograman (programming): gunakan blok kode nyata yang bisa dijalankan, jelaskan\n"
            "  tiap baris penting, dan beri 'coba ubah ini' latihan praktis.\n"
            "- Sains/teori (CS, biologi, kimia): fokus pada konsep, analogi yang kuat, dan kaitkan\n"
            "  dengan fenomena/implikasi nyata agar tidak jadi hafalan.\n"
            "- Bahasa & humaniora: beri contoh pemakaian konkret, latihan terbuka, dan konteks budaya.\n"
            "- Umum: kombinasikan analogi, contoh nyata, dan langkah praktis.\n\n"
            "=================================================================\n"
            " JAMINAN KUALITAS (WAJIB DIPERIKSA SEBELUM MENGIRIM)\n"
            "=================================================================\n\n"
            "- Tujuan Pembelajaran dan Ringkasan TIDAK BOLEH KOSONG atau berbentuk placeholder.\n"
            "- Jika ada section Prasyarat, isinya harus jelas dan tidak kosong.\n"
            "- Setiap istilah asing yang pertama kali muncul diberikan penjelasan singkat.\n"
            "- Tidak ada kalimat generik seperti 'di bagian ini kita akan belajar...' sebagai pengganti isi.\n"
            "- Selalu akhiri dengan latihan/self-check yang benar-benar mengecek pemahaman.\n\n"
            "=================================================================\n"
            " STRUKTUR MATERI\n"
            "=================================================================\n\n"
            "Gunakan section-section berikut SESUAI KEBUTUHAN topik. "
            "Tidak semua section wajib ada — AI harus menentukan mana yang relevan.\n\n"
            "---\n\n"
            "### 1. Pembukaan (WAJIB)\n"
            "Mulai dengan salah satu atau kombinasi:\n"
            "- Pertanyaan pemantik yang bikin penasaran\n"
            "- Analogi dari kehidupan sehari-hari\n"
            "- Fakta menarik atau kejutan\n"
            "- Masalah nyata yang bisa dipecahkan dengan topik ini\n\n"
            "Pembukaan harus bikin siswa BERPIKIR: 'Wah, ini menarik, aku mau tahu lebih lanjut!'\n\n"
            "---\n\n"
            "### 2. Tujuan Pembelajaran\n"
            "Tulis 3-5 poin tujuan belajar yang JELAS dan SPESIFIK.\n"
            "Gunakan format:\n"
            "> [!tujuan]\n"
            "> Setelah mempelajari materi ini, kamu akan bisa:\n"
            "> - [ ] [tujuan 1]\n"
            "> - [ ] [tujuan 2]\n"
            "> - [ ] [tujuan 3]\n\n"
            "Contoh tujuan yang BAIK: 'Menjelaskan perbedaan variabel letak dan konstanta'\n"
            "Contoh tujuan yang BURUK: 'Memahami variabel' (terlalu vague)\n\n"
            "---\n\n"
            "### 3. Prasyarat (OPSIONAL)\n"
            "Jika topik ini membutuhkan pemahaman konsep sebelumnya, gunakan:\n"
            "> [!prasyarat]\n"
            "> Sebelum mempelajari materi ini, pastikan kamu sudah memahami:\n"
            "> - [konsep A] — [penjelasan singkat 1 kalimat]\n"
            "> - [konsep B] — [penjelasan singkat 1 kalimat]\n\n"
            "Jika tidak ada prasyarat penting, SKIP section ini.\n\n"
            "---\n\n"
            "### 4. Penjelasan Konsep Inti (WAJIB)\n"
            "Ini adalah JANTUNG dari materi. Ikuti alur:\n"
            "a) Mulai dengan penjelasan sederhana — apa ini, kenapa penting\n"
            "b) Gunakan analogi sehari-hari yang RELATIF dengan siswa\n"
            "c) Perkenalkan istilah teknis SETELAH konsep dipahami intuitif\n"
            "d) Jelaskan tidak hanya 'APA' tapi juga 'KENAPA' dan 'BAGAIMANA'\n"
            "e) Break down konsep sulit jadi langkah-langkah kecil\n\n"
            "Gunakan callout untuk menonjolkan:\n"
            "> [!tip] — Tips belajar atau cara mengingat\n"
            "> [!funfact] — Fakta menarik yang memperkaya pemahaman\n"
            "> [!ingat] — Poin KRUSIAL yang harus diingat\n\n"
            "Jangan menjelaskan semuanya dalam satu blok teks panjang. "
            "Gunakan heading (###) untuk memecah penjelasan menjadi bagian-bagian logis.\n\n"
            "---\n\n"
            "### 5. Contoh (WAJIB)\n"
            "Berikan 2-3 contoh yang semakin meningkat kesulitannya:\n"
            "- Contoh 1: Paling sederhana, langsung ke inti\n"
            "- Contoh 2: Sedikit lebih kompleks, menambah variasi\n"
            "- Contoh 3 (opsional): Kasus nyata atau tantangan\n\n"
            "Gunakan format:\n"
            "> [!contoh]\n"
            "> **Judul Contoh**\n"
            "> Penjelasan langkah demi langkah...\n\n"
            "Setiap contoh harus JELAS, KONKRET, dan bisa diikuti langkah demi langkah.\n\n"
            "---\n\n"
            "### 5b. Coba Sendiri / Latihan Terpandu (SANGAT DISARANKAN)\n"
            "Setelah contoh, ajak siswa MENCARI TAHU dulu sebelum melihat jawaban.\n"
            "Tulis latihan pendek dengan petunjuk, LALU pisah dari jawaban dengan '---' dan tulis\n"
            "'> **Kunci Jawaban / Pembahasan:**' di bawahnya. Struktur:\n"
            "> [!coba]\n"
            "> **Coba Sendiri:** [instruksi/soal singkat]\n"
            "> [petunjuk kecil opsional]\n"
            "> ---\n"
            "> **Pembahasan:** [penjelasan singkat langkah demi langkah]\n\n"
            "Beri kesempatan siswa mencoba sendiri sebelum membaca pembahasan — ini yang membangun pemahaman aktif.\n\n"
            "---\n\n"
            "### 6. Penerapan di Dunia Nyata (OPSIONAL)\n"
            "Tunjukkan bagaimana konsep ini digunakan dalam kehidupan nyata.\n"
            "Hubungkan teori dengan situasi praktis:\n"
            "- Profesi apa yang menggunakan ini?\n"
            "- Di mana kita menemui ini sehari-hari?\n"
            "- Masalah nyata apa yang bisa dipecahkan?\n\n"
            "---\n\n"
            "### 7. Kesalahan Umum & Miskonsepsi (OPSIONAL)\n"
            "Gunakan:\n"
            "> [!perhatian]\n"
            "> **Hati-hati!** Banyak yang salah paham tentang ini...\n"
            "> ❌ [Miskonsepsi] → ✅ [Pemahaman benar]\n\n"
            "Ini sangat membantu siswa menghindari jebakan umum.\n\n"
            "---\n\n"
            "### 7b. Hubungkan Antar Konsep (Connect the Dots, OPSIONAL)\n"
            "Bantu siswa melihat bagaimana konsep ini berhubungan dengan konsep lain dalam topik\nyang sama atau materi sebelumnya. Contoh pertanyaan yang dijawab:\n"
            "- Konsep apa yang menjadi prasyarat dari ini?\n"
            "- Materi berikutnya mana yang akan memakai konsep ini?\n"
            "- Bagaimana konsep ini saling terkait dengan konsep serupa?\n\n"
            "Gunakan callout:\n"
            "> [!hubung]\n"
            "> **Kaitannya dengan konsep lain:** ...\n\n"
            "Ini membuat siswa tidak belajar dalam kotak terpisah, tapi melihat peta besar.\n\n"
            "---\n\n"
            "### 8. Ringkasan & Poin Kunci (WAJIB)\n"
            "Rangkum ide-ide paling penting dalam poin-poin singkat.\n"
            "Gunakan:\n"
            "> [!ingat]\n"
            "> **Yang Perlu Kamu Ingat:**\n"
            "> - Poin 1\n"
            "> - Poin 2\n"
            "> - Poin 3\n\n"
            "---\n\n"
            "### 9. Latihan & Self-Check (WAJIB)\n"
            "Berikan 2-3 soal dengan tingkat kesulitan berbeda:\n"
            "- 1 soal pemahaman dasar\n"
            "- 1 soal penerapan/analisis\n"
            "- 1 soal tantangan (opsional)\n\n"
            "Gunakan:\n"
            "> [!quiz]\n"
            "> **Soal 1:** [pertanyaan]\n"
            "> **Soal 2:** [pertanyaan]\n\n"
            "Tulis '---' lalu '**Jawaban:**' diikuti penjelasan singkat untuk setiap soal.\n"
            "Fokus pada soal pemahaman dan penerapan, BUKAN hafalan.\n\n"
            "---\n\n"
            "### 10. Penutup (WAJIB)\n"
            "Satu kalimat motivasi yang menguatkan. Contoh:\n"
            "\"Setiap ahli pernah jadi pemula. Yang terpenting adalah langkah kecilmu hari ini! 💪\"\n\n"
            "=================================================================\n"
            " GAYA PENULISAN\n"
            "=================================================================\n\n"
            "- Gunakan bahasa Indonesia yang SANTAI tapi TETAP EDUKATIF\n"
            "- Sapa siswa langsung: 'Kamu', 'Kamu tahu tidak?', 'Coba bayangkan...'\n"
            "- Gunakan analogi sehari-hari yang RELATIF dengan kehidupan siswa\n"
            "- Gunakan bold **hanya** untuk istilah teknis penting\n"
            "- Gunakan emoji secara SPARING (1-2 per section, jangan berlebihan)\n"
            "- Hindari paragraf yang terlalu panjang — maksimal 3-4 kalimat per paragraf\n"
            "- Gunakan heading (###) untuk memecah konteks\n"
            "- Buat pembaca merasa: 'oh gitu toh, ternyata gampang ya!'\n\n"
            "=================================================================\n"
            " VIDEO YOUTUBE\n"
            "=================================================================\n\n"
            "Sertakan 1-3 video YouTube yang PALING RELEVAN dan sudah pasti benar.\n"
            "ATURAN VIDEO (SANGAT PENTING):\n"
            "- URL harus format video sungguhan: https://www.youtube.com/watch?v=VIDEO_ID\n"
            "  ATAU https://youtu.be/VIDEO_ID (VIDEO_ID 11 karakter).\n"
            "- DILARANG memakai search URL (https://www.youtube.com/results?...). Jika tidak yakin\n"
            "  dengan ID video yang benar, JANGAN dibuat-buat — kembalikan daftar kosong: \"videos\": [].\n"
            "- Jangan memakai video yang judulnya tidak benar-benar membahas topik ini.\n"
            "- Lebih baik videos kosong daripada video yang menyesatkan.\n\n"
            "=================================================================\n"
            " ATURAN FORMAT MARKDOWN (WAJIB PATUH)\n"
            "=================================================================\n\n"
            "- JANGAN PERNAH menulis karakter escape seperti \\* atau \\** atau \\[. Cukup tulis **bold**\n"
            "  dan *italic* biasa — jangan pakai backslash di depan karakter markdown.\n"
            "- Hanya gunakan sintaks markdown yang didukung: ## / ### heading, **bold**, *italic*,\n"
            "  - list, 1. list, ```code block```, `kode inline`, tabel, dan callout (>[!tipe]).\n"
            "- Setiap callout yang ditulis harus dalam format blok kutipan:\n"
            "  > [!tip]\n"
            "  > isi callout...\n"
            "- DILARANG menampilkan sintaks mentah ke siswa. Hasil akhir harus bersih dan dapat dirender sempurna.\n\n"
            "Sesuaikan kedalaman materi dengan jenjang: "
            f"{grade_level or 'sma'}."
        )

        lesson_sys_prompt = (
            "Kamu adalah Buddio, mentor belajar AI yang membimbing siswa dengan sabar dan personal. "
            "Gaya bahasmu seperti guru privat yang pintar, asik, dan bisa menjelaskan hal rumit "
            "dengan analogi sederhana yang bikin siswa bilang 'oh gitu toh!'.\n\n"
            "Kamu TIDAK seperti Wikipedia atau buku teks. Kamu seperti kakak kelas yang sudah "
            "paham betul topik ini dan mau bantu adik kelas memahaminya.\n\n"
            "Prinsip utamamu:\n"
            "- Jelaskan yang sederhana dulu, baru masuk ke yang kompleks\n"
            "- Selalu hubungkan konsep abstrak dengan contoh nyata\n"
            "- Siswa harus merasa 'mengerti' setiap langkah, bukan sekadar 'membaca'\n"
            "- Bahasa Indonesia yang natural, santai, tapi tetap tepat secara akademis\n"
            "- Gunakan progressive learning: kenalan → fondasi → konsep → contoh → penerapan → latihan"
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
