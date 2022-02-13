import os
from log import logger
import gevent
import config
from repositories import ArticleRep


class GetNewFeedsFromSites:

    def __init__(self):
        logger.debug('GetNewFeedsFromSites: init module')
        self.sources = os.getenv('SOURCES').split(', ')
        self.rep = ArticleRep(config.DB())
        self.articles = []

    def call(self) -> None:
        jobs = [gevent.spawn(self.__call, class_) for class_ in self.sources]
        gevent.joinall(jobs)
        for item in self.articles:
            self.rep.create_row_by_source(item)

    def __call(self, class_: str) -> None:
        logger.debug(F"Start: Class is {class_}")

        exec_text = f"from scrapers import {class_};"
        exec_text += f"time = self.rep.get_last_time_by_source('{class_}',{class_}.TimeDelta);"
        exec_text += F"self.articles += {class_}(last_time=time).call()"
        logger.debug(F"Start: execute str='{exec_text}'")
        exec(exec_text)

