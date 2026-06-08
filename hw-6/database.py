from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    from models import Book, Reader, Borrow
    Base.metadata.create_all(engine)

def get_session():
    """Получить сессию БД"""
    return SessionLocal()
