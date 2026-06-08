"""
Диалоговые окна для добавления и редактирования данных
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QSpinBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from models import Student, Course


class AddStudentDialog(QDialog):
    """Диалог добавления нового студента"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.student_data = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Добавить студента")
        self.setGeometry(100, 100, 400, 250)
        
        layout = QVBoxLayout()
        
        # ФИО
        layout.addWidget(QLabel("ФИО:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)
        
        # Возраст
        layout.addWidget(QLabel("Возраст:"))
        self.age_input = QSpinBox()
        self.age_input.setMinimum(1)
        self.age_input.setMaximum(120)
        self.age_input.setValue(18)
        layout.addWidget(self.age_input)
        
        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)
        
        # Телефон
        layout.addWidget(QLabel("Номер телефона:"))
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_input)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Получить введённые данные"""
        return {
            'full_name': self.name_input.text(),
            'age': self.age_input.value(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text()
        }


class EditStudentDialog(QDialog):
    """Диалог редактирования студента"""
    
    def __init__(self, student: Student, parent=None):
        super().__init__(parent)
        self.student = student
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Редактировать студента - {self.student.full_name}")
        self.setGeometry(100, 100, 400, 250)
        
        layout = QVBoxLayout()
        
        # ФИО
        layout.addWidget(QLabel("ФИО:"))
        self.name_input = QLineEdit()
        self.name_input.setText(self.student.full_name)
        layout.addWidget(self.name_input)
        
        # Возраст
        layout.addWidget(QLabel("Возраст:"))
        self.age_input = QSpinBox()
        self.age_input.setMinimum(1)
        self.age_input.setMaximum(120)
        self.age_input.setValue(self.student.age)
        layout.addWidget(self.age_input)
        
        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setText(self.student.email)
        layout.addWidget(self.email_input)
        
        # Телефон
        layout.addWidget(QLabel("Номер телефона:"))
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.student.phone)
        layout.addWidget(self.phone_input)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Получить отредактированные данные"""
        return {
            'full_name': self.name_input.text(),
            'age': self.age_input.value(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text()
        }


class AddCourseDialog(QDialog):
    """Диалог добавления нового курса"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Добавить курс")
        self.setGeometry(100, 100, 400, 250)
        
        layout = QVBoxLayout()
        
        # Название курса
        layout.addWidget(QLabel("Название курса:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)
        
        # Преподаватель
        layout.addWidget(QLabel("Преподаватель:"))
        self.instructor_input = QLineEdit()
        layout.addWidget(self.instructor_input)
        
        # Длительность
        layout.addWidget(QLabel("Длительность (часов):"))
        self.duration_input = QSpinBox()
        self.duration_input.setMinimum(1)
        self.duration_input.setMaximum(1000)
        self.duration_input.setValue(40)
        layout.addWidget(self.duration_input)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Получить введённые данные"""
        return {
            'title': self.title_input.text(),
            'instructor': self.instructor_input.text(),
            'duration_hours': self.duration_input.value()
        }


class EditCourseDialog(QDialog):
    """Диалог редактирования курса"""
    
    def __init__(self, course: Course, parent=None):
        super().__init__(parent)
        self.course = course
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Редактировать курс - {self.course.title}")
        self.setGeometry(100, 100, 400, 250)
        
        layout = QVBoxLayout()
        
        # Название курса
        layout.addWidget(QLabel("Название курса:"))
        self.title_input = QLineEdit()
        self.title_input.setText(self.course.title)
        layout.addWidget(self.title_input)
        
        # Преподаватель
        layout.addWidget(QLabel("Преподаватель:"))
        self.instructor_input = QLineEdit()
        self.instructor_input.setText(self.course.instructor)
        layout.addWidget(self.instructor_input)
        
        # Длительность
        layout.addWidget(QLabel("Длительность (часов):"))
        self.duration_input = QSpinBox()
        self.duration_input.setMinimum(1)
        self.duration_input.setMaximum(1000)
        self.duration_input.setValue(self.course.duration_hours)
        layout.addWidget(self.duration_input)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Получить отредактированные данные"""
        return {
            'title': self.title_input.text(),
            'instructor': self.instructor_input.text(),
            'duration_hours': self.duration_input.value()
        }
