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
        source='RBC',
        title=tag.find('title').text,
        text=tag.find('description').text
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
        all_articles = list(map(_convert_to_article, elems))
        filtered_articles = list(filter(filter_fun, all_articles))
        return list(map(self._get_picture, filtered_articles))

    def _get_picture(self, article: Article)->Article:
        response = requests.get(article.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        #with open(f"{i}.html", 'w') as f:
         #   f.write(soup.prettify())
        #TODO не было картинки
        img = soup.find(class_='g-image')
        if img is None:
            article.picture_url = 'https://toplogos.ru/images/thumbs/preview-logo-rbc.png'
        else:
            article.picture_url = soup.find(class_='g-image').get('src')
        return article
        #g-image  article__main-image__image


    def call(self) -> list:
        res = self._get_news_feeds()
        #self._get_news_feeds()
        logger.info(F"RBC: articles of number {len(res)}")
        return res