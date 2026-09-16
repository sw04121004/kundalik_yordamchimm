"""
AI provider integration for Qulay's AI Assistant.

Configuration comes entirely from environment variables (see backend/.env.example).
No API key is ever hard-coded. If no key is configured, the app does not crash —
it returns a clear, honest message explaining that the AI is not connected yet,
instead of pretending to produce a real AI answer.

Supported providers (set AI_PROVIDER in .env):
  - "openai"    -> any OpenAI-compatible /chat/completions endpoint
                   (OpenAI itself, or compatible gateways/proxies)
  - "anthropic" -> Anthropic's /v1/messages endpoint
"""
import os

import requests

AI_PROVIDER = os.environ.get("AI_PROVIDER", "openai").strip().lower()
AI_API_KEY = os.environ.get("AI_API_KEY", "").strip()
AI_MODEL = os.environ.get("AI_MODEL", "").strip()

_DEFAULT_BASE_URLS = {
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com/v1",
}
_DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
}

AI_API_BASE_URL = os.environ.get("AI_API_BASE_URL", "").strip() or _DEFAULT_BASE_URLS.get(
    AI_PROVIDER, _DEFAULT_BASE_URLS["openai"]
)
if not AI_MODEL:
    AI_MODEL = _DEFAULT_MODELS.get(AI_PROVIDER, _DEFAULT_MODELS["openai"])

REQUEST_TIMEOUT = 30


def _get_config():
    """Read AI configuration fresh from environment each call.
    
    This lets the server pick up .env changes without a full restart
    (in dev mode with Django's auto-reloader the module re-imports, but
    in production or when the key is set after startup this is safer).
    """
    provider = os.environ.get("AI_PROVIDER", "openai").strip().lower()
    key = os.environ.get("AI_API_KEY", "").strip()
    model = os.environ.get("AI_MODEL", "").strip()
    base_url = os.environ.get("AI_API_BASE_URL", "").strip()

    if not base_url:
        base_url = _DEFAULT_BASE_URLS.get(provider, _DEFAULT_BASE_URLS["openai"])
    if not model:
        model = _DEFAULT_MODELS.get(provider, _DEFAULT_MODELS["openai"])

    return provider, key, model, base_url



PURPOSE_SYSTEM_PROMPTS = {
    "general": "Sen umumiy yordamchisan. Savollarga aniq va qisqa javob ber.",
    "kitchen": "Sen oshxona va pazandalik bo'yicha yordamchisan. Retseptlar, ovqat tayyorlash, masalliqlar haqida maslahat berasan.",
    "study": "Sen o'quvchilar va talabalar uchun yordamchisan. Mavzularni tushuntirasan, lug'at va testlar tuzishda yordam berasan.",
    "document": "Sen hujjatlar bilan ishlash bo'yicha yordamchisan. Xatlarni yozish, xulosalash, matnlarni tahrirlash vazifalarini bajarasan.",
    "translation": "Sen aniq va tabiiy tarjimon yordamchisan. O'zbek, rus, ingliz tillarida erkin tarjima qilasan.",
    "home": "Sen uy yumushlari va ro'zg'or maslahatchisisan. Uyni toza saqlash, tejamkorlik va uy rejalari haqida yordam berasan.",
    "finance": "Sen shaxsiy moliya bo'yicha maslahatchisan. Xarajatlarni tejash, byudjet tuzish va hisoblashda yordam berasan.",
    "programming": "Sen tajribali dasturchisan. Kod yozish, xatolarni topish va algoritmlarni tushuntirishda yordam berasan.",
    "ideas": "Sen ijodkor yordamchisan. Yangi g'oyalar o'ylab topish, loyiha rejalarini tuzishda ko'maklashasan.",
    "cv": "Sen karyera maslahatchisisan. CV (rezume), motivatsion xat va ishga kirish suhbatlarida yordam berasan."
}

DEFAULT_PROMPT_KEY = "general"

# Every system prompt also gets this shared instruction so the assistant copes
# gracefully with real, messy Uzbek input (typos, slang, mixed languages).
_INPUT_TOLERANCE_NOTE = (
    " Foydalanuvchilar ko'pincha imlo xatolari bilan, so'zlashuv uslubida, "
    "o'zbek/rus/ingliz tillarini aralashtirib yoki juda qisqa yozishadi "
    "(masalan: 'kodim ishlameyapti', 'shu mavzuni oddiyroq tushuntir'). Bunday "
    "xabarlarni ham to'g'ri tushunib, tabiiy va do'stona ohangda javob ber. "
    "Grammatikasi mukammal bo'lishini talab qilma."
)


class AIUnavailableError(Exception):
    """Raised when the configured AI provider could not be reached."""


def is_configured() -> bool:
    _, key, _, _ = _get_config()
    return bool(key)


def get_not_configured_message() -> str:
    return (
        "🤖 AI yordamchi hozircha ulanmagan.\n\n"
        "Administrator backend/.env faylida AI_API_KEY (va xohlasa AI_PROVIDER, "
        "AI_MODEL) qiymatlarini to'ldirishi kerak. Bu sozlangandan so'ng AI "
        "javoblari avtomatik ravishda ishga tushadi — hozircha bu haqiqiy AI "
        "javobi emas, shunchaki tizim xabari."
    )


def _build_history_with_system(purpose: str, history: list[dict]) -> tuple[str, list[dict]]:
    system_prompt = PURPOSE_SYSTEM_PROMPTS.get(purpose, PURPOSE_SYSTEM_PROMPTS[DEFAULT_PROMPT_KEY])
    system_prompt += _INPUT_TOLERANCE_NOTE
    # keep only the last N turns to keep requests small and fast
    trimmed = history[-20:]
    return system_prompt, trimmed


def generate_reply(purpose: str, history: list[dict]) -> str:
    """
    history: list of {"role": "user"|"assistant", "content": str}, oldest first.
    Returns the assistant's reply text.
    Raises AIUnavailableError if the provider call fails.
    Returns a clearly-labeled fallback message (not a real AI answer) if no
    API key is configured at all.
    """
    provider, key, model, base_url = _get_config()
    if not key:
        return get_not_configured_message()

    system_prompt, messages = _build_history_with_system(purpose, history)

    try:
        if provider == "anthropic":
            return _call_anthropic(system_prompt, messages, key, model, base_url)
        return _call_openai_compatible(system_prompt, messages, key, model, base_url)
    except AIUnavailableError:
        raise
    except Exception as exc:  # network errors, bad JSON, unexpected shape, etc.
        raise AIUnavailableError(str(exc)) from exc


def _call_openai_compatible(system_prompt: str, messages: list[dict], key: str, model: str, base_url: str) -> str:
    url = f"{base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "max_tokens": 800,
        "temperature": 0.6,
    }
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.RequestException as exc:
        if exc.response is not None and exc.response.status_code == 429:
            raise AIUnavailableError("Kiritilgan API kalitida limit tugagan (Rate limit exceeded). Boshqa kalit kiriting yoki kuting.") from exc
        raise AIUnavailableError(f"OpenAI-compatible API xatosi: {exc}") from exc
    except (KeyError, IndexError, ValueError) as exc:
        raise AIUnavailableError(f"AI javobini o'qishda xatolik: {exc}") from exc


def _call_anthropic(system_prompt: str, messages: list[dict], key: str, model: str, base_url: str) -> str:
    url = f"{base_url.rstrip('/')}/messages"
    payload = {
        "model": model,
        "system": system_prompt,
        "max_tokens": 800,
        "messages": messages,
    }
    try:
        response = requests.post(
            url,
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return "".join(block.get("text", "") for block in data.get("content", [])).strip()
    except requests.RequestException as exc:
        raise AIUnavailableError(f"Anthropic API xatosi: {exc}") from exc
    except (KeyError, IndexError, ValueError) as exc:
        raise AIUnavailableError(f"AI javobini o'qishda xatolik: {exc}") from exc

