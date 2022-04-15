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
            interval: int = 60,
            **kwargs
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
        payload = {
            'username': 'ZiGi_hate',
        }
        while True:
            response = requests.post(self.url, headers=headers, data=json.dumps(payload))
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
        payload = {
            'username': 'ZiGi_hate',
        }
        while True:
            with open('trovo.txt', 'r') as f:
                status = f.read()
            response = requests.post(self.url, headers=headers, data=json.dumps(payload))
            data = response.json()
            if data.get('is_live') and status == 'enabled':
                text = self.get_message_text(data=data)
                bot.send_message(chat_id=channel_id, text=text)
                with open('trovo.txt', 'w') as f:
                    f.write('disabled')
                self.interval = 600
            elif not data.get('is_live') and status == 'disabled':
                with open('trovo.txt', 'w') as f:
                    f.write('enabled')
                self.interval = 60
            await asyncio.sleep(self.interval)

    def get_message_text(self, *args, **kwargs) -> str:
        """
        полулачеам текст для отправляемого сообщения
        :return:
        """
        data = kwargs.pop('data')
        url = data.get('channel_url')
        return f'Старт на {self.name} {url}'


class ServiceStateTwitch(ServiceStateBase):
    """
    Сервис для твича
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('secret'):
            self.secret = kwargs.pop('secret')
        self.name: str = 'twitch'

    def get_token(self) -> str:
        """
        получаем токен для твича
        :return:
        """
        headers = {
            'Client-ID': self.token,
            'client_secret': self.secret,
        }
        payload = {
            'grant_type': 'client_credentials',
            'client_secret': self.secret,
            'client_id': self.token
        }
        url = 'https://id.twitch.tv/oauth2/token'
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()
        if response.status_code == 200:
            return data['access_token']
        else:
            return ''

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
        token = self.get_token()
        headers = {
            'Client-ID': self.token,
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }
        params = {
            'user_login': 'zigi_hate',
        }
        while True:
            response = requests.get(self.url, headers=headers, params=params)
            data = response.json()
            with open('twitch.txt', 'r') as f:
                status = f.read()
            if data.get('data') \
                    and len(data['data']) == 1 \
                    and data['data'][0]['type'] == 'live' \
                    and status == 'enabled':
                text = self.get_message_text(data=data)
                bot.send_message(chat_id=channel_id, text=text)
                with open('twitch.txt', 'w') as f:
                    f.write('disabled')
                self.enabled = False
                self.interval = 600
            elif not data.get('data') and status == 'disabled':
                with open('twitch.txt', 'w') as f:
                    f.write('enabled')
                self.enabled = True
                self.interval = 60
            await asyncio.sleep(self.interval)

    def get_message_text(self, *args, **kwargs) -> str:
        """
        полулачеам текст для отправляемого сообщения
        :return:
        """
        data = kwargs.pop('data')
        url = data.get('channel_url')
        return f'Старт на {self.name} https://www.twitch.tv/zigi_hate'
