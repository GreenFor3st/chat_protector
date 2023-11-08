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
    VIRUS_TOTAL_APIKEY
)

from chat_protector.services_manager import target_finder
from chat_protector.services.errors import error


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

    app.add_handler(MessageHandler(filters.ALL, target_finder))
    # app.add_handler(CommandHandler('/start', start))
    # app.add_handler(CommandHandler('/help', help))
    # app.add_handler(CommandHandler('/scan', scan))
    # app.add_handler(CommandHandler('/start_stream_scanning', start_stream_scanning))
    # app.add_handler(CommandHandler('/stop_stream_scanning', stop_stream_scanning))

    # errors
    app.add_error_handler(error)

    # start
    app.run_polling(poll_interval=1)
