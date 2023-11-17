from telegram import Update
from telegram.ext import CallbackContext

from chat_protector.handlers.services.message_senders import send_message
from chat_protector.templates import render_template


async def help_(update: Update, context: CallbackContext):
    await send_message(update, f'{render_template("help.j2")}')
