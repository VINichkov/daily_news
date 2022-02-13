import os
import config
from log import logger
from channel import Telegram
from repositories import ArticleRep
from data_models import ArticleMsg


class SendToTelegram:

    def __init__(self):
        self.tm = Telegram(
            token=os.getenv('AUTH_TOKEN'),
            channel_id=os.getenv('CHANNEL_ID')
        )
        self.rep = ArticleRep(config.DB())

    def call(self):
        article_bd = self.rep.get_first_item()
        if article_bd is not None:
            article_msg = ArticleMsg()
            article_msg.from_article_model(article_bd)
            self.tm.send_message(article_msg.text_msg())
            self.rep.sent(article_bd)