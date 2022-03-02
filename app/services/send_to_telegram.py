import os
from PIL import Image
import requests

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
            try:
                self.tm.send_news(
                    picture=self.validate_image(article_msg.picture_url),
                    text=article_msg.text_msg(),
                    url=article_msg.url)
            except Exception:
                logger.error('Ошибка отправки:\n', traceback.format_exc())
            self.rep.sent(article_bd)

    def validate_image(self, img: str) -> any:
        im = Image.open(requests.get(img, stream=True).raw)
        (width, height) = im.size
        if width > 1200:
            return im.resize([1200, 800])
        else:
            return img
