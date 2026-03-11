from datetime import datetime, timedelta

from Models.Book import BookType, Book
from Models.BookLending import BookLending
from Models.BookRack import BookRack
from Models.SearchResult import SearchResult
from Models.User import Member, NormalUser, Worker, SystemAdmin, Staff
from Models.BookReservation import BookReservation, ReservationStatus
from Models.Room import Room
from Models.RoomReservation import RoomReservation
from Models.TimeSlot import TimeSlot
from Models.Payment import Payment
from Models.PaymentGateway import PaymentGateway
from Models.PaymentMethod import CashPayment, QRPayment, CreditCardPayment


class Library:

    def __init__(self):
        self.books = []
        self.racks = []
        self.users = []
        self.lendings = []
        self.bookreservations = []
        self.rooms = []
        self.room_reservations = []
        self.payments = []
        self.gateway = PaymentGateway()
        
    # ---------------- VALIDATION ----------------

    def validate_user(self, user_id):

        for user in self.users:
            if user.id == user_id and not user.deleted:
                return True, user

        return False, "USER NOT FOUND"

    def validate_staff(self, user_id):

        success, user = self.validate_user(user_id)

        if not success:
            return False, user

        if user.getRole() not in ["WORKER", "ADMIN"]:
            return False, "ONLY STAFF"

        return True, user

    def validate_admin(self, user_id):

        success, user = self.validate_user(user_id)

        if not success:
            return False, user

        if user.getRole() != "ADMIN":
            return False, "ONLY ADMIN"

        return True, user

    def validate_book(self, isbn):

        for book in self.books:
            if book.isbn == isbn and not book.deleted:
                return True, book

        return False, "BOOK NOT FOUND"

    def validate_book_item(self, barcode):

        for book in self.books:
            for item in book.bookitems :
                if item.barcode == barcode and not item.deleted and not book.deleted:
                    return True, item

        return False, "BOOK ITEM NOT FOUND"

    def validate_rack(self, floor, row):

        for rack in self.racks:
            if rack.floor == floor and rack.row == row:
                return True, rack

        return False, "RACK NOT FOUND"

    # ---------------- LOGIN ----------------

    def login(self, username, password):

        for user in self.users:
            if user.username == username and user.password == password:
                if user.deleted:
                    return None
                return user

        return None
    
    # ---------------- LOGOUT ----------------

    def logout(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return True, f"User {user.username} logged out successfully"

        return False, "USER NOT FOUND"

    # ---------------- REGISTER ----------------

    def register_user(self, name, username, password):
        for user in self.users:
            if user.username == username:
                return False, "USERNAME EXISTS"

        running = len([u for u in self.users if not u.deleted]) + 1
        new_id = f"6801{running:04d}"

        user = NormalUser(new_id, name, username, password)

        self.users.append(user)

        return True, user

    # ---------------- MEMBER UPGRADE ----------------

    def upgrade_member(self, user_id):

        success, user = self.validate_user(user_id)

        if not success:
            return False, user

        if not isinstance(user, NormalUser):
            return False, "ONLY NORMAL USER CAN UPGRADE"

        member_id = f"M{user.id}"

        member = Member(
            user.id,
            user.name,
            user.username,
            user.password,
            member_id,
            10
        )

        self.users.remove(user)
        self.users.append(member)

        return True, member

    # ---------------- CREATE STAFF ----------------

    def create_staff(self, name, username, password, role="worker", admin_id=None):
        if admin_id:
            success, admin = self.validate_admin(admin_id)
            if not success:
                return False, admin
        
        for user in self.users:
            if user.username == username:
                return False, "USERNAME EXISTS"

        running = len([u for u in self.users if not u.deleted]) + 1
        user_id = f"6801{running:04d}"
        staff_id = f"S{running:03d}"

        if role == "admin":
            staff = SystemAdmin(user_id, name, username, password, staff_id)
        else:
            staff = Worker(user_id, name, username, password, staff_id)

        self.users.append(staff)

        return True, staff

    # ---------------- BOOK MANAGEMENT ----------------

    def add_book(self, user_id, isbn, title, author, price, book_type):
        success, worker = self.validate_staff(user_id)
        if not success:
            return False, worker
        
        if isinstance(book_type, str):
            try:
                book_type = BookType[book_type.upper()]
            except KeyError:
                return False, "INVALID BOOK TYPE"

        for b in self.books:
            if b.isbn == isbn and not b.deleted:
                return False, "BOOK ALREADY EXISTS"
            if b.isbn == isbn and b.deleted:
                b.deleted = False
                b.title = title
                b.author = author
                b.price = price
                b.booktype = book_type
                return True, b

        book = Book(isbn, title, author, price, book_type)
        self.books.append(book)

        return True, book

    def add_book_item(self, user_id, isbn, barcode):

        success, worker = self.validate_staff(user_id)
        if not success:
            return False, worker

        success, book = self.validate_book(isbn)
        if not success:
            return False, book

        for b in self.books:
            for item in b.bookitems:
                if item.barcode == barcode:
                    if item.deleted:
                        item.deleted = False
                        item.book = book
                        return True, item

                    return False, "BARCODE EXISTS"

        item = book.addBookItem(barcode)

        return True, item

    def add_rack(self, user_id, floor, row):
        success, worker = self.validate_staff(user_id)
        if not success:
            return False, worker

        if floor <= 0:
            return False, "INVALID FLOOR"

        for rack in self.racks:
            if rack.floor == floor and rack.row == row:
                return False, "RACK ALREADY EXISTS"

        rack = BookRack(floor, row)
        self.racks.append(rack)

        return True, rack
    
    def deleteRack(self, staff_id, floor, row):
        success, staff = self.validate_staff(staff_id)
        if not success:
            return False, staff

        success, rack = self.validate_rack(floor, row)
        if not success:
            return False, rack

        for item in rack.items:
            item.rack = None

        rack.items.clear()
        self.racks.remove(rack)

        return True, "RACK DELETED"

    def place_book_in_rack(self, user_id, barcode, floor, row):
        success, worker = self.validate_staff(user_id)
        if not success:
            return False, worker

        success, item = self.validate_book_item(barcode)
        if not success:
            return False, item
        
        if item.deleted:
            return False, "BOOK ITEM REMOVED"

        success, rack = self.validate_rack(floor, row)
        if not success:
            return False, rack

        for r in self.racks:
            if item in r.items:
                return False, "BOOK ITEM ALREADY PLACED"

        rack.add_item(item)

        return True, "BOOK PLACED"
    
    def deleteBook(self, staff_id, isbn):
        success, staff = self.validate_staff(staff_id)
        if not success:
            return False, staff

        success, book = self.validate_book(isbn)
        if not success:
            return False, book

        if book.deleted:
            return False, "BOOK ALREADY DELETED"

        book.deleted = True
        for item in book.bookitems:
            item.deleted = True

        return True, "BOOK DELETED"
    
    def deleteBookItem(self, staff_id, barcode):
        success, staff = self.validate_staff(staff_id)
        if not success:
            return False, staff

        success, item = self.validate_book_item(barcode)
        if not success:
            return False, item

        if item.deleted:
            return False, "BOOK ITEM ALREADY DELETED"

        for lending in self.lendings:
            if lending.bookitem == item and lending.status == "BORROWED":
                return False, "BOOK ITEM CURRENTLY BORROWED"

        if item.rack:
            rack = item.rack
            if item in rack.items:
                rack.items.remove(item)
            item.rack = None

        item.deleted = True

        return True, "BOOK ITEM DELETED"
    
    # -----------------SHOW BOOK---------------

    def getAvailableBooks(self):
        results = []
        for book in self.books:
            if book.deleted:
                continue

            available = book.getAvailableAmount()
            if available > 0:
                location = self.find_location(book)
                results.append({
                    "isbn": book.isbn,
                    "title": book.title,
                    "available": available,
                    "location": location
                })

        return results

    # ---------------- SEARCH ----------------

    def find_location(self, book):

        for rack in self.racks:
            if rack.has_book(book):
                return rack.get_full_location()

        return "Unknown Location"

    def find_book(self, keyword):

        matched_books = []

        for book in self.books:

            k = keyword.lower()

            if (
                k in book.title.lower()
                or k in book.author.lower()
                or k in book.isbn.lower()
            ):
                if book.deleted:
                    continue
                matched_books.append(book)

        results = []

        for book in matched_books:

            location = self.find_location(book)
            available = book.getAvailableAmount()

            result = SearchResult(book, location, available)

            results.append(result.to_dict())

        return results

    #-----------------PAYMENT---------------

    def processPayment(self, user, price, payment_type, payment_data):
        if payment_type == "cash":
            payment_method = CashPayment()

        elif payment_type == "qr":
            payment_method = QRPayment()

        elif payment_type == "credit":

            if not payment_data:
                return False, "CARD INFO REQUIRED", None

            card_number = payment_data.get("card_number")
            holder = payment_data.get("holder")
            expiry = payment_data.get("expiry")
            cvv = payment_data.get("cvv")

            payment_method = CreditCardPayment(
                card_number,
                holder,
                expiry,
                cvv
            )

        else:
            return False, "INVALID PAYMENT METHOD", None

        success, message = payment_method.pay(self.gateway, price)

        if not success:
            return False, message, payment_method

        return True, "SUCCESS", payment_method


    # ---------------- BORROW ----------------

    def countBorrowedBooks(self, user):

        count = 0

        for lending in self.lendings:
            if lending.user == user and lending.status == "BORROWED":
                count += 1

        return count

    def requestBorrow(self, user_id, isbn, payment_type, payment_data=None):
        success, user = self.validate_user(user_id)
        if not success:
            return False, user

        success, book = self.validate_book(isbn)
        if not success:
            return False, book

        if isinstance(user, Member):
            if user.getScore() <= 0:
                return False, "MEMBER BANNED"

        if book.booktype == BookType.PREMIUM and isinstance(user, NormalUser):
            return False, "MEMBER ONLY"

        if book.deleted:
            return False, "BOOK REMOVED"

       # ---------------- RESERVATION CHECK ----------------

        self.expireReservations(book)
        if book.reservations:
            first = book.reservations[0]
            if first.user != user:
                return False, "BOOK RESERVED"

            if first.status == "WAITING":
                return False, "WAIT YOUR TURN"

            if first.status == "READY":
                item = book.getAvailableItem()
                if not item:
                    return False, "BOOK NOT READY"

                full_price = item.book.price * (1 - user.getDiscount())
                deposit = first.deposit_amount
                price = full_price - deposit

                success, message, payment_method = self.processPayment(
                    user, price, payment_type, payment_data
                )

                if not success:
                    return False, message

                lending = self.createLending(user, item)
                lending.payment_status = "PAID"

                pid = f"PAY{len(self.payments)+1:04d}"
                payment = Payment(pid, user, price, payment_method, [lending], "SUCCESS")
                self.payments.append(payment)

                first.status = "FULFILLED"
                book.reservations.pop(0)

                return True, lending

            else:
                return False, "WAIT YOUR TURN"

        # ---------------- NORMAL BORROW ----------------

        item = book.getAvailableItem()
        if not item:
            return False, "BOOK NOT AVAILABLE"

        if self.countBorrowedBooks(user) >= user.borrowLimit():
            return False, "LIMIT REACHED"

        price = item.book.price * (1 - user.getDiscount())

        # -------- PAYMENT --------
        success, message, payment_method = self.processPayment(
            user, price, payment_type, payment_data
        )

        if not success:
            return False, message

        lending = self.createLending(user, item)
        lending.payment_status = "PAID"

        # -------- PAYMENT RECORD --------

        pid = f"PAY{len(self.payments)+1:04d}"
        payment = Payment(pid, user, price, payment_method, [lending], "SUCCESS")
        self.payments.append(payment)

        return True, lending

    # ---------------- CREATE LENDING ----------------

    def createLending(self, user, item):
        issueDate = datetime.now()

        if isinstance(user, NormalUser):
            dueDate = issueDate + timedelta(days=1)
        else:
            dueDate = issueDate + timedelta(days=7)

        price = item.book.price * (1 - user.getDiscount())

        year = issueDate.year
        running = len(self.lendings) + 1
        lending_id = f"LEN{year}{running:03d}"

        lending = BookLending(
            lending_id,
            user,
            item,
            price,
            issueDate,
            dueDate,
            None,
            "BORROWED"
        )

        item.bookBorrowed()
        self.lendings.append(lending)

        return lending

    # ------------------Return Book-------------------

    def returnRequest(self, lendingID):
        lending = self.findLending(lendingID)
        if lending is None:
            return False, "LENDING_NOT_FOUND"

        if lending.status == "RETURNED":
            return False, "RETURN_ALREADY"

        user = lending.user
        fine = lending.calculateFine()
        lending.fine_amount = fine
        if fine > 0 and isinstance(user, Member):
            self.applyPenalty(user, fine)

        self.closeLending(lending)
        score = user.score if isinstance(user, Member) else None

        return True, lending.to_dict(fine, score)

    def findLending(self, lendingID):
        for lending in self.lendings:
            if lending.id == lendingID:
                return lending
        return None

    def applyPenalty(self, user, fine):
        user.score = max(0, user.score - fine/5)
        return None

    def closeLending(self, lending):

        lending.status = "RETURNED"
        lending.returnDate = datetime.now()
        lending.bookitem.bookReturned()

        book = lending.bookitem.book

        if book.reservations:
            first = book.reservations[0]

            if first.status == "WAITING":
                first.mark_ready()

    #-------------Book Reservation----------------

    def countActiveReservations(self, user):
        count = 0
        for r in self.bookreservations:
            if r.user == user and r.status in ["WAITING", "READY"]:
                count += 1

        return count
    
    def expireReservations(self, book):
        while book.reservations and book.reservations[0].is_expired():
            expired = book.reservations.pop(0)
            expired.status = "EXPIRED"

            for r in self.bookreservations:
                if r.id == expired.id:
                    r.status = "EXPIRED"
                    break

            if book.reservations:
                book.reservations[0].mark_ready()

    def reserveBook(self, user_id, isbn, payment_type, payment_data=None):
        success, user = self.validate_user(user_id)
        if not success:
            return False, user

        if not isinstance(user, Member):
            return False, "MEMBER ONLY"

        success, book = self.validate_book(isbn)
        if not success:
            return False, book

        if self.countActiveReservations(user) >= 5:
            return False, "RESERVATION LIMIT"

        self.expireReservations(book)

        if book.getAvailableAmount() > len(book.reservations):
            return False, "BOOK AVAILABLE NO NEED RESERVE"

        for r in book.reservations:
            if r.user == user and r.status in ["WAITING", "READY"]:
                return False, "ALREADY RESERVED"

        deposit = book.price * 0.1

        # -------- PAYMENT --------
        success, message, payment_method = self.processPayment(
            user, deposit, payment_type, payment_data
        )

        if not success:
            return False, message

        rid = f"BR{len(self.bookreservations)+1:04d}"
        reservation = BookReservation(rid, user, book)

        reservation.set_deposit(deposit)

        book.reservations.append(reservation)
        self.bookreservations.append(reservation)
        pid = f"PAY{len(self.payments)+1:04d}"
        payment = Payment(pid, user, deposit, payment_method, [reservation], "SUCCESS")
        self.payments.append(payment)

        return True, reservation

    def cancelReservation(self, reservation_id, user_id):
        for r in self.bookreservations:
            if r.id == reservation_id:
                if r.user.id != user_id:
                    return False, "NOT OWNER"

                r.status = "CANCELLED"
                if r in r.book.reservations:
                    r.book.reservations.remove(r)
                    if r.book.reservations:
                        first = r.book.reservations[0]
                        if first.status == "WAITING":
                            first.mark_ready()

                return True, "CANCELLED"

        return False, "NOT FOUND"

    def getReservationQueue(self, isbn):
        success, book = self.validate_book(isbn)
        if not success:
            return False, book

        queue = []
        position = 1
        for r in book.reservations:
            queue.append({
                "position": position,
                "reservation_id": r.id,
                "user": r.user.name,
                "status": r.status
            })
            position += 1

        return True, queue
    
#----------------RoomReservation-----------------

    def add_room(self, user_id, room_id, name, capacity, price):
        success, user = self.validate_user(user_id)
        if not success:
            return False, user

        if not isinstance(user, Staff):
            return False, "ONLY STAFF CAN ADD ROOM"

        for room in self.rooms:
            if room.room_id == room_id:

                if room.deleted:
                    room.deleted = False
                    room.name = name
                    room.capacity = capacity
                    room.clear_timeslots()
                    return True, room

                return False, "ROOM ALREADY EXISTS"

        room = Room(room_id, name, capacity, price)
        self.rooms.append(room)

        return True, room
    
    def find_room(self, room_id):
        for room in self.rooms:
            if room.room_id == room_id and not room.deleted:
                return True, room

        return False, "ROOM NOT FOUND"

    def getRooms(self):
        results = []
        for room in self.rooms:
            if room.deleted:
                continue

            results.append({
                "room_id": room.room_id,
                "name": room.name,
                "capacity": room.capacity,
                "price": room.price
            })

        return results
    
    def deleteRoom(self, staff_id, room_id):
        success, staff = self.validate_staff(staff_id)
        if not success:
            return False, staff

        success, room = self.find_room(room_id)
        if not success:
            return False, room

        room.deleted = True
        room.clear_timeslots()

        return True, "ROOM DELETED"
    
    def requestRoomReservation(self, user_id, room_id, reserve_date, slot_time, people, payment_type, payment_data=None):
        try:
            if isinstance(reserve_date, str):
                reserve_date = datetime.strptime(reserve_date, "%Y-%m-%d")
        except:
            return False, "INVALID DATE FORMAT"

        success, user = self.validate_user(user_id)
        if not success:
            return False, user

        if not isinstance(user, Member):
            return False, "MEMBER ONLY"

        success, room = self.find_room(room_id)
        if not success:
            return False, room
        
        if room.deleted:
            return False, "ROOM REMOVED"

        slot_id = TimeSlot.get_slot_id(slot_time)
        if slot_id is None:
            return False, "INVALID SLOT TIME"

        if room.over_capacity(people):
            return False, "ROOM CAPACITY NOT ENOUGH"

        now = datetime.now()
        today = now.date()
        reserve_day = reserve_date.date()

        if reserve_day < today:
            return False, "CANNOT RESERVE IN THE PAST"

        if reserve_day > today + timedelta(days=7):
            return False, "CAN BOOK ONLY WITHIN 7 DAYS"

        if reserve_day == today:
            slot_time = TimeSlot.SLOT_TIMES[slot_id]
            start_hour = int(slot_time.split("-")[0].split(".")[0])

            if start_hour <= now.hour:
                return False, "TIMESLOT ALREADY PASSED"

        for r in self.room_reservations:
            if r.user == user and r.date == reserve_date and r.timeslot.slot_id == slot_id:
                return False, "USER ALREADY RESERVED THIS SLOT"
            
        count = 0
        for r in self.room_reservations:
            if r.user == user and r.date.date() == reserve_day:
                count += 1
        if count >= 5:
            return False, "MAX 5 RESERVATIONS PER DAY"
        
        timeslot = room.reserve_timeslot(reserve_date, slot_id)
        if not timeslot:
            return False, "SLOT ALREADY RESERVED"

        price = room.price * (1 - user.getDiscount())

        success, message, payment_method = self.processPayment(
            user, price, payment_type, payment_data
        )

        if not success:
            return False, message

        rid = f"RR{len(self.room_reservations)+1:04d}"
        reservation = RoomReservation(rid, user, room, reserve_date, timeslot)
        reservation.payment_status = "PAID"
        self.room_reservations.append(reservation)
        pid = f"PAY{len(self.payments)+1:04d}"

        payment = Payment(
            pid,
            user,
            price,
            payment_method,
            [reservation],
            "SUCCESS"
        )

        self.payments.append(payment)

        return True, reservation
        
    def cancelRoomReservation(self, reservation_id, user_id):
        success, user = self.validate_user(user_id)
        if not success:
            return False, user

        for r in self.room_reservations:
            if r.id == reservation_id:
                if r.user.id != user_id:
                    return False, "NOT OWNER"
                
                r.room.remove_timeslot(r.timeslot)
                self.room_reservations.remove(r)
                return True, "CANCEL SUCCESS"

        return False, "RESERVATION NOT FOUND"
    
    #---------------------DELETE USER-----------------------

    def deleteUser(self, admin_id, user_id):
        success, admin = self.validate_admin(admin_id)
        if not success:
            return False, admin

        success, user = self.validate_user(user_id)
        if not success:
            return False, user

        if user.deleted:
            return False, "USER ALREADY DELETED"

        for l in self.lendings:
            if l.user == user and l.status == "BORROWED":
                return False, "USER STILL BORROWING"

        user.deleted = True

        return True, "USER DELETED"
    
    #---------------------Pay Fine----------------------
    
    def payFine(self, lending_id, payment_type, payment_data=None):
        lending = self.findLending(lending_id)
        if not lending:
            return False, "LENDING NOT FOUND"

        if lending.fine_status == "PAID":
            return False, "FINE ALREADY PAID"

        fine = lending.fine_amount
        if fine <= 0:
            lending.fine_status = "PAID"
            return False, "NO FINE"

        # -------- PAYMENT --------
        success, message, payment_method = self.processPayment(
            lending.user, fine, payment_type, payment_data
        )

        pid = f"PAY{len(self.payments)+1:04d}"

        if not success:
            payment = Payment(pid, lending.user, fine, payment_method, [lending], "FAILED")
            self.payments.append(payment)
            return False, message

        lending.fine_status = "PAID"

        payment = Payment(pid, lending.user, fine, payment_method, [lending], "SUCCESS")
        self.payments.append(payment)

        return True, payment