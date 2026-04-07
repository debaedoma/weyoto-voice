# App settings
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)
BASE_DIR = Path(__file__).resolve().parent


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    AUDIO_STORAGE_DIR = os.getenv(
        "AUDIO_STORAGE_DIR",
        str(BASE_DIR / "instance" / "audio"),
    )
