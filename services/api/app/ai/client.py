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
            f"Buatkan materi pembelajaran lengkap untuk langkah belajar \"{step_title}\" "
            f"dalam topik \"{topic_title}\" untuk jenjang {grade_level or 'sma'}.\n\n"
            f"Deskripsi langkah: {step_description or '-'}\n\n"
            "Kembalikan JSON dengan format:\n"
            "{\n"
            '  "content": "...",\n'
            '  "videos": [\n'
            '    {"title": "Judul Video", "url": "https://www.youtube.com/watch?v=VIDEO_ID", "description": "Deskripsi singkat"}\n'
            "  ]\n"
            "}\n\n"
            "UNTUK CONTENT (materi inti):\n"
            "Tulis materi pembelajaran yang KAYA, TERSTRUKTUR, dan MENARIK dalam Bahasa Indonesia. "
            "Gunakan markdown dengan format:\n"
            "## Penjelasan Konsep\n"
            "Jelaskan konsep secara mendalam, bertahap, dan mudah dipahami.\n\n"
            "## Poin-Poin Penting\n"
            "Bullet points berisi istilah penting dan definisinya.\n\n"
            "## Contoh\n"
            "Berikan 2-3 contoh konkret dengan penjelasan langkah demi langkah.\n\n"
            "## Contoh Soal\n"
            "Buat 2-3 contoh soal beserta pembahasan lengkap.\n\n"
            "## Ringkasan Materi\n"
            "Rangkum poin-poin utama dalam beberapa kalimat.\n\n"
            "UNTUK VIDEOS:\n"
            "Cari dan masukkan 3-4 URL video YouTube yang RELEVAN dengan topik ini. "
            "Gunakan format URL: https://www.youtube.com/watch?v=VIDEO_ID\n"
            "Jika tidak yakin dengan URL spesifik, gunakan URL pencarian YouTube: "
            "https://www.youtube.com/results?search_query=kata+kunci+pencarian\n"
            "Pastikan setiap video memiliki judul dan deskripsi singkat.\n\n"
            "Sesuaikan kedalaman materi dengan jenjang pendidikan: "
            f"{grade_level or 'sma'}."
        )

        lesson_sys_prompt = (
            "Kamu adalah Buddio, mentor belajar AI yang ahli menyusun materi pembelajaran "
            "yang terstruktur, menarik, dan mudah dipahami dalam Bahasa Indonesia."
        )

        try:
            data = _generate_json(prompt, max_tokens=4096, system_instruction=lesson_sys_prompt)
            data.setdefault("content", "")
            data.setdefault("videos", [])
            return data, "gemini"
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini lesson failed, falling back to mock: %s", exc)
            return mock_ai.mock_lesson(step_title, topic_title), "mock"


buddio_ai = BuddioAI()
