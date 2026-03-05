class SearchResult:
    def __init__(self, book, location, available_count):
        self.id = book.isbn
        self.title = book.title
        self.author = book.author
        self.price = book.price
        self.book_type = book.booktype
        self.location = location
        self.available_amount = available_count

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "book_type": self.book_type,
            "location": self.location,
            "available_amount": self.available_amount
        }