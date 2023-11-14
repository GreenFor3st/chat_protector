import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

VIRUS_TOTAL_APIKEY = os.getenv("VIRUS_TOTAL_APIKEY", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

BASE_DIR = Path(__file__).resolve().parent

FOLDER_FOR_FILES = 'handlers/services/download/'

stream_mode = True
