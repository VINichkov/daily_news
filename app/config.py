from dotenv import load_dotenv

load_dotenv("./share/.env")

from sqlalchemy.orm import Session
from models import articles
# crud
from database import DB, engine



articles.Base.metadata.create_all(bind=engine)

