from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QLineEdit, QListWidget, QVBoxLayout, QHBoxLayout, QMessageBox
)
from services.service import NotesService

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.service = NotesService()        
        self.setup_window()
        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.update_notes()

    def setup_window(self):
        self.setWindowTitle("Notes APP")
        self.resize(400, 500)

    def create_widgets(self):
        self.title = QLabel("Мои заметки")
        self.input_note = QLineEdit()
        self.input_note.setPlaceholderText("Введите заметку")
        self.button_add = QPushButton("Добавить")
        self.button_clear = QPushButton("Очистить все")
        self.notes_list = QListWidget()

    def create_layout(self):
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        layout.addWidget(self.title)
        layout.addWidget(self.input_note)
        
        button_layout.addWidget(self.button_add)
        button_layout.addWidget(self.button_clear)
        layout.addLayout(button_layout)
        
        layout.addWidget(self.notes_list)

        self.setLayout(layout)

    def connect_signals(self):
        self.button_add.clicked.connect(self.add_note)
        self.button_clear.clicked.connect(self.clear_all)
        self.notes_list.itemDoubleClicked.connect(self.delete_note)
        self.input_note.returnPressed.connect(self.add_note)

    def add_note(self):
        text = self.input_note.text()

        if self.service.add_note(text):
            self.update_notes()
            self.input_note.clear()
        else:
            QMessageBox.warning(self, "Ошибка", "Эта заметка уже существует или поле пусто!")

    def update_notes(self):
        self.notes_list.clear()
        self.notes_list.addItems(
            self.service.get_notes()
        )

    def delete_note(self, item):
        text = item.text()
        self.service.delete_note(text)
        self.update_notes()

    def clear_all(self):
        reply = QMessageBox.question(
            self, 
            "Подтверждение", 
            "Вы уверены? Все заметки будут удалены!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.service.db.clear_all()
            self.update_notes()