from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QLabel, QComboBox, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from services.transaction import (
    get_all_transactions, delete_transaction, get_categories, 
    calculate_balance, get_transactions_by_type, get_transactions_by_category
)
from ui.dialog import AddTransactionDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Tracker")
        self.setGeometry(100, 100, 900, 600)

        # Главный виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Баланс
        balance_layout = QHBoxLayout()
        self.balance_label = QLabel("Баланс: 0 руб.")
        self.balance_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        balance_layout.addWidget(self.balance_label)
        balance_layout.addStretch()
        layout.addLayout(balance_layout)

        # Фильтры
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Фильтр:"))
        
        self.filter_box = QComboBox()
        self.filter_box.addItem("Все операции", "all")
        self.filter_box.addItem("Доходы", "income")
        self.filter_box.addItem("Расходы", "expense")
        self.filter_box.currentIndexChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.filter_box)
        
        filter_layout.addWidget(QLabel("По категории:"))
        self.category_box = QComboBox()
        self.category_box.addItem("Все категории", None)
        categories = get_categories()
        for c in categories:
            self.category_box.addItem(c.name, c.id)
        self.category_box.currentIndexChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.category_box)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Сумма", "Тип", "Категория", "Описание", "Дата"])
        self.table.setColumnWidth(4, 200)
        layout.addWidget(self.table)

        # Кнопки
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Добавить операцию")
        add_btn.clicked.connect(self.open_add_dialog)
        buttons_layout.addWidget(add_btn)

        delete_btn = QPushButton("❌ Удалить операцию")
        delete_btn.clicked.connect(self.delete_selected)
        buttons_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.clicked.connect(self.load_data)
        buttons_layout.addWidget(refresh_btn)

        layout.addLayout(buttons_layout)

        main_widget.setLayout(layout)
        self.load_data()

    def load_data(self):
        """Загружает все операции в таблицу"""
        data = get_all_transactions()
        self.table.setRowCount(len(data))

        for row, t in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(t.id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(t.amount)))
            type_display = "Доход" if t.type == "income" else "Расход"
            self.table.setItem(row, 2, QTableWidgetItem(type_display))
            self.table.setItem(row, 3, QTableWidgetItem(t.category.name if t.category else ""))
            self.table.setItem(row, 4, QTableWidgetItem(t.description or ""))
            self.table.setItem(row, 5, QTableWidgetItem(t.created_at.strftime("%Y-%m-%d %H:%M") if t.created_at else ""))

        self.update_balance()

    def apply_filter(self):
        """Применяет фильтры к таблице"""
        filter_type = self.filter_box.currentData()
        category_id = self.category_box.currentData()

        # Получаем все данные
        if filter_type == "all":
            data = get_all_transactions()
        else:
            data = get_transactions_by_type(filter_type)

        # Фильтруем по категории если выбрана
        if category_id is not None:
            data = [t for t in data if t.category_id == category_id]

        # Обновляем таблицу
        self.table.setRowCount(len(data))
        for row, t in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(t.id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(t.amount)))
            type_display = "Доход" if t.type == "income" else "Расход"
            self.table.setItem(row, 2, QTableWidgetItem(type_display))
            self.table.setItem(row, 3, QTableWidgetItem(t.category.name if t.category else ""))
            self.table.setItem(row, 4, QTableWidgetItem(t.description or ""))
            self.table.setItem(row, 5, QTableWidgetItem(t.created_at.strftime("%Y-%m-%d %H:%M") if t.created_at else ""))

        self.update_balance()

    def update_balance(self):
        """Обновляет отображение баланса"""
        balance = calculate_balance()
        self.balance_label.setText(f"Баланс: {balance:.2f} руб.")

    def open_add_dialog(self):
        """Открывает диалог добавления операции"""
        dialog = AddTransactionDialog()
        if dialog.exec() == 1:  # QDialog.Accepted
            self.load_data()
            # Сбрасываем фильтры
            self.filter_box.blockSignals(True)
            self.category_box.blockSignals(True)
            self.filter_box.setCurrentIndex(0)
            self.category_box.setCurrentIndex(0)
            self.filter_box.blockSignals(False)
            self.category_box.blockSignals(False)

    def delete_selected(self):
        """Удаляет выбранную операцию"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите операцию для удаления")
            return

        transaction_id = int(self.table.item(current_row, 0).text())
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить эту операцию?")
        
        if reply == QMessageBox.StandardButton.Yes:
            delete_transaction(transaction_id)
            self.load_data()

        self.balance_label.setText(f"Баланс: {balance}")

    def open_add_dialog(self):
        dialog = AddTransactionDialog()
        if dialog.exec():
            self.load_data()

    def delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            transaction_id = int(self.table.item(row, 0).text())
            delete_transaction(transaction_id)
            self.load_data()