import yaml
import asyncio

from telegram.ext import ExtBot

from services import ServiceStateTrovo


def stop():
    task.cancel()


def get_config() -> dict:
    """
    загрузка конфига
    return: словарь с параметрами
    """
    with open('config.yml', 'r') as file:
        config_dict = yaml.safe_load(file)
    return config_dict


if __name__ == '__main__':
    config = get_config()

    TOKEN = config.get('TOKEN')
    CHANNEL_ID = config.get('CHANNEL_ID')
    url = config.get('trovo_url')
    """Start the bot."""
    bot = ExtBot(TOKEN)

    service = ServiceStateTrovo(
        url=url,
        token=''
    )

    loop = asyncio.get_event_loop()
    task = loop.create_task(service.request(
        bot=bot,
        channel_id=CHANNEL_ID
    ))
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass
