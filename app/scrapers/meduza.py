import requests
from datetime import datetime
from bs4 import BeautifulSoup
from bs4 import Tag
from models import Article
from log import logger
from datetime import timedelta


def _convert_to_article(tag: Tag) -> Article:
    desc_tag = BeautifulSoup(tag.find('description').text, 'html.parser')
    desc = ''
    if desc_tag is not None:
        p = desc_tag.find_all('p')[2]
        if p is not None:
            desc = p.text
    return Article(
        url=tag.guid.text,
        tags="#meduza",
        time=datetime.strptime(tag.pubdate.text, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None),
        source='Meduza',
        title=desc,
        picture_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Meduza_logo.svg/200px-Meduza_logo.svg.png'
    )


class Meduza:
    TimeDelta = timedelta(minutes=10)

    def __init__(self, last_time: str) -> None:
        self.__url = 'https://meduza.io/rss/all'
        self.source = 'Meduza'
        self.last_time = last_time


    def _get_news_feeds(self) -> list:
        def filter_fun(x):
            logger.debug(F"Meduza filt: {x.time}>{self.last_time}  = {x.time.timestamp() > self.last_time.timestamp()}")
            return x.time.timestamp() > self.last_time.timestamp()
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elems = soup.find_all('item')
        list_articles = list(map(_convert_to_article, elems))
        return list(filter(filter_fun, list_articles))


    def call(self) -> list:
        res = self._get_news_feeds()
        logger.info(F"Meduza: articles of number {len(res)}")
        return res