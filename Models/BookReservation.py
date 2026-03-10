from datetime import datetime, timedelta

class ReservationStatus:
    WAITING = "WAITING"
    READY = "READY"
    FULFILLED = "FULFILLED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"

class BookReservation:
    def __init__(self, id, user, book):
        self.__id = id
        self.__user = user
        self.__book = book
        self.__reservationDate = datetime.now()
        self.__expireDate = None
        self.__status = ReservationStatus.WAITING
        self.__deposit_paid = False
        self.__deposit_amount = 0

    @property
    def id(self):
        return self.__id

    @property
    def user(self):
        return self.__user

    @property
    def book(self):
        return self.__book
    
    @property
    def reservationDate(self):
        return self.__reservationDate

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def expireDate(self):
        return self.__expireDate

    @expireDate.setter
    def expireDate(self, expire_date):
        self.__expireDate = expire_date

    @property
    def deposit_paid(self):
        return self.__deposit_paid

    @property
    def deposit_amount(self):
        return self.__deposit_amount

    def set_deposit(self, amount):
        self.__deposit_paid = True
        self.__deposit_amount = amount

    def mark_ready(self):
        self.__status = ReservationStatus.READY
        self.__expireDate = datetime.now() + timedelta(hours=24)

    def is_expired(self):
        if self.__status != ReservationStatus.READY:
            return False

        if self.__expireDate is None:
            return False

        return datetime.now() > self.__expireDate
    
    def to_dict(self):
        return {
            "reservation_id": self.id,
            "book": self.book.title,
            "isbn": self.book.isbn,
            "status": self.status,
            "reserved_at": str(self.reservationDate),
            "expire_at": str(self.expireDate) if self.expireDate else None,
            "deposit": self.deposit_amount
        }