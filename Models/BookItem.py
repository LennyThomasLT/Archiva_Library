class BookItem:
    def __init__(self, barcode, book):
        self.__barcode = barcode
        self.__book = book
        self.__status = True
        self.__rack = None
        self.__deleted = False

    @property
    def barcode(self):
        return self.__barcode

    @property
    def book(self):
        return self.__book

    @book.setter
    def book(self, value):
        self.__book = value

    @property
    def rack(self):
        return self.__rack

    @rack.setter
    def rack(self, value):
        self.__rack = value

    @property
    def deleted(self):
        return self.__deleted

    @deleted.setter
    def deleted(self, value):
        self.__deleted = value
        
    def checkAvailable(self):
        return self.__status

    def bookBorrowed(self):
        self.__status = False

    def bookReturned(self):
        self.__status = True