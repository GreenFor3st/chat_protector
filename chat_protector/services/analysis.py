import requests
from vt import Client

from chat_protector.config import VIRUS_TOTAL_APIKEY

from chat_protector.services.exceptions import ApiError


async def file_analysis(file_path) -> dict or None:
    client = Client(VIRUS_TOTAL_APIKEY)
    status_file = {}
    with open(file_path, "rb") as f:
        try:
            file_id = await client.scan_file_async(f)
            response = await client.get_object_async("/analyses/{}".format(file_id.id))
        except Exception:
            await client.close_async()
            raise ApiError

        if response.stats['suspicious'] or response.stats['malicious'] > 0:
            status_file[f'{file_path}'] = {'suspicious': response.stats['suspicious'],
                                           'malicious': response.stats['malicious']}
            await client.close_async()
            return status_file

    await client.close_async()
    return


async def url_analysis(url) -> dict or None:
    client = Client(VIRUS_TOTAL_APIKEY)
    status_link = {}
    try:
        url_id = await client.scan_url_async(url)
        response = await client.get_object_async("/analyses/{}".format(url_id.id))

    except Exception as e:
        await client.close_async()
        raise ApiError

    if response.stats["malicious"] or response.stats["suspicious"] > 0:
        status_link[f'{url}'] = {'malicious': response.stats["malicious"],
                                 'suspicious': response.stats["suspicious"]}
        await client.close_async()
        return status_link

    await client.close_async()
    return


def ping_urls(url):
    response = requests.get(url)
    return response.status_code == 200
