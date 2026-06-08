import sys
from PyQt6.QtWidgets import QApplication
from database import init_db
from ui import LibraryManagerUI

def main():

    init_db()
    
    app = QApplication(sys.argv)
    window = LibraryManagerUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
