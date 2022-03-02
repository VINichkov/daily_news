import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
from models import Article
from log import logger


def _convert_to_article(tag: Tag) -> Article:
    return Article(
        url=tag.guid.text,
        tags=f"#ria #{tag.category.text.replace(' ', '_')}".lower(),
        time=datetime.strptime(tag.pubdate.text, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None),
        source='Ria',
        title=tag.find('title').text,
        text=tag.find('description').text
    )


class Ria:
    TimeDelta = timedelta(minutes=10)

    def __init__(self, last_time: str) -> None:
        self.__url = 'https://ria.ru/export/rss2/archive/index.xml'
        self.source = 'Ria'
        self.last_time = last_time


    def _get_news_feeds(self) -> list:
        def filter_fun(x):
            logger.debug(F"Ria filt: {x.time}>{self.last_time}  = {x.time.timestamp() > self.last_time.timestamp()}")
            return x.time.timestamp() > self.last_time.timestamp()
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elems = soup.find_all('item')
        all_articles = list(map(_convert_to_article, elems))
        filtered_articles = list(filter(filter_fun, all_articles))
        return list(map(self._get_picture, filtered_articles))

    def _get_picture(self, article: Article)->Article:
        response = requests.get(article.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img = soup.find(class_='media').find('img')
        if img is None:
            article.picture_url = 'https://avatars.mds.yandex.net/get-zen-logos/1597769/pub_5a0c48cf168a91bf9190bbef_5cc2dd3224176a00ae4fe496/xxh'
        else:
            article.picture_url = img.get('src')
        return article


    def call(self) -> list:
        res = self._get_news_feeds()
        logger.info(F"Ria: articles of number {len(res)}")
        return res