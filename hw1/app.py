import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, 
    QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите текст...")
        
        self.button = QPushButton("Показать")
        self.button.clicked.connect(self.on_button_click)
        
        self.label = QLabel("...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите тескт:"))
        layout.addWidget(self.input_field)
        layout.addWidget(self.button)
        layout.addWidget(QLabel("Резултат:"))
        layout.addWidget(self.label)
        layout.addStretch()
        
        self.setLayout(layout)
        
        self.setWindowTitle("Mini UI приложение")
        self.setGeometry(100, 100, 400, 300)

    def on_button_click(self):
        """Обработчик нажатия кнопки"""
        text = self.input_field.text()
        
        if text.strip() == "":
            self.label.setText("Введите текст!")
        else:
            self.label.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())