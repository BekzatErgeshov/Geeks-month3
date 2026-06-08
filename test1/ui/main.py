import sys
from PyQt6.QtWidgets import QApplication
from database.db import engine
from database.models import Base, Category
from database.db import SessionLocal
from ui.main_window import MainWindow

def seed_categories():
    """Заполняет БД начальными категориями"""
    session = SessionLocal()
    try:
        if not session.query(Category).first():
            categories = [
                Category(name="Еда"),
                Category(name="Транспорт"),
                Category(name="Зарплата"),
                Category(name="Развлечения"),
                Category(name="Коммунальные услуги"),
                Category(name="Медицина"),
                Category(name="Образование"),
                Category(name="Прочее")
            ]
            session.add_all(categories)
            session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    # Создаем таблицы в БД
    Base.metadata.create_all(engine)
    # Добавляем начальные данные
    seed_categories()

    # Запускаем приложение
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())