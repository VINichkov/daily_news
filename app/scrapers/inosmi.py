import requests
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup, Tag
from models import Article
from log import logger


class Inosmi:
    TimeDelta = timedelta(hours=1)

    def __init__(self, last_time: str) -> None:
        self.__url = 'https://inosmi.ru/today/'
        self.__domain = 'https://inosmi.ru'
        self.source = 'Inosmi'
        self.last_time = last_time


    def _get_news_feeds(self) -> list:
        def filter_fun(x):
            logger.debug(F"Inosmi filt: {x.time}>{self.last_time}  = {x.time.timestamp() > self.last_time.timestamp()}")
            return x.time.timestamp() > self.last_time.timestamp()
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elems = soup.find_all(class_='list-item')
        list_articles = list(map(self._convert_to_article, elems))
        return list(filter(filter_fun, list_articles))

    def call(self) -> list:
        res = self._get_news_feeds()
        logger.info(F"Inosmi: articles of number {len(res)}")
        return res

    def _convert_to_article(self, tag: Tag) -> Article:
        return Article(
            url=self.__domain + tag.find(class_='list-item__title').get('href'),
            tags=f"#Inosmi {self.__tags(tag.find(class_='source'))}".lower(),
            time= self.__date(tag.find(class_='list-item__date').text).replace(tzinfo=None),
            source='Inosmi',
            title=tag.find(class_='list-item__title').text,
            picture_url=tag.img.get('src')
        )

    def __tags(self, tag_name: Tag) -> str:
        if tag_name is not None:
            return ' '.join(list(map(lambda x: F"#{x.text}", tag_name.find_all('span'))))

    def __date(self, date_post: str) -> datetime:
        if date_post is not None:
            if len(date_post) > 5:
                date_post = date_post[len(date_post)-5:]
                date_p = datetime.today()- timedelta(days=1)
            else:
                date_p = datetime.today()
            time = datetime.strptime(date_post, '%H:%M')
            return datetime.combine(date_p, time.time())
