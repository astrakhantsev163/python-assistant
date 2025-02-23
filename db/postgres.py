from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Postgres

engine = create_engine(Postgres.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Функция для получения сессии БД
def get_postgres():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
