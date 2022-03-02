from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    url = Column(String, nullable=False)
    tags = Column(String, nullable=False)
    text = Column(String)
    picture_url = Column(String)
    title = Column(String, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)
    sent = Column(Boolean, default=False)
