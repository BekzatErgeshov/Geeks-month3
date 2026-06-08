from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QListWidget, QMessageBox, QLabel
)


class MainWindow(QWidget):
    def __init__(self, services, user):
        super().__init__()
        self.services = services
        self.user = user

        self.setWindowTitle(f"Task Manage ({user.username}) - Роль: {user.role.upper()}")

        if self.services.is_admin(user):
            self.setup_admin_ui()
        else:
            self.setup_employee_ui()

    def setup_employee_ui(self):
        """Интерфейс для сотрудника"""
        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите задачу")

        self.btn_add = QPushButton("Добавить")
        self.btn_delete = QPushButton("Удалить выбранное")

        self.list_widget = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Мои задачи:"))
        layout.addWidget(self.input)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        self.btn_add.clicked.connect(self.add_task)
        self.btn_delete.clicked.connect(self.delete_task)

        self.load_tasks()

    def setup_admin_ui(self):
        """Интерфейс для администратора"""
        self.list_widget = QListWidget()
        
        self.btn_refresh = QPushButton("Обновить список")
        self.btn_refresh.clicked.connect(self.load_users)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Список пользователей:"))
        layout.addWidget(self.list_widget)
        layout.addWidget(self.btn_refresh)

        self.setLayout(layout)
        
        self.load_users()

    def add_task(self):
        text = self.input.text()

        if not text:
            return

        self.services.create_task(text, self.user.id)

        self.input.clear()
        self.load_tasks()

    def load_tasks(self):
        self.list_widget.clear()

        tasks = self.services.get_tasks(self.user.id)

        for task in tasks:
            self.list_widget.addItem(f"{task.id} : {task.title}")

    def delete_task(self):
        selected = self.list_widget.currentItem()

        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выбери Задачу")
            return 

        task_id = int(selected.text().split(":")[0])

        self.services.delete_task(task_id)
        self.load_tasks()

    def load_users(self):
        """Загружает список всех пользователей для администратора"""
        self.list_widget.clear()

        users = self.services.get_all_users()

        for user in users:
            role_text = "ADMIN" if user.role == "admin" else "EMPLOYEE"
            self.list_widget.addItem(f"{user.id}: {user.username} ({role_text})")
