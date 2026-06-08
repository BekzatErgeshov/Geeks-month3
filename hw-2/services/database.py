import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_path="notes.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Инициализация БД и создание таблицы заметок"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def add_note(self, text):
        """Добавить заметку в БД"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO notes (text) VALUES (?)",
                    (text,)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_notes(self):
        """Получить все заметки из БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT text FROM notes ORDER BY created_at DESC")
            notes = [row[0] for row in cursor.fetchall()]
            return notes
    
    def delete_note(self, text):
        """Удалить заметку из БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE text = ?", (text,))
            conn.commit()
    
    def clear_all(self):
        """Очистить все заметки"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes")
            conn.commit()
