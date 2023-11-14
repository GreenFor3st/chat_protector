from chat_protector.config import (TELEGRAM_BOT_TOKEN,
                                   FOLDER_FOR_FILES)

from telegram import (Bot, File)


async def download(file_id: str, file_name: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        file = await bot.get_file(file_id)

        await File.download_to_drive(file, custom_path=f'{FOLDER_FOR_FILES}{file_name}')
    except Exception as e:
        print(f"Error downloading file: {e}")
