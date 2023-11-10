import re

from telegram import Update
from telegram.ext import CallbackContext

from chat_protector.services.file_downloader import download
from chat_protector.services.url_analysis import url_analysis_output
from chat_protector.config import TELEGRAM_CHAT_ID


async def target_finder(update: Update, context: CallbackContext):

    target_chat_id = int(TELEGRAM_CHAT_ID)
    message_chat_id = update.message.chat.id

    if message_chat_id == target_chat_id:
        try:
            file = update.message.document.file_id
        except:
            try:
                file = update.message.photo[0].file_id
            except:
                file = update.message.video.file_id

        message_text = update.message.text or False

        if message_text:
            urls = re.findall(r'https?://[^\s,]+', message_text)

            if urls:
                await url_analysis_output(update, urls)

        if file:
            await download(file)
