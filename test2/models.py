"""
Модели данных для приложения Student Course Manager
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Таблица связи для многие-ко-многим отношения студентов и курсов
student_course_association = Table(
    'student_course_association',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id', ondelete='CASCADE'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id', ondelete='CASCADE'), primary_key=True),
    Column('enrollment_date', DateTime, default=datetime.utcnow)
)


class Student(Base):
    """Модель студента"""
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    
    # Связь с курсами
    courses = relationship(
        'Course',
        secondary=student_course_association,
        back_populates='students',
        cascade='all, delete'
    )
    
    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.full_name}', email='{self.email}')>"


class Course(Base):
    """Модель курса"""
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    instructor = Column(String(100), nullable=False)
    duration_hours = Column(Integer, nullable=False)  # Длительность в часах
    
    # Связь со студентами
    students = relationship(
        'Student',
        secondary=student_course_association,
        back_populates='courses',
        cascade='all, delete'
    )
    
    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', instructor='{self.instructor}')>"
