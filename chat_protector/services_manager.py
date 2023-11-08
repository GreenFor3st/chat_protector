import re

from telegram import Update
from telegram.ext import CallbackContext

from chat_protector.services.url_analysis import url_analysis_output
from chat_protector.config import TELEGRAM_CHAT_ID


async def target_finder(update: Update, context: CallbackContext):

    target_chat_id = int(TELEGRAM_CHAT_ID)
    message_chat_id = update.message.chat.id

    if message_chat_id == target_chat_id:

        message_text = update.message.text.lower()
        urls = re.findall(r'https?://[^\s,]+', message_text)

        if urls:
            await url_analysis_output(update, urls)

        media = update.message.document or update.message.photo or update.message.video or False

        if media:
            print(media)
