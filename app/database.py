import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    os.getenv('DATABASE_URL'), connect_args={"check_same_thread": False}, echo=False
)
DB = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()