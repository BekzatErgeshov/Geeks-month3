from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Путь к БД в папке проекта
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "finance.db")
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)