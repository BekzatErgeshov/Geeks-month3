from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt
from database import get_session
from models import Book, Reader, Borrow

class LibraryManagerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.session = get_session()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Library Manager")
        self.setGeometry(100, 100, 900, 600)
        
        tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        
        tabs.addTab(self.create_books_tab(), "Books")
        
        tabs.addTab(self.create_readers_tab(), "Readers")
        
        tabs.addTab(self.create_borrows_tab(), "Borrowed Books")
        
        self.setLayout(main_layout)
    
    def create_books_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search book:"))
        self.search_book_input = QLineEdit()
        search_layout.addWidget(self.search_book_input)
        self.search_book_btn = QPushButton("Search")
        self.search_book_btn.clicked.connect(self.search_books)
        search_layout.addWidget(self.search_book_btn)
        layout.addLayout(search_layout)
        
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(3)
        self.books_table.setHorizontalHeaderLabels(["ID", "Title", "Author"])
        self.books_table.setColumnWidth(1, 300)
        layout.addWidget(self.books_table)
        
        add_book_layout = QHBoxLayout()
        add_book_layout.addWidget(QLabel("Title:"))
        self.book_title_input = QLineEdit()
        add_book_layout.addWidget(self.book_title_input)
        
        add_book_layout.addWidget(QLabel("Author:"))
        self.book_author_input = QLineEdit()
        add_book_layout.addWidget(self.book_author_input)
        
        self.add_book_btn = QPushButton("Add Book")
        self.add_book_btn.clicked.connect(self.add_book)
        add_book_layout.addWidget(self.add_book_btn)
        layout.addLayout(add_book_layout)
        
        delete_book_layout = QHBoxLayout()
        delete_book_layout.addWidget(QLabel("Book ID to delete:"))
        self.delete_book_id_input = QLineEdit()
        self.delete_book_id_input.setMaximumWidth(100)
        delete_book_layout.addWidget(self.delete_book_id_input)
        
        self.delete_book_btn = QPushButton("Delete Book")
        self.delete_book_btn.clicked.connect(self.delete_book)
        delete_book_layout.addWidget(self.delete_book_btn)
        delete_book_layout.addStretch()
        layout.addLayout(delete_book_layout)

        self.refresh_books_btn = QPushButton("Refresh")
        self.refresh_books_btn.clicked.connect(self.load_books)
        layout.addWidget(self.refresh_books_btn)
        
        widget.setLayout(layout)
        self.load_books()
        return widget
    
    def create_readers_tab(self):

        widget = QWidget()
        layout = QVBoxLayout()
        
        self.readers_table = QTableWidget()
        self.readers_table.setColumnCount(2)
        self.readers_table.setHorizontalHeaderLabels(["ID", "Name"])
        layout.addWidget(self.readers_table)

        add_reader_layout = QHBoxLayout()
        add_reader_layout.addWidget(QLabel("Reader name:"))
        self.reader_name_input = QLineEdit()
        add_reader_layout.addWidget(self.reader_name_input)
        
        self.add_reader_btn = QPushButton("Add Reader")
        self.add_reader_btn.clicked.connect(self.add_reader)
        add_reader_layout.addWidget(self.add_reader_btn)
        layout.addLayout(add_reader_layout)
        
        self.refresh_readers_btn = QPushButton("Refresh")
        self.refresh_readers_btn.clicked.connect(self.load_readers)
        layout.addWidget(self.refresh_readers_btn)
        
        widget.setLayout(layout)
        self.load_readers()
        return widget
    
    def create_borrows_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.borrows_table = QTableWidget()
        self.borrows_table.setColumnCount(4)
        self.borrows_table.setHorizontalHeaderLabels(["Borrow ID", "Reader", "Book", "Author"])
        self.borrows_table.setColumnWidth(2, 300)
        layout.addWidget(self.borrows_table)

        borrow_layout = QHBoxLayout()
        borrow_layout.addWidget(QLabel("Reader ID:"))
        self.borrow_reader_id_input = QLineEdit()
        self.borrow_reader_id_input.setMaximumWidth(100)
        borrow_layout.addWidget(self.borrow_reader_id_input)
        
        borrow_layout.addWidget(QLabel("Book ID:"))
        self.borrow_book_id_input = QLineEdit()
        self.borrow_book_id_input.setMaximumWidth(100)
        borrow_layout.addWidget(self.borrow_book_id_input)
        
        self.add_borrow_btn = QPushButton("Add Borrow")
        self.add_borrow_btn.clicked.connect(self.add_borrow)
        borrow_layout.addWidget(self.add_borrow_btn)
        borrow_layout.addStretch()
        layout.addLayout(borrow_layout)
        
        self.refresh_borrows_btn = QPushButton("Show Borrowed Books")
        self.refresh_borrows_btn.clicked.connect(self.load_borrows)
        layout.addWidget(self.refresh_borrows_btn)
        
        widget.setLayout(layout)
        self.load_borrows()
        return widget

    def load_books(self):
        try:
            books = self.session.query(Book).all()
            self.books_table.setRowCount(len(books))
            
            for row, book in enumerate(books):
                self.books_table.setItem(row, 0, QTableWidgetItem(str(book.id)))
                self.books_table.setItem(row, 1, QTableWidgetItem(book.title))
                self.books_table.setItem(row, 2, QTableWidgetItem(book.author))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load books: {str(e)}")
    
    def add_book(self):
        title = self.book_title_input.text().strip()
        author = self.book_author_input.text().strip()
        
        if not title or not author:
            QMessageBox.warning(self, "Warning", "Please fill in title and author")
            return
        
        try:
            new_book = Book(title=title, author=author)
            self.session.add(new_book)
            self.session.commit()
            
            QMessageBox.information(self, "Success", f"Book '{title}' added successfully!")
            self.book_title_input.clear()
            self.book_author_input.clear()
            self.load_books()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to add book: {str(e)}")
    
    def delete_book(self):
        book_id = self.delete_book_id_input.text().strip()
        
        if not book_id:
            QMessageBox.warning(self, "Warning", "Please enter book ID")
            return
        
        try:
            book_id = int(book_id)
            book = self.session.query(Book).filter(Book.id == book_id).first()
            
            if not book:
                QMessageBox.warning(self, "Warning", f"Book with ID {book_id} not found")
                return
            
            self.session.delete(book)
            self.session.commit()
            
            QMessageBox.information(self, "Success", f"Book with ID {book_id} deleted successfully!")
            self.delete_book_id_input.clear()
            self.load_books()
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter a valid book ID (number)")
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to delete book: {str(e)}")
    
    def search_books(self):
        search_text = self.search_book_input.text().strip()
        
        if not search_text:
            self.load_books()
            return
        
        try:
            books = self.session.query(Book).filter(Book.title.contains(search_text)).all()
            self.books_table.setRowCount(len(books))
            
            if not books:
                QMessageBox.information(self, "Search", "No books found")
                return
            
            for row, book in enumerate(books):
                self.books_table.setItem(row, 0, QTableWidgetItem(str(book.id)))
                self.books_table.setItem(row, 1, QTableWidgetItem(book.title))
                self.books_table.setItem(row, 2, QTableWidgetItem(book.author))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to search books: {str(e)}")
    
    def load_readers(self):
        try:
            readers = self.session.query(Reader).all()
            self.readers_table.setRowCount(len(readers))
            
            for row, reader in enumerate(readers):
                self.readers_table.setItem(row, 0, QTableWidgetItem(str(reader.id)))
                self.readers_table.setItem(row, 1, QTableWidgetItem(reader.name))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load readers: {str(e)}")
    
    def add_reader(self):
        name = self.reader_name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter reader name")
            return
        
        try:
            new_reader = Reader(name=name)
            self.session.add(new_reader)
            self.session.commit()
            
            QMessageBox.information(self, "Success", f"Reader '{name}' added successfully!")
            self.reader_name_input.clear()
            self.load_readers()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to add reader: {str(e)}")
    
    def load_borrows(self):
        try:
            borrows = self.session.query(Borrow).all()
            self.borrows_table.setRowCount(len(borrows))
            
            for row, borrow in enumerate(borrows):
                self.borrows_table.setItem(row, 0, QTableWidgetItem(str(borrow.id)))
                self.borrows_table.setItem(row, 1, QTableWidgetItem(borrow.reader.name))
                self.borrows_table.setItem(row, 2, QTableWidgetItem(borrow.book.title))
                self.borrows_table.setItem(row, 3, QTableWidgetItem(borrow.book.author))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load borrows: {str(e)}")
    
    def add_borrow(self):
        reader_id_str = self.borrow_reader_id_input.text().strip()
        book_id_str = self.borrow_book_id_input.text().strip()
        
        if not reader_id_str or not book_id_str:
            QMessageBox.warning(self, "Warning", "Please enter both reader ID and book ID")
            return
        
        try:
            reader_id = int(reader_id_str)
            book_id = int(book_id_str)
            
            reader = self.session.query(Reader).filter(Reader.id == reader_id).first()
            book = self.session.query(Book).filter(Book.id == book_id).first()
            
            if not reader:
                QMessageBox.warning(self, "Warning", f"Reader with ID {reader_id} not found")
                return
            
            if not book:
                QMessageBox.warning(self, "Warning", f"Book with ID {book_id} not found")
                return
            
            borrow = Borrow(reader_id=reader_id, book_id=book_id)
            self.session.add(borrow)
            self.session.commit()
            
            QMessageBox.information(
                self, 
                "Success", 
                f"Borrow added: '{reader.name}' borrowed '{book.title}'"
            )
            self.borrow_reader_id_input.clear()
            self.borrow_book_id_input.clear()
            self.load_borrows()
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter valid IDs (numbers)")
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to add borrow: {str(e)}")
    
    def closeEvent(self, event):
        self.session.close()
        event.accept()
