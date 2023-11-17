from telegram import Update
from telegram import Bot

from chat_protector.config import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN


async def reply_to_message(update: Update, text: str):
    await update.message.reply_text(text, reply_to_message_id=update.message.message_id)


async def send_message(update: Update, text: str):
    await update.message.reply_text(text)
