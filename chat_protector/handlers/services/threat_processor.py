import os
import time

import requests
from telegram import Update

from chat_protector.config import FOLDER_FOR_FILES
from chat_protector.handlers.services.file_downloader import download
from chat_protector.handlers.services.message_senders import (reply_to_message, send_message)
from chat_protector import analysis


async def process_and_report_threats(update: Update, file_id=None, file_name=None, urls=None):
    threat_detected = False

    async def process_file(file_path):
        nonlocal threat_detected
        try:
            result = await analysis.file_analysis(file_path)
            if result:
                threat_detected = True
                for file, values in result.items():
                    await reply_to_message(update, f'{file}'
                                                   f'malicious: {values["malicious"]}\n'
                                                   f'suspicious: {values["suspicious"]}')
            if not threat_detected:
                await reply_to_message(update, 'No threats detected')

            os.remove(file_path)
            print(f"File {file_name} removed")
        except Exception as e:
            await reply_to_message(update, f'{e}')

    async def process_url(url):
        nonlocal threat_detected
        try:
            if analysis.ping_urls(url):
                result = await analysis.url_analysis(url)
                if result:
                    threat_detected = True
                    for link, values in result.items():
                        await reply_to_message(update, f'{link}\n'
                                                       f'malicious: {values["malicious"]}\n'
                                                       f'suspicious: {values["suspicious"]}')
                if not threat_detected:
                    await reply_to_message(update, 'No threats detected')
            else:
                await reply_to_message(update, 'It is impossible to connect to the host because it does not found')
        except requests.exceptions.RequestException:
            await reply_to_message(update, 'It is impossible to connect to the host because it does not exist')
        except analysis.ApiError:
            await send_message(update, 'Problems with API operation')

    if file_id:
        await download(file_id, file_name)
        files = os.listdir(FOLDER_FOR_FILES)
        for file_name in files:
            file_path = os.path.join(FOLDER_FOR_FILES, file_name)
            await reply_to_message(update, 'Processing')
            await process_file(file_path)
            await reply_to_message(update, 'Processing complete')
            time.sleep(30)

    if urls:
        for url in urls:
            await reply_to_message(update, 'Processing')
            await process_url(url)
            await reply_to_message(update, 'Processing complete')
            time.sleep(15)
