import requests
from datetime import datetime
from bs4 import BeautifulSoup
from bs4 import Tag
from models import Article
from log import logger
from datetime import timedelta


def _convert_to_article(tag: Tag) -> Article:
    return Article(
        url=tag.find('rbc_news:pdalink').text,
        tags=f"#rbc #{tag.category.text.replace(' ', '_')}".lower(),
        time=datetime.strptime(tag.pubdate.text, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None),
        source='RBC'
    )


class RBC:
    TimeDelta = timedelta(days=2)

    def __init__(self, last_time: str) -> None:
        self.__url = 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss'
        self.source = 'RBC'
        self.last_time = last_time


    def _get_news_feeds(self) -> list:
        def filter_fun(x):
            logger.debug(F"RBC filt: {x.time}>{self.last_time}  = {x.time.timestamp() > self.last_time.timestamp()}")
            return x.time.timestamp() > self.last_time.timestamp()
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elems = soup.find_all('item')
        list_articles = list(map(_convert_to_article, elems))
        return list(filter(filter_fun, list_articles))


    def call(self) -> list:
        res = self._get_news_feeds()
        logger.debug(F"RBC: articles of number {len(res)}")
        return res