from telegram import Update


async def reply_to_message(update: Update, text: str):
    await update.message.reply_text(text, reply_to_message_id=update.message.message_id)


async def send_message(update: Update, text: str):
    await update.message.reply_text(text)
