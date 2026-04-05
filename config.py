# App settings
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")