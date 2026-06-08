from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    
    borrows = relationship("Borrow", back_populates="book", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"


class Reader(Base):
    __tablename__ = "readers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    borrows = relationship("Borrow", back_populates="reader", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Reader(id={self.id}, name='{self.name}')>"


class Borrow(Base):
    __tablename__ = "borrows"
    
    id = Column(Integer, primary_key=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    
    reader = relationship("Reader", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")
    
    def __repr__(self):
        return f"<Borrow(reader_id={self.reader_id}, book_id={self.book_id})>"
