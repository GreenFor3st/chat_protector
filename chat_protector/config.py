import os
from pathlib import Path


VIRUS_TOTAL_APIKEY = os.getenv("VIRUS_TOTAL_APIKEY", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", ""))

BASE_DIR = Path(__file__).resolve().parent
