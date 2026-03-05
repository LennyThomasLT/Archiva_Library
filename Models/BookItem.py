class BookItem:
    def __init__(self, barcode, book):
        self.barcode = barcode
        self.book = book
        self.status = True

    def checkAvailable(self):
        return self.status

    def bookBorrowed(self):
        self.status = False

    def bookReturned(self):
        self.status = True

    