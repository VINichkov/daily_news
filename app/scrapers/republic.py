import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
from models import Article
from log import logger
from urllib.parse import urlparse


def _convert_to_article(tag: Tag) -> Article:
    img = BeautifulSoup(tag.description.text, 'html.parser').find('img')
    url_p = ''
    desc = ''
    if img is not None:
        url_p = img.get('src')
    desc_tag = tag.find('description')
    if desc_tag is not None:
        desc_all_text= desc_tag.text
        index = desc_all_text.find('<br/>')
        if index != -1:
            desc = desc_all_text[index+5:].strip()

    return Article(
        url=_url(tag.source.get('url')),
        tags="#republic #иностранный_агент",
        time=datetime.strptime(tag.pubdate.text, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None),
        source='Republic',
        title=tag.find('title').text,
        text=desc,
        picture_url=url_p
    )


def _url(origin_url: str) -> str:
    parse_url = urlparse(origin_url)
    new_url = parse_url._replace(query='')
    return new_url.geturl()


class Republic:
    TimeDelta = timedelta(days=2)

    def __init__(self, last_time: str) -> None:
        self.__url = 'https://republic.ru/export/all.xml'
        self.source = 'Republic'
        self.last_time = last_time

    def _get_news_feeds(self) -> list:
        def filter_fun(x):
            logger.debug(
                F"Republic filt: {x.time}>{self.last_time}  = {x.time.timestamp() > self.last_time.timestamp()}")
            return x.time.timestamp() > self.last_time.timestamp()

        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elems = soup.find_all('item')
        list_articles = list(map(_convert_to_article, elems))
        return list(filter(filter_fun, list_articles))

    def call(self) -> list:
        res = self._get_news_feeds()
        logger.info(F"Republic: articles of number {len(res)}")
        return res
