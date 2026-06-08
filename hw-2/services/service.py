from services.database import Database


class NotesService:
    def __init__(self, db_path="notes.db"):
        self.db = Database(db_path)

    def add_note(self, text):
        if text.strip():
            return self.db.add_note(text)
        return False

    def get_notes(self):
        return self.db.get_notes()

    def delete_note(self, text):
        self.db.delete_note(text)