from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from models import Article
from log import logger


class ArticleRep:

    def __init__(self, db: Session):
        self.db = db

    def get_first_item(self) -> Article:

        item = self.db.query(Article) \
            .filter(Article.sent == False) \
            .order_by(Article.time.asc()).first()
        return item

    def get_last_time_by_source(self, source: str, delta: timedelta = timedelta(minutes=20)) -> datetime:
        offset = timezone(timedelta(hours=3))  # UTS MSK
        item = self.db.query(Article) \
            .filter(Article.source == source) \
            .order_by(Article.time.desc()).first()
        if item is None:

            time = datetime.now(offset) - delta
            time = time.replace(tzinfo=None)
        else:

            time = item.time
        logger.debug(F"ArticleRep: last time is {time}")
        return time

    def create_row_by_source(self, article: Article) -> Article:
        item = article
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def sent(self, article: Article):
        self.db.query(Article).filter(Article.id == article.id).update({'sent': True})
        self.db.commit()
        return article

    def clear(self):
        time = datetime.now() - timedelta(days=1)
        self.db.query(Article).where(Article.sent == True, Article.time < time).delete()
        self.db.commit()
