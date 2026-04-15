# App settings
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)
BASE_DIR = Path(__file__).resolve().parent


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Africa/Lagos")
    OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
    WEEKLY_WORD_LIMIT = int(os.getenv("WEEKLY_WORD_LIMIT", "500"))
    MAX_WORDS_PER_GENERATION = int(os.getenv("MAX_WORDS_PER_GENERATION", "120"))
    MAX_FINE_TUNE_WORDS = int(os.getenv("MAX_FINE_TUNE_WORDS", "25"))
    DEFAULT_TTS_INSTRUCTION = os.getenv(
        "DEFAULT_TTS_INSTRUCTION",
        "Match the tone of the text.",
    )
    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "instance" / "weyoto_voice.db"),
    )
    AUDIO_STORAGE_DIR = os.getenv(
        "AUDIO_STORAGE_DIR",
        str(BASE_DIR / "instance" / "audio"),
    )
