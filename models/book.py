class Book:
    def __init__(self, book_id, title, author, available=True):
        self.id = book_id
        self.title = title
        self.author = author
        self.available = bool(available)

    def __repr__(self):
        return f"[{self.id}] {self.title} by {self.author} ({'Available' if self.available else 'Borrowed'})"
