import asyncio

import requests

from telegram.ext import ExtBot


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
    ):
        while True:
            response = requests.get(
                self.url,
                headers={
                    'Accept': 'application/json',
                    'Client-ID': 'здесь будет токен приложения trovo'
                },
                data={
                    'username': 'ZiGi_hate'  # хотя, лучше это параметром
                    # передавать
                }
            )
            data = response.json()
            if data.get('is_live') and self.enabled:
                text = self.get_message_text()
                bot.send_message(chat_id=channel_id, text=text)
                self.enabled = False
                self.interval = 3600
            await asyncio.sleep(self.interval)

    def get_message_text(self) -> str:
        """
        полулачеам текст для отправляемого сообщения
        :return:
        """
        return self.url


class ServiceStateTrovo(ServiceStateBase):
    """
    сервис для trovo
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name: str = 'trovo'

    def get_message_text(self) -> str:
        """
        полулачеам текст для отправляемого сообщения
        :return:
        """
        return f'Старт на trovo {self.url}'
