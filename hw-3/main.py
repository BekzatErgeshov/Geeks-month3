import sys
from PyQt6.QtWidgets import QApplication, QInputDialog

from database import engine, SessionLocal, Base
from services import TaskServices
from ui import MainWindow

Base.metadata.create_all(engine)


def main():
    app = QApplication(sys.argv)

    # session
    session = SessionLocal()
    service = TaskServices(session)

    username, ok = QInputDialog.getText(None, "Login", "Введите имя:")

    if not ok or not username:
        return

    user = service.get_user(username)

    if not user:
        all_users = service.get_all_users()
        role = "admin" if len(all_users) == 0 else "employee"
        user = service.create_user(username, role)
        
        if role == "admin":
            print(f"Первый пользователь '{username}' создан с ролью АДМИНИСТРАТОР")

    window = MainWindow(service, user)
    window.show()

    sys.exit(app.exec())

main()
