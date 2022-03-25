import asyncio

import requests

from telegram.ext import ExtBot

import json


class ServiceStateBase:
    """
    базовый класс для сервиса
    """

    def __init__(
            self,
            url: str,
            token: str,
            name: str = '',
            interval: int = 60
    ):
        self.enabled: bool = True
        self.name = name
        self.interval = interval
        self.url = url
        self.token = token

    async def request(
            self,
            bot: ExtBot,
            channel_id: str
    ) -> None:
        """
        запрос к сервиусу
        :param bot: tg-bot
        :param channel_id: id чата
        """
        headers = {
            'Client-ID': self.token,
            'Accept': 'application/json'
        }
        data = {
            'username': 'ZiGi_hate',
        }
        while True:
            response = requests.post(self.url, headers=headers, data=json.dumps(data))
            data = response.json()
            if data.get('is_live') and self.enabled:
                text = self.get_message_text(data=data)
                bot.send_message(chat_id=channel_id, text=text)
                self.enabled = False
                self.interval = 600
            else:
                self.enabled = True
                self.interval = 60
            await asyncio.sleep(self.interval)

    def get_message_text(self, *args, **kwargs) -> str:
        """
        полулачеам текст для отправляемого сообщения
        :return:
        """
        return ''


class ServiceStateTrovo(ServiceStateBase):
    """
    сервис для trovo
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name: str = 'trovo'

    def get_message_text(self, *args, **kwargs) -> str:
        """
        полулачеам текст для отправляемого сообщения
        :return:
        """
        data = kwargs.pop('data')
        url = data.get('channel_url')
        return f'Старт на {self.name} {url}'
