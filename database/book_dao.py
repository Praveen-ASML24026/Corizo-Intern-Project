from .db_config import get_connection
from src.models.book import Book

class BookDAO:
    def add_book(self, title, author):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        conn.commit()
        conn.close()

    def get_all_books(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author, available FROM books")
        result = cur.fetchall()
        conn.close()
        return [Book(*row) for row in result]

    def search_by_title(self, title):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author, available FROM books WHERE title LIKE %s", (f"%{title}%",))
        result = cur.fetchall()
        conn.close()
        return [Book(*row) for row in result]

    def update_availability(self, book_id, available):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE books SET available=%s WHERE id=%s", (available, book_id))
        conn.commit()
        conn.close()

    def get_by_id(self, book_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author, available FROM books WHERE id=%s", (book_id,))
        row = cur.fetchone()
        conn.close()
        return Book(*row) if row else None
