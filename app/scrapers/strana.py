import requests
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup, Tag
from models import Article
from log import logger
import re


class Strana:
    TimeDelta = timedelta(hours=2)

    def __init__(self, last_time: str) -> None:
        self.__url = 'https://strana.best/news.html'
        self.__domain = 'https://strana.best'
        self.source = 'Strana'
        self.last_time = last_time


    def _get_news_feeds(self) -> list:
        def filter_fun(x):
            logger.debug(F"Strana filt: {x.time}>{self.last_time}  = {x.time.timestamp() > self.last_time.timestamp()}")
            return x.time.timestamp() > self.last_time.timestamp()
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elems = soup.find_all(class_='lenta-news')
        all_articles = list(map(self._convert_to_article, elems))
        filtered_articles = list(filter(filter_fun, all_articles))
        return list(map(self._get_picture, filtered_articles))

    def call(self) -> list:
        res = self._get_news_feeds()
        logger.debug(F"Strana: articles of number {len(res)}")
        return res

    def _convert_to_article(self, tag: Tag) -> Article:
        return Article(
            url=self.__domain + tag.find(class_='article').get('href'),
            tags='#Страна_UA',
            time=self.__date(tag.time),
            source='Strana',
            title=tag.find(class_='article').text
        )

    def __tags(self, tag_name: Tag) -> str:
        if tag_name is not None:
            return ' '.join(list(map(lambda x: F"#{x.text}", tag_name.find_all('span'))))

    def __date(self, date_post: Tag) -> datetime:
        if date_post is not None:
            date_str = date_post.span.get('data-time')
            time_str = re.findall(r"\d\d:\d\d", date_post.text)[0]
            if date_str is not None and time_str is not None:
                datetime_d = datetime.fromisoformat(F"{date_str}T{time_str}:00") + timedelta(hours=1)
                return datetime_d

    def _get_picture(self, article: Article)->Article:
        response = requests.get(article.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        art = soup.find(class_='article')
        img = art.img
        if img is None:
            article.picture_url = 'https://strana.news/user/img/logo.png'
        else:
            article.picture_url = img.get('src')
        return article