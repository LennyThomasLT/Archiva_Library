class BookLending:
    def __init__(self, id, user, bookitem, price, issueDate, dueDate, returnDate, status):
        self.id = id
        self.user = user
        self.bookitem = bookitem
        self.price = price
        self.issueDate = issueDate
        self.dueDate = dueDate
        self.returnDate = returnDate
        self.status = status

    def to_dict(self):

        return {
            "lendingID": self.id,
            "user": self.user.name,
            "barcode": self.bookitem.barcode,
            "price": self.price,
            "issueDate": str(self.issueDate),
            "dueDate": str(self.dueDate),
            "returnDate": str(self.returnDate),
            "status": self.status
        }