import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QListWidget, QLineEdit,
    QLabel, QMessageBox
)

from database import engine, SessionLocal, Base
from models import User, Product

Base.metadata.create_all(bind=engine)

db = SessionLocal()

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CRUD")
        self.resize(500, 500)

        self.layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Имя пользователя")
        self.add_user_btn = QPushButton("Добавить пользователя")
        self.add_user_btn.clicked.connect(self.create_user)

        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Название товара")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена")

        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("ID Владельца")

        self.add_product_btn = QPushButton("Добавить товар") 
        self.add_product_btn.clicked.connect(self.create_product)

        self.delete_product_input = QLineEdit()
        self.delete_product_input.setPlaceholderText("ID товара для удаления")
        self.delete_product_btn = QPushButton("Удалить товар")
        self.delete_product_btn.clicked.connect(self.delete_product)

        self.change_price_id_input = QLineEdit()
        self.change_price_id_input.setPlaceholderText("ID товара")
        self.change_price_new_input = QLineEdit()
        self.change_price_new_input.setPlaceholderText("Новая цена")
        self.change_price_btn = QPushButton("Изменить цену товара")
        self.change_price_btn.clicked.connect(self.change_price)
        
        self.show_product_btn = QPushButton("Показать товары")
        self.show_product_btn.clicked.connect(self.show_products)

        self.show_user_btn = QPushButton("Показать пользователей")
        self.show_user_btn.clicked.connect(self.show_users)

        self.user_filter_input = QLineEdit()
        self.user_filter_input.setPlaceholderText("ID пользователя для фильтра")
        self.join_btn = QPushButton("JOIN запрос")
        self.join_btn.clicked.connect(self.join_query)

        self.list_widget = QListWidget()

        self.layout.addWidget(QLabel("Пользователь"))
        self.layout.addWidget(self.user_input)
        self.layout.addWidget(self.add_user_btn)

        self.layout.addWidget(QLabel("Товар"))
        self.layout.addWidget(self.product_input)
        self.layout.addWidget(self.price_input)
        self.layout.addWidget(self.owner_input)
        self.layout.addWidget(self.add_product_btn)

        self.layout.addWidget(QLabel("Удалить товар"))
        self.layout.addWidget(self.delete_product_input)
        self.layout.addWidget(self.delete_product_btn)

        self.layout.addWidget(QLabel("Изменить цену"))
        self.layout.addWidget(self.change_price_id_input)
        self.layout.addWidget(self.change_price_new_input)
        self.layout.addWidget(self.change_price_btn)

        self.layout.addWidget(self.show_user_btn)
        self.layout.addWidget(self.show_product_btn)

        self.layout.addWidget(QLabel("Товары пользователя"))
        self.layout.addWidget(self.user_filter_input)
        self.layout.addWidget(self.join_btn)

        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

    def create_user(self):
        name = self.user_input.text()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите имя")
            return

        user = User(name=name)

        db.add(user)
        db.commit()

        QMessageBox.information(self, "Успех", "Пользователь создан")

        self.user_input.clear()

    def create_product(self):
        title = self.product_input.text()
        price = self.price_input.text()
        owner_id = self.owner_input.text()

        if not title or not price or not owner_id:
            QMessageBox.warning(self, "Error", "Запольните поля")
            return 

        product = Product(
            title=title,
            price=price,
            owner_id=int(owner_id)
        )

        db.add(product)
        db.commit()

        QMessageBox.information(self, "Успех", "Товар создан")
        self.product_input.clear()
        self.price_input.clear()
        self.owner_input.clear()

    def show_users(self):
        self.list_widget.clear()

        users = db.query(User).all()

        for user in users:
            self.list_widget.addItem(
                f"{user.id} - {user.name}"
            )

    def show_products(self):
        self.list_widget.clear()
        
        products = db.query(Product).all()

        for product in products:
            self.list_widget.addItem(
                f"{product.title} - {product.price}"
            )

    def join_query(self):
        self.list_widget.clear()

        user_id = self.user_filter_input.text()

        if not user_id:
            QMessageBox.warning(self, "Ошибка", "Введите ID пользователя")
            return

        products = db.query(Product).filter(Product.owner_id == int(user_id)).all()

        if not products:
            QMessageBox.information(self, "Результат", "Товары не найдены")
            return

        for product in products:
            self.list_widget.addItem(
                f"{product.title}\n"
                f"{product.price} руб.\n"
                f"Владелец: {product.owner.name}"
            )

    def delete_product(self):
        product_id = self.delete_product_input.text()

        if not product_id:
            QMessageBox.warning(self, "Ошибка", "Введите ID товара")
            return

        product = db.query(Product).filter(Product.id == int(product_id)).first()

        if not product:
            QMessageBox.warning(self, "Ошибка", "Товар не найден")
            return

        db.delete(product)
        db.commit()

        QMessageBox.information(self, "Успех", "Товар удален")
        self.delete_product_input.clear()

    def change_price(self):
        product_id = self.change_price_id_input.text()
        new_price = self.change_price_new_input.text()

        if not product_id or not new_price:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        product = db.query(Product).filter(Product.id == int(product_id)).first()

        if not product:
            QMessageBox.warning(self, "Ошибка", "Товар не найден")
            return

        product.price = new_price
        db.commit()

        QMessageBox.information(self, "Успех", "Цена изменена")
        self.change_price_id_input.clear()
        self.change_price_new_input.clear()
app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec())
