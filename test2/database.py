"""
Конфигурация базы данных и управление сессиями
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
import os

# Путь к файлу БД
DB_PATH = os.path.join(os.path.dirname(__file__), 'students_courses.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Создание engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Установите True для отладки SQL запросов
)

# Создание SessionLocal для работы с сессиями
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Инициализация базы данных - создание всех таблиц"""
    Base.metadata.create_all(bind=engine)
    print(f"✓ База данных инициализирована: {DB_PATH}")


def get_session() -> Session:
    """Получить новую сессию БД"""
    return SessionLocal()


def close_session(session: Session):
    """Закрыть сессию"""
    if session:
        session.close()
