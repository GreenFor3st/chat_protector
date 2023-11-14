import re

from telegram import Update
from telegram.ext import CallbackContext

from chat_protector.handlers.services.threat_processor import process_and_report_threats


from chat_protector.config import TELEGRAM_CHAT_ID, stream_mode


async def scan(update: Update, context: CallbackContext):

    file_id = None
    file_name = None

    if stream_mode:
        message_text = update.message.text
    else:
        message_text = update.message.reply_to_message.text

    target_chat_id = int(TELEGRAM_CHAT_ID)
    message_chat_id = update.message.chat.id

    if message_chat_id == target_chat_id:
        try:
            if stream_mode:
                document = update.message.document
                photo = update.message.photo
                video = update.message.video
                if document:
                    file_id = document.file_id
                    file_name = document.file_name
                elif photo:
                    file_id = photo[0].file_id
                    file_name = photo[0].file_size
                elif video:
                    file_id = video.file_id
                    file_name = video.file_name
            else:
                document = update.message.reply_to_message.document
                photo = update.message.reply_to_message.photo
                video = update.message.reply_to_message.video
                if document:
                    file_id = document.file_id
                    file_name = document.file_name
                elif photo:
                    file_id = photo[0].file_id
                    file_name = photo[0].file_size
                elif video:
                    file_id = video.file_id
                    file_name = video.file_name
        except Exception as e:
            print(f"Error getting file_id: {e}")

        if message_text:
            urls = re.findall(r'https?://[^\s,]+', message_text)
            if urls:
                await process_and_report_threats(update, urls=urls)

        if file_id:
            await process_and_report_threats(update, file_id=file_id, file_name=file_name)
