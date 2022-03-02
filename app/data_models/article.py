from datetime import datetime
from dataclasses import dataclass
from models import Article


@dataclass
class ArticleMsg:
    url: str = None
    tags: str = None
    picture_url: str = None
    text: str = ''
    title: str = None


    def text_msg(self) -> str:
        if self.text is None:
            self.text = ''
        print('ArticleMsg: An article to text')
        msg = f"{self.tags}\n\n" \
              f"<b>{self.title.strip()}</b>\n\n" \
              f"{self.text[0:400].strip()}\n" \
              f"<b><a href='{self.url}'>Подробнее</a></b>"
        return msg

    def from_article_model(self, art: Article):
        self.url = art.url
        self.tags = art.tags
        self.picture_url = art.picture_url
        self.title = art.title
        self.text = art.text
