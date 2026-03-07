from enum import Enum
from Models.BookItem import BookItem


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
        self.reservations = []

    def getBookType(self):
        return self.booktype

    def addBookItem(self, barcode):
        item = BookItem(barcode, self)
        self.bookitems.append(item)
        return item

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