import yaml
import asyncio

from telegram.ext import ExtBot

from services import ServiceStateTrovo, ServiceStateTwitch


def get_config() -> dict:
    """
    загрузка конфига
    return: словарь с параметрами
    """
    with open('config.yml', 'r') as file:
        config_dict = yaml.safe_load(file)
    return config_dict


async def main():
    config = get_config()

    TOKEN = config.get('TOKEN')
    CHANNEL_ID = config.get('CHANNEL_ID')
    TROVO_TOKEN = config.get('TROVO_TOKEN')
    trovo_url = config.get('trovo_url')

    TWITCH_TOKEN = config.get('TWITCH_TOKEN')
    TWITCH_SECRET = config.get('TWITCH_SECRET')
    twitch_url = config.get('twitch_url')
    """Start the bot."""
    bot = ExtBot(TOKEN)

    service_trovo = ServiceStateTrovo(
        url=trovo_url,
        token=TROVO_TOKEN
    )

    with open('twitch.txt', 'w') as f:
        f.write('enabled')
    with open('trovo.txt', 'w') as f:
        f.write('enabled')

    service_twitch = ServiceStateTwitch(
        url=twitch_url,
        token=TWITCH_TOKEN,
        secret=TWITCH_SECRET
    )
    await asyncio.gather(
        service_twitch.request(
            bot=bot,
            channel_id=CHANNEL_ID,
        ),
        service_trovo.request(
            bot=bot,
            channel_id=CHANNEL_ID
        )
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError:
        pass
