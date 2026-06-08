from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    type = Column(String)  # income / expense
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category")