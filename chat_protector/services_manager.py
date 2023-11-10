import re

from telegram import Update
from telegram.ext import CallbackContext

from chat_protector.services.file_downloader import download
from chat_protector.services.message_sender import reply_to_message

from chat_protector.services.url_analysis import url_analysis_processor
from chat_protector.services.file_analysis import file_analysis_processor

from chat_protector.config import TELEGRAM_CHAT_ID, FOLDER_FOR_FILES


async def target_finder(update: Update, context: CallbackContext):

    file = None
    file_name = None

    message_text = update.message.text

    target_chat_id = int(TELEGRAM_CHAT_ID)
    message_chat_id = update.message.chat.id

    if message_chat_id == target_chat_id:
        try:
            if update.message.document:
                file = update.message.document.file_id
                file_name = update.message.document.file_name
            elif update.message.photo:
                file = update.message.photo[0].file_id
                file_name = update.message.photo[0].api_kwargs
            elif update.message.video:
                file = update.message.video.file_id
        except Exception as e:
            print(f"Error getting file_id: {e}")

        if message_text:
            urls = re.findall(r'https?://[^\s,]+', message_text)

            if urls:
                await reply_to_message(update, 'Processing')
                await url_analysis_processor(update, urls)
                await reply_to_message(update, 'Processing complete')

        if file:
            await reply_to_message(update, 'Processing')
            await download(file, file_name)
            await file_analysis_processor(update, FOLDER_FOR_FILES)
            await reply_to_message(update, 'Processing complete')
