from enum import Enum

class BookType(Enum):
    GENERAL = "GENERAL"
    PREMIUM = "PREMIUM"


class Book:
    def __init__(self, isbn, title, author, price, booktype):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
        self.booktype = booktype
        self.bookitems = []

    def getBookType(self):
        return self.booktype

    def getAvailableItem(self):
        for item in self.bookitems:
            if item.checkAvailable():
                return item
        return None

    def getAvailableAmount(self):
        count = 0
        for item in self.bookitems:
            if item.checkAvailable():
                count += 1
        return count
    