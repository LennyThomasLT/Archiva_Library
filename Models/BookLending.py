from datetime import datetime
from Models.User import Member

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
        self.payment_status = "UNPAID"
        self.fine_status = "UNPAID"
        self.fine_amount = 0 

    def calculateFine(self):
        if datetime.now() > self.dueDate:
            days_overdue = (datetime.now() - self.dueDate).days
            return days_overdue * 10
        return 0
    
    def to_dict(self, fine=None, member_score=None):
        return {
            "lendingID": self.id,
            "user": self.user.name,
            "barcode": self.bookitem.barcode,
            "price": self.price,
            "issueDate": str(self.issueDate),
            "dueDate": str(self.dueDate),
            "returnDate": str(self.returnDate),
            "status": self.status,
            "payment_status": self.payment_status,
            "fine_status": self.fine_status,
            "fine": self.fine_amount,
            "member_score": self.user.score if isinstance(self.user, Member) else None
        }