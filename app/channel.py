import telebot


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

