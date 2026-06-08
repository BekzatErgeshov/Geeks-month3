"""
Student Course Manager - Приложение для управления студентами и курсами
Главная точка входа приложения
"""
import sys
from PyQt6.QtWidgets import QApplication
from database import init_db
from ui.main_window import MainWindow


def main():
    """Запуск приложения"""
    # Инициализация базы данных
    init_db()
    
    # Создание приложения PyQt6
    app = QApplication(sys.argv)
    
    # Создание и отображение главного окна
    window = MainWindow()
    window.show()
    
    # Запуск цикла событий
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
