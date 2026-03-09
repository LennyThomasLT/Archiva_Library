from datetime import datetime

class Payment:
    def __init__(self, id, user, amount, method, lendings, status):

        self.id = id
        self.user = user
        self.amount = amount
        self.method = method
        self.lendings = lendings
        self.status = status
        self.date = datetime.now()

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