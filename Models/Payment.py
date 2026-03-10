from datetime import datetime

class Payment:
    def __init__(self, id, user, amount, method, lendings, status):

        self.__id = id
        self.__user = user
        self.__amount = amount
        self.__method = method
        self.__lendings = lendings
        self.__status = status
        self.__date = datetime.now()

    @property
    def id(self):
        return self.__id
    
    @property
    def user(self):
        return self.__user
    
    @property
    def amount(self):
        return self.__amount
    
    @property
    def method(self):
        return self.__method

    @property
    def lendings(self):
        return self.__lendings
    
    @property
    def status(self):
        return self.__status
    
    @property
    def date(self):
        return self.__date
    
    def to_dict(self):
        return {
            "payment_id": self.id,
            "user": self.user.name,
            "amount": self.amount,
            "method": type(self.method).__name__,
            "status": self.status,
            "lendings": [l.id for l in self.lendings],
            "date": str(self.date)
        }