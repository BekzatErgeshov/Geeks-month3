"""
Главное окно приложения Student Course Manager
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
    QLabel, QMessageBox, QComboBox, QDialog
)
from PyQt6.QtCore import Qt
from services import StudentService, CourseService, EnrollmentService
from database import get_session, close_session
from ui.dialogs import (
    AddStudentDialog, EditStudentDialog, AddCourseDialog, EditCourseDialog
)


class StudentTab(QWidget):
    """Вкладка управления студентами"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = get_session()
        self.init_ui()
        self.refresh_students()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Поиск
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Поиск по имени:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите имя студента...")
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("Поиск")
        search_btn.clicked.connect(self.search_students)
        search_layout.addWidget(search_btn)
        
        reset_btn = QPushButton("Сброс")
        reset_btn.clicked.connect(self.refresh_students)
        search_layout.addWidget(reset_btn)
        
        layout.addLayout(search_layout)
        
        # Таблица студентов
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "ФИО", "Возраст", "Email", "Телефон"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.table)
        
        # Кнопки операций
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Добавить")
        add_btn.clicked.connect(self.add_student)
        buttons_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Редактировать")
        edit_btn.clicked.connect(self.edit_student)
        buttons_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Удалить")
        delete_btn.clicked.connect(self.delete_student)
        buttons_layout.addWidget(delete_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def refresh_students(self):
        """Обновить список студентов"""
        self.search_input.clear()
        students = StudentService.get_all_students(self.session)
        self.display_students(students)
    
    def search_students(self):
        """Поиск студентов по имени"""
        search_term = self.search_input.text().strip()
        if search_term:
            students = StudentService.search_students_by_name(search_term, self.session)
            self.display_students(students)
        else:
            self.refresh_students()
    
    def display_students(self, students):
        """Отобразить студентов в таблице"""
        self.table.setRowCount(len(students))
        for row, student in enumerate(students):
            self.table.setItem(row, 0, QTableWidgetItem(str(student.id)))
            self.table.setItem(row, 1, QTableWidgetItem(student.full_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(student.age)))
            self.table.setItem(row, 3, QTableWidgetItem(student.email))
            self.table.setItem(row, 4, QTableWidgetItem(student.phone))
    
    def add_student(self):
        """Добавить нового студента"""
        dialog = AddStudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data['full_name'] or not data['email'] or not data['phone']:
                QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
                return
            
            try:
                StudentService.create_student(
                    full_name=data['full_name'],
                    age=data['age'],
                    email=data['email'],
                    phone=data['phone'],
                    session=self.session
                )
                QMessageBox.information(self, "Успех", "Студент добавлен!")
                self.refresh_students()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
    
    def edit_student(self):
        """Редактировать студента"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите студента для редактирования!")
            return
        
        student_id = int(self.table.item(current_row, 0).text())
        student = StudentService.get_student_by_id(student_id, self.session)
        
        if not student:
            QMessageBox.critical(self, "Ошибка", "Студент не найден!")
            return
        
        dialog = EditStudentDialog(student, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data['full_name'] or not data['email'] or not data['phone']:
                QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
                return
            
            try:
                StudentService.update_student(
                    student_id=student_id,
                    full_name=data['full_name'],
                    age=data['age'],
                    email=data['email'],
                    phone=data['phone'],
                    session=self.session
                )
                QMessageBox.information(self, "Успех", "Студент обновлён!")
                self.refresh_students()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
    
    def delete_student(self):
        """Удалить студента"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите студента для удаления!")
            return
        
        student_id = int(self.table.item(current_row, 0).text())
        student_name = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы действительно хотите удалить студента '{student_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                StudentService.delete_student(student_id, self.session)
                QMessageBox.information(self, "Успех", "Студент удалён!")
                self.refresh_students()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))


class CourseTab(QWidget):
    """Вкладка управления курсами"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = get_session()
        self.init_ui()
        self.refresh_courses()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Поиск
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Поиск по названию:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите название курса...")
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("Поиск")
        search_btn.clicked.connect(self.search_courses)
        search_layout.addWidget(search_btn)
        
        reset_btn = QPushButton("Сброс")
        reset_btn.clicked.connect(self.refresh_courses)
        search_layout.addWidget(reset_btn)
        
        layout.addLayout(search_layout)
        
        # Таблица курсов
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Преподаватель", "Длительность (ч)"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.table)
        
        # Кнопки операций
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Добавить")
        add_btn.clicked.connect(self.add_course)
        buttons_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Редактировать")
        edit_btn.clicked.connect(self.edit_course)
        buttons_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Удалить")
        delete_btn.clicked.connect(self.delete_course)
        buttons_layout.addWidget(delete_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def refresh_courses(self):
        """Обновить список курсов"""
        self.search_input.clear()
        courses = CourseService.get_all_courses(self.session)
        self.display_courses(courses)
    
    def search_courses(self):
        """Поиск курсов по названию"""
        search_term = self.search_input.text().strip()
        if search_term:
            courses = CourseService.search_courses_by_title(search_term, self.session)
            self.display_courses(courses)
        else:
            self.refresh_courses()
    
    def display_courses(self, courses):
        """Отобразить курсы в таблице"""
        self.table.setRowCount(len(courses))
        for row, course in enumerate(courses):
            self.table.setItem(row, 0, QTableWidgetItem(str(course.id)))
            self.table.setItem(row, 1, QTableWidgetItem(course.title))
            self.table.setItem(row, 2, QTableWidgetItem(course.instructor))
            self.table.setItem(row, 3, QTableWidgetItem(str(course.duration_hours)))
    
    def add_course(self):
        """Добавить новый курс"""
        dialog = AddCourseDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data['title'] or not data['instructor']:
                QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
                return
            
            try:
                CourseService.create_course(
                    title=data['title'],
                    instructor=data['instructor'],
                    duration_hours=data['duration_hours'],
                    session=self.session
                )
                QMessageBox.information(self, "Успех", "Курс добавлен!")
                self.refresh_courses()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
    
    def edit_course(self):
        """Редактировать курс"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите курс для редактирования!")
            return
        
        course_id = int(self.table.item(current_row, 0).text())
        course = CourseService.get_course_by_id(course_id, self.session)
        
        if not course:
            QMessageBox.critical(self, "Ошибка", "Курс не найден!")
            return
        
        dialog = EditCourseDialog(course, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data['title'] or not data['instructor']:
                QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
                return
            
            try:
                CourseService.update_course(
                    course_id=course_id,
                    title=data['title'],
                    instructor=data['instructor'],
                    duration_hours=data['duration_hours'],
                    session=self.session
                )
                QMessageBox.information(self, "Успех", "Курс обновлён!")
                self.refresh_courses()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
    
    def delete_course(self):
        """Удалить курс"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите курс для удаления!")
            return
        
        course_id = int(self.table.item(current_row, 0).text())
        course_title = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы действительно хотите удалить курс '{course_title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                CourseService.delete_course(course_id, self.session)
                QMessageBox.information(self, "Успех", "Курс удалён!")
                self.refresh_courses()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))


class EnrollmentTab(QWidget):
    """Вкладка управления записями на курсы"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = get_session()
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Выбор студента и курса
        selection_layout = QHBoxLayout()
        
        selection_layout.addWidget(QLabel("Студент:"))
        self.student_combo = QComboBox()
        selection_layout.addWidget(self.student_combo)
        
        selection_layout.addWidget(QLabel("Курс:"))
        self.course_combo = QComboBox()
        selection_layout.addWidget(self.course_combo)
        
        layout.addLayout(selection_layout)
        
        # Кнопки для записи и отписки
        enroll_buttons_layout = QHBoxLayout()
        
        enroll_btn = QPushButton("✅ Записать на курс")
        enroll_btn.clicked.connect(self.enroll_student)
        enroll_buttons_layout.addWidget(enroll_btn)
        
        unenroll_btn = QPushButton("❌ Отписать с курса")
        unenroll_btn.clicked.connect(self.unenroll_student)
        enroll_buttons_layout.addWidget(unenroll_btn)
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.clicked.connect(self.refresh_data)
        enroll_buttons_layout.addWidget(refresh_btn)
        
        layout.addLayout(enroll_buttons_layout)
        
        # Таблица записей студента
        layout.addWidget(QLabel("Курсы студента:"))
        self.student_courses_table = QTableWidget()
        self.student_courses_table.setColumnCount(4)
        self.student_courses_table.setHorizontalHeaderLabels(["ID", "Название", "Преподаватель", "Длительность (ч)"])
        layout.addWidget(self.student_courses_table)
        
        # Таблица студентов курса
        layout.addWidget(QLabel("Студенты курса:"))
        self.course_students_table = QTableWidget()
        self.course_students_table.setColumnCount(4)
        self.course_students_table.setHorizontalHeaderLabels(["ID", "ФИО", "Email", "Телефон"])
        layout.addWidget(self.course_students_table)
        
        self.setLayout(layout)
        
        # Подключить сигналы
        self.student_combo.currentIndexChanged.connect(self.on_student_changed)
        self.course_combo.currentIndexChanged.connect(self.on_course_changed)
    
    def refresh_data(self):
        """Обновить данные студентов и курсов"""
        self.student_combo.clear()
        self.course_combo.clear()
        
        students = StudentService.get_all_students(self.session)
        courses = CourseService.get_all_courses(self.session)
        
        for student in students:
            self.student_combo.addItem(student.full_name, student.id)
        
        for course in courses:
            self.course_combo.addItem(course.title, course.id)
        
        if students:
            self.on_student_changed()
        if courses:
            self.on_course_changed()
    
    def on_student_changed(self):
        """Студент выбран - обновить курсы студента"""
        if self.student_combo.count() == 0:
            self.student_courses_table.setRowCount(0)
            return
        
        student_id = self.student_combo.currentData()
        courses = EnrollmentService.get_student_courses(student_id, self.session)
        
        self.student_courses_table.setRowCount(len(courses))
        for row, course in enumerate(courses):
            self.student_courses_table.setItem(row, 0, QTableWidgetItem(str(course.id)))
            self.student_courses_table.setItem(row, 1, QTableWidgetItem(course.title))
            self.student_courses_table.setItem(row, 2, QTableWidgetItem(course.instructor))
            self.student_courses_table.setItem(row, 3, QTableWidgetItem(str(course.duration_hours)))
    
    def on_course_changed(self):
        """Курс выбран - обновить студентов курса"""
        if self.course_combo.count() == 0:
            self.course_students_table.setRowCount(0)
            return
        
        course_id = self.course_combo.currentData()
        students = EnrollmentService.get_course_students(course_id, self.session)
        
        self.course_students_table.setRowCount(len(students))
        for row, student in enumerate(students):
            self.course_students_table.setItem(row, 0, QTableWidgetItem(str(student.id)))
            self.course_students_table.setItem(row, 1, QTableWidgetItem(student.full_name))
            self.course_students_table.setItem(row, 2, QTableWidgetItem(student.email))
            self.course_students_table.setItem(row, 3, QTableWidgetItem(student.phone))
    
    def enroll_student(self):
        """Записать студента на курс"""
        if self.student_combo.count() == 0 or self.course_combo.count() == 0:
            QMessageBox.warning(self, "Ошибка", "Нет доступных студентов или курсов!")
            return
        
        student_id = self.student_combo.currentData()
        course_id = self.course_combo.currentData()
        
        try:
            success = EnrollmentService.enroll_student(student_id, course_id, self.session)
            if success:
                QMessageBox.information(self, "Успех", "Студент записан на курс!")
                self.on_student_changed()
                self.on_course_changed()
            else:
                QMessageBox.information(self, "Информация", "Студент уже записан на этот курс!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def unenroll_student(self):
        """Отписать студента с курса"""
        if self.student_combo.count() == 0 or self.course_combo.count() == 0:
            QMessageBox.warning(self, "Ошибка", "Нет доступных студентов или курсов!")
            return
        
        student_id = self.student_combo.currentData()
        course_id = self.course_combo.currentData()
        
        try:
            success = EnrollmentService.unenroll_student(student_id, course_id, self.session)
            if success:
                QMessageBox.information(self, "Успех", "Студент отписан с курса!")
                self.on_student_changed()
                self.on_course_changed()
            else:
                QMessageBox.information(self, "Информация", "Студент не записан на этот курс!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Course Manager")
        self.setGeometry(100, 100, 1000, 600)
        
        # Создание вкладок
        tabs = QTabWidget()
        tabs.addTab(StudentTab(self), "👥 Студенты")
        tabs.addTab(CourseTab(self), "📚 Курсы")
        tabs.addTab(EnrollmentTab(self), "📝 Записи на курсы")
        
        self.setCentralWidget(tabs)
