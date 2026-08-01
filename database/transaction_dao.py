from .db_config import get_connection
from src.models.transaction import Transaction

class TransactionDAO:
    def add_transaction(self, book_id, member_id, borrow_date, return_date=None):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO transactions (book_id, member_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)", (book_id, member_id, borrow_date, return_date))
        conn.commit()
        conn.close()

    def update_return(self, transaction_id, return_date):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE transactions SET return_date=%s WHERE id=%s", (return_date, transaction_id))
        conn.commit()
        conn.close()

    def get_all_transactions(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, book_id, member_id, borrow_date, return_date FROM transactions")
        rows = cur.fetchall()
        conn.close()
        return [Transaction(*row) for row in rows]

    def get_by_id(self, transaction_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, book_id, member_id, borrow_date, return_date FROM transactions WHERE id=%s", (transaction_id,))
        row = cur.fetchone()
        conn.close()
        return Transaction(*row) if row else None
