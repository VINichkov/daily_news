import telebot
from telebot import types
from urllib.parse import urlparse

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Telegram(metaclass=Singleton):

    def __init__(self, token: str, channel_id: str):
        print('Telegram: init module')
        try:
            if self.bot is None:
                self.bot = telebot.TeleBot(token)
                self.channel_id = channel_id
        except AttributeError:
            self.bot = telebot.TeleBot(token)
            self.channel_id = channel_id

    def send_message(self, text: str) -> None:
        print('Telegram: send a message')
        self.bot.send_message(
            chat_id=self.channel_id,
            text=text,
            parse_mode='HTML',
        )

    def send_news(self, picture: any, text: str, url: str) -> None:
        print('Telegram: send a message')
        self.bot.send_photo(
            chat_id=self.channel_id,
            photo=picture,
            caption=text,
            parse_mode='HTML',
            #reply_markup=self._button_creator(url)
        )
    def utm_url(self, url: str) -> str:
        parse_url = urlparse(url)
        new_url = parse_url._replace(
            query='utm_source=telegram&utm_medium=social_cpc&utm_campaign=daily_news_ru'
        )
        return new_url.geturl()


    def _button_creator(self, url: str) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Подробнее", url=self.utm_url(url))
        markup.add(button)
        return markup
