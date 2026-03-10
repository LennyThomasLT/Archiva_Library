from enum import Enum
from Models.BookItem import BookItem


class BookType(Enum):
    GENERAL = "GENERAL"
    PREMIUM = "PREMIUM"


class Book:
    def __init__(self, isbn, title, author, price, booktype):
        self.__isbn = isbn
        self.__title = title
        self.__author = author
        self.__price = price
        self.__booktype = booktype
        self.__bookitems = []
        self.__reservations = []
        self.__deleted = False

    @property
    def isbn(self):
        return self.__isbn

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, value):
        self.__title = value
    
    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, value):
        self.__author = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value

    @property
    def booktype(self):
        return self.__booktype
    
    @booktype.setter
    def booktype(self, value):
        self.__booktype = value

    @property
    def bookitems(self):
        return self.__bookitems

    @property
    def reservations(self):
        return self.__reservations

    @property
    def deleted(self):
        return self.__deleted

    @deleted.setter
    def deleted(self, value):
        self.__deleted = value

    def addBookItem(self, barcode):
        item = BookItem(barcode, self)
        self.__bookitems.append(item)
        return item

    def getAvailableItem(self):
        for item in self.bookitems:
            if item.checkAvailable() and not item.deleted and item.rack is not None:
                return item
        return None

    def getAvailableAmount(self):
        count = 0
        for item in self.bookitems:
            if item.checkAvailable() and not item.deleted:
                count += 1
        return count