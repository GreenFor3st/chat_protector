
from chat_protector.config import TELEGRAM_BOT_TOKEN

import os
import io
import telegram
from telegram import Update, File


async def download(file_id: str):
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        file = await bot.get_file(file_id)
        return await File.download_to_drive(file)
    except Exception as e:
        print(f"Error downloading file: {e}")
