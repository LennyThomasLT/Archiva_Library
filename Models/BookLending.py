from datetime import datetime
from Models.User import Member

class BookLending:
    def __init__(self, id, user, bookitem, price, issueDate, dueDate, returnDate, status):
        self.__id = id
        self.__user = user
        self.__bookitem = bookitem
        self.__price = price
        self.__issueDate = issueDate
        self.__dueDate = dueDate
        self.__returnDate = returnDate
        self.__status = status
        self.__payment_status = "UNPAID"
        self.__fine_status = "UNPAID"
        self.__fine_amount = 0 

    @property
    def id(self):
        return self.__id

    @property
    def user(self):
        return self.__user

    @property
    def bookitem(self):
        return self.__bookitem

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def returnDate(self):
        return self.__returnDate
    
    @returnDate.setter
    def returnDate(self, value):
        self.__returnDate = value
    
    @property
    def price(self):
        return self.__price

    @property
    def issueDate(self):
        return self.__issueDate

    @property
    def dueDate(self):
        return self.__dueDate
    
    @dueDate.setter
    def dueDate(self, value):
        self.__dueDate = value

    @property
    def payment_status(self):
        return self.__payment_status

    @payment_status.setter
    def payment_status(self, value):
        self.__payment_status = value

    @property
    def fine_status(self):
        return self.__fine_status

    @fine_status.setter
    def fine_status(self, value):
        self.__fine_status = value

    @property
    def fine_amount(self):
        return self.__fine_amount

    @fine_amount.setter
    def fine_amount(self, value):
        self.__fine_amount = value

    def getUser(self):
        return self.__user

    def getStatus(self):
        return self.__status

    def setStatus(self, status):
        self.__status = status
        
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
            "returnDate": str(self.returnDate) if self.returnDate else None,
            "status": self.status,
            "payment_status": self.payment_status,
            "fine_status": self.fine_status,
            "fine": self.fine_amount,
            "member_score": self.user.score if isinstance(self.user, Member) else None
        }