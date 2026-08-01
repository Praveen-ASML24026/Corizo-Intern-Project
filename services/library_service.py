from src.database.book_dao import BookDAO
from src.database.member_dao import MemberDAO
from src.database.transaction_dao import TransactionDAO
from src.dsa.hash_map import HashMap
from src.dsa.linked_list import LinkedList
from src.dsa.stack import Stack
from src.dsa.queue import Queue
from datetime import datetime
from prettytable import PrettyTable

class LibraryService:
    def __init__(self):
        self.book_dao = BookDAO()
        self.member_dao = MemberDAO()
        self.trans_dao = TransactionDAO()
        self.books_map = HashMap()
        self.activity_log = LinkedList(limit=50)
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.borrow_queue = Queue()
        self.sync_books()
        self.sync_members()

    def sync_books(self):
        books = self.book_dao.get_all_books()
        for book in books:
            self.books_map.put(book.id, book)

    def sync_members(self):
        members = self.member_dao.get_all_members()
        self.members_map = HashMap()
        for m in members:
            self.members_map.put(m.id, m)

    def add_book(self, title, author):
        self.book_dao.add_book(title, author)
        self.activity_log.add_first(f"Added book '{title}'")
        self.undo_stack.push(("ADD_BOOK", title, author))
        self.sync_books()
        print(f"Book '{title}' added successfully!")

    def show_books(self):
        books = self.book_dao.get_all_books()
        table = PrettyTable()
        table.field_names = ["ID","Title","Author","Available"]
        for b in books:
            table.add_row([b.id, b.title, b.author, b.available])
        print(table)

    def add_member(self, name, email):
        self.member_dao.add_member(name, email)
        self.activity_log.add_first(f"Added member '{name}'")
        self.undo_stack.push(("ADD_MEMBER", name, email))
        self.sync_members()
        print(f"Member '{name}' added successfully!")

    def show_members(self):
        members = self.member_dao.get_all_members()
        table = PrettyTable()
        table.field_names = ["ID","Name","Email"]
        for m in members:
            table.add_row([m.id, m.name, m.email])
        print(table)

    def request_borrow(self, book_id, member_id):
        # queue the request
        self.borrow_queue.enqueue((book_id, member_id))
        self.activity_log.add_first(f"Borrow requested: Book {book_id} by Member {member_id}")
        print("Borrow request queued. Processing...")
        self.process_borrow_queue()

    def process_borrow_queue(self):
        while not self.borrow_queue.is_empty():
            book_id, member_id = self.borrow_queue.dequeue()
            book = self.book_dao.get_by_id(book_id)
            member = self.member_dao.get_by_id(member_id)
            if not book:
                print(f"Book id {book_id} not found.")
                continue
            if not member:
                print(f"Member id {member_id} not found.")
                continue
            if not book.available:
                print(f"Book id {book_id} is not available.")
                continue
            # mark unavailable and add transaction
            self.book_dao.update_availability(book_id, False)
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.trans_dao.add_transaction(book_id, member_id, now, None)
            self.activity_log.add_first(f"Book {book_id} borrowed by Member {member_id}")
            self.undo_stack.push(("BORROW", book_id))
            self.sync_books()
            print(f"Book {book_id} borrowed by Member {member_id} at {now}")

    def return_book(self, transaction_id):
        trans = self.trans_dao.get_by_id(transaction_id)
        if not trans:
            print("Transaction not found.")
            return
        if trans.return_date:
            print("Book already returned.")
            return
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.trans_dao.update_return(transaction_id, now)
        self.book_dao.update_availability(trans.book_id, True)
        self.activity_log.add_first(f"Book {trans.book_id} returned (T{transaction_id})")
        self.undo_stack.push(("RETURN", transaction_id))
        self.sync_books()
        print(f"Transaction {transaction_id} returned at {now}")

    def print_activity(self):
        self.activity_log.print_all()

    def undo(self):
        if self.undo_stack.is_empty():
            print("Nothing to undo.")
            return
        op = self.undo_stack.pop()
        self.redo_stack.push(op)
        typ = op[0]
        if typ == "ADD_BOOK":
            # best-effort: remove last matching book by title
            title = op[1]
            # naive removal, search and delete first match
            books = self.book_dao.get_all_books()
            for b in books:
                if b.title == title:
                    # remove via SQL by id
                    conn = None
                    from src.database.db_config import get_connection
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM books WHERE id=%s", (b.id,))
                    conn.commit()
                    conn.close()
                    self.activity_log.add_first(f"UNDO: removed book '{title}'")
                    self.sync_books()
                    print(f"Undo: removed book '{title}'")
                    return
            print("Undo failed: book not found.")
        elif typ == "BORROW":
            book_id = op[1]
            # find latest transaction for that book without return_date
            trans = None
            for t in self.trans_dao.get_all_transactions()[::-1]:
                if t.book_id == book_id and not t.return_date:
                    trans = t
                    break
            if trans:
                self.trans_dao.update_return(trans.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.book_dao.update_availability(book_id, True)
                self.activity_log.add_first(f"UNDO: borrow for book {book_id}")
                self.sync_books()
                print(f"Undo borrow for book {book_id}")
            else:
                print("Undo failed: transaction not found.")
        elif typ == "RETURN":
            trans_id = op[1]
            # can't easily un-return without archived data; just notify
            print("Undo for RETURN is not supported in this simple demo.")

    def redo(self):
        if self.redo_stack.is_empty():
            print("Nothing to redo.")
            return
        op = self.redo_stack.pop()
        typ = op[0]
        # very basic redo: reapply ADD_BOOK or BORROW by re-calling methods
        if typ == "ADD_BOOK":
            _, title, author = op
            self.add_book(title, author)
            print("Redo: added book.")
        elif typ == "BORROW":
            book_id = op[1]
            # can't know member id here; inform user
            print("Redo for BORROW requires member context; skipping.")

    def generate_reports(self):
        trans = self.trans_dao.get_all_transactions()
        borrow_count = {}
        for t in trans:
            borrow_count[t.book_id] = borrow_count.get(t.book_id, 0) + 1
        # sort by count desc
        sorted_books = sorted(borrow_count.items(), key=lambda x: x[1], reverse=True)
        table = PrettyTable()
        table.field_names = ["Book ID","Borrow Count"]
        for bid, cnt in sorted_books:
            table.add_row([bid, cnt])
        print("Most borrowed books:")
        print(table)
