from datetime import datetime, timedelta

class ReservationStatus:
    WAITING = "WAITING"
    READY = "READY"
    FULFILLED = "FULFILLED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class BookReservation:
    def __init__(self, id, user, book):
        self.id = id
        self.user = user
        self.book = book
        self.reservationDate = datetime.now()
        self.expireDate = None
        self.status = ReservationStatus.WAITING

    def mark_ready(self):
        self.status = ReservationStatus.READY
        self.expireDate = datetime.now() + timedelta(hours=24)

    def is_expired(self):
        if self.status != ReservationStatus.READY:
            return False
        return datetime.now() > self.expireDate
    
