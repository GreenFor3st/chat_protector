from time import sleep
import requests
from telegram import Update
from vt import Client

from .message_sender import reply_to_message
from chat_protector.config import VIRUS_TOTAL_APIKEY


def ping_urls(url):
    response = requests.get(url)
    return response.status_code == 200


async def url_analysis(url) -> dict or None:
    client = Client(VIRUS_TOTAL_APIKEY)
    status_link = {}
    try:
        url_id = await client.scan_url_async(url)
        response = await client.get_object_async("/analyses/{}".format(url_id.id))

    except Exception as e:
        print(e)
        await client.close_async()
        return

    status_link[f'{url}'] = {'malicious': response.stats["malicious"],
                             'suspicious': response.stats["suspicious"]}

    await client.close_async()

    return status_link


async def url_analysis_output(update: Update, urls):
    for url in urls:
        try:
            if ping_urls(url):

                result = await url_analysis(url)
                for link, values in result.items():
                    await reply_to_message(update,
                                           f'malicious: {values["malicious"]}\n'
                                           f'suspicious: {values["suspicious"]}')
            else:
                await reply_to_message(update, 'It is impossible to connect to the host because it does not found')

        except requests.exceptions.RequestException:
            await reply_to_message(update, 'It is impossible to connect to the host because it does not exist')

        except Exception as e:
            await reply_to_message(update, f'{e}')
        sleep(15)
