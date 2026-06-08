"""
Бизнес-логика для работы со студентами, курсами и записями
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Student, Course
from database import get_session


class StudentService:
    """Сервис для работы со студентами"""
    
    @staticmethod
    def create_student(full_name: str, age: int, email: str, phone: str, session: Session = None) -> Student:
        """Создать нового студента"""
        if session is None:
            session = get_session()
        
        try:
            student = Student(
                full_name=full_name,
                age=age,
                email=email,
                phone=phone
            )
            session.add(student)
            session.commit()
            return student
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка при создании студента: {str(e)}")
    
    @staticmethod
    def get_all_students(session: Session = None) -> List[Student]:
        """Получить всех студентов"""
        if session is None:
            session = get_session()
        return session.query(Student).all()
    
    @staticmethod
    def get_student_by_id(student_id: int, session: Session = None) -> Optional[Student]:
        """Получить студента по ID"""
        if session is None:
            session = get_session()
        return session.query(Student).filter(Student.id == student_id).first()
    
    @staticmethod
    def search_students_by_name(name: str, session: Session = None) -> List[Student]:
        """Поиск студентов по имени"""
        if session is None:
            session = get_session()
        return session.query(Student).filter(Student.full_name.ilike(f"%{name}%")).all()
    
    @staticmethod
    def update_student(student_id: int, full_name: str = None, age: int = None, 
                      email: str = None, phone: str = None, session: Session = None) -> Optional[Student]:
        """Обновить информацию студента"""
        if session is None:
            session = get_session()
        
        try:
            student = session.query(Student).filter(Student.id == student_id).first()
            if student:
                if full_name:
                    student.full_name = full_name
                if age:
                    student.age = age
                if email:
                    student.email = email
                if phone:
                    student.phone = phone
                session.commit()
            return student
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка при обновлении студента: {str(e)}")
    
    @staticmethod
    def delete_student(student_id: int, session: Session = None) -> bool:
        """Удалить студента"""
        if session is None:
            session = get_session()
        
        try:
            student = session.query(Student).filter(Student.id == student_id).first()
            if student:
                session.delete(student)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка при удалении студента: {str(e)}")


class CourseService:
    """Сервис для работы с курсами"""
    
    @staticmethod
    def create_course(title: str, instructor: str, duration_hours: int, session: Session = None) -> Course:
        """Создать новый курс"""
        if session is None:
            session = get_session()
        
        try:
            course = Course(
                title=title,
                instructor=instructor,
                duration_hours=duration_hours
            )
            session.add(course)
            session.commit()
            return course
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка при создании курса: {str(e)}")
    
    @staticmethod
    def get_all_courses(session: Session = None) -> List[Course]:
        """Получить все курсы"""
        if session is None:
            session = get_session()
        return session.query(Course).all()
    
    @staticmethod
    def get_course_by_id(course_id: int, session: Session = None) -> Optional[Course]:
        """Получить курс по ID"""
        if session is None:
            session = get_session()
        return session.query(Course).filter(Course.id == course_id).first()
    
    @staticmethod
    def search_courses_by_title(title: str, session: Session = None) -> List[Course]:
        """Поиск курсов по названию"""
        if session is None:
            session = get_session()
        return session.query(Course).filter(Course.title.ilike(f"%{title}%")).all()
    
    @staticmethod
    def update_course(course_id: int, title: str = None, instructor: str = None,
                     duration_hours: int = None, session: Session = None) -> Optional[Course]:
        """Обновить информацию курса"""
        if session is None:
            session = get_session()
        
        try:
            course = session.query(Course).filter(Course.id == course_id).first()
            if course:
                if title:
                    course.title = title
                if instructor:
                    course.instructor = instructor
                if duration_hours:
                    course.duration_hours = duration_hours
                session.commit()
            return course
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка при обновлении курса: {str(e)}")
    
    @staticmethod
    def delete_course(course_id: int, session: Session = None) -> bool:
        """Удалить курс"""
        if session is None:
            session = get_session()
        
        try:
            course = session.query(Course).filter(Course.id == course_id).first()
            if course:
                session.delete(course)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка при удалении курса: {str(e)}")


class EnrollmentService:
    """Сервис для работы с записями студентов на курсы"""
    
    @staticmethod
    def enroll_student(student_id: int, course_id: int, session: Session = None) -> bool:
        """Записать студента на курс"""
        if session is None:
            session = get_session()
        
        try:
            student = session.query(Student).filter(Student.id == student_id).first()
            course = session.query(Course).filter(Course.id == course_id).first()
            
            if not student or not course:
                raise Exception("Студент или курс не найден")
            
            if course not in student.courses:
                student.courses.append(course)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка при записи на курс: {str(e)}")
    
    @staticmethod
    def unenroll_student(student_id: int, course_id: int, session: Session = None) -> bool:
        """Удалить студента с курса"""
        if session is None:
            session = get_session()
        
        try:
            student = session.query(Student).filter(Student.id == student_id).first()
            course = session.query(Course).filter(Course.id == course_id).first()
            
            if not student or not course:
                raise Exception("Студент или курс не найден")
            
            if course in student.courses:
                student.courses.remove(course)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка при удалении записи с курса: {str(e)}")
    
    @staticmethod
    def get_student_courses(student_id: int, session: Session = None) -> List[Course]:
        """Получить все курсы студента"""
        if session is None:
            session = get_session()
        
        student = session.query(Student).filter(Student.id == student_id).first()
        if student:
            return student.courses
        return []
    
    @staticmethod
    def get_course_students(course_id: int, session: Session = None) -> List[Student]:
        """Получить всех студентов курса"""
        if session is None:
            session = get_session()
        
        course = session.query(Course).filter(Course.id == course_id).first()
        if course:
            return course.students
        return []
