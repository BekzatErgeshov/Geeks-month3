from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel, QMessageBox
from services.transaction import create_transaction, get_categories

class AddTransactionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить операцию")
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()

        # Сумма
        layout.addWidget(QLabel("Сумма:"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Введите сумму")
        layout.addWidget(self.amount_input)

        # Тип
        layout.addWidget(QLabel("Тип:"))
        self.type_box = QComboBox()
        self.type_box.addItems(["income", "expense"])
        self.type_box.setItemText(0, "Доход")
        self.type_box.setItemText(1, "Расход")
        layout.addWidget(self.type_box)

        # Категория
        layout.addWidget(QLabel("Категория:"))
        self.category_box = QComboBox()
        self.categories = get_categories()
        for c in self.categories:
            self.category_box.addItem(c.name, c.id)
        layout.addWidget(self.category_box)

        # Описание
        layout.addWidget(QLabel("Описание:"))
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Введите описание")
        layout.addWidget(self.description_input)

        # Кнопка сохранения
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save(self):
        try:
            amount_text = self.amount_input.text().strip()
            if not amount_text:
                QMessageBox.warning(self, "Ошибка", "Введите сумму")
                return
            
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, "Ошибка", "Сумма должна быть больше нуля")
                return
            
            type_ = "income" if self.type_box.currentIndex() == 0 else "expense"
            category_id = self.category_box.currentData()
            description = self.description_input.text().strip()

            create_transaction(amount, type_, category_id, description)
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму")