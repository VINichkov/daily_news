from datetime import datetime
from dataclasses import dataclass
from models import Article


@dataclass
class ArticleMsg:
    url: str = None
    tags: str = None


    def text_msg(self) -> str:
        print('ArticleMsg: An article to text')
        return f"<b>Подробнее по ссылке:</b> {self.url}\n\n{self.tags}"

    def from_article_model(self, art: Article):
        self.url = art.url
        self.tags = art.tags
