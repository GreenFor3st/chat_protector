import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from chat_protector.config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    VIRUS_TOTAL_APIKEY,
    stream_mode
)

from chat_protector import handlers
from chat_protector.handlers.services.errors import error

COMMAND_HANDLERS = {
    "help": handlers.help_,
}


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not VIRUS_TOTAL_APIKEY:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID or VIRUS_TOTAL_APIKEY env variables "
        "wasn't implemented in .env (all should be initialized)."
    )

if __name__ == "__main__":

    print('Bot is runing')

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        app.add_handler(CommandHandler(command_name, command_handler))

    if stream_mode:
        app.add_handler(MessageHandler(filters.ALL, handlers.scan))
    else:
        app.add_handler(CommandHandler('scan', handlers.scan))

    # errors
    app.add_error_handler(error)

    # start
    app.run_polling(poll_interval=1)
