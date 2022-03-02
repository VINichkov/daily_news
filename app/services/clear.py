import config
from repositories import ArticleRep


class Clear:

    def __init__(self):
        self.rep = ArticleRep(config.DB())

    def call(self):
        self.rep.clear()
