class Transaction:
    def __init__(self, trans_id, book_id, member_id, borrow_date, return_date):
        self.id = trans_id
        self.book_id = book_id
        self.member_id = member_id
        self.borrow_date = borrow_date
        self.return_date = return_date

    def __repr__(self):
        return f"[T{self.id}] Book:{self.book_id} Member:{self.member_id} Borrowed:{self.borrow_date} Returned:{self.return_date}"
