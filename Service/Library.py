from datetime import datetime, timedelta

from Models.Book import BookType, Book
from Models.BookLending import BookLending
from Models.BookRack import BookRack
from Models.SearchResult import SearchResult
from Models.User import Member, NormalUser, Worker, SystemAdmin


class Library:

    def __init__(self):
        self.books = []
        self.racks = []
        self.users = []
        self.lendings = []

    # ---------------- VALIDATION ----------------

    def validate_user(self, user_id):

        for user in self.users:
            if user.id == user_id:
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
            if book.isbn == isbn:
                return True, book

        return False, "BOOK NOT FOUND"

    def validate_book_item(self, barcode):

        for book in self.books:
            for item in book.bookitems:
                if item.barcode == barcode:
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
                return user

        return None

    # ---------------- REGISTER ----------------

    def register_user(self, name, username, password):
        for user in self.users:
            if user.username == username:
                return False, "USERNAME EXISTS"

        running = len(self.users) + 1
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

    def create_staff(self, admin_id, name, username, password, role="worker"):

        success, admin = self.validate_admin(admin_id)

        if not success:
            return False, admin

        return True, self._create_staff(name, username, password, role)

    def _create_staff(self, name, username, password, role="worker"):

        running = len(self.users) + 1
        user_id = f"6801{running:04d}"
        staff_id = f"S{running:03d}"

        if role == "admin":
            staff = SystemAdmin(user_id, name, username, password, staff_id)
        else:
            staff = Worker(user_id, name, username, password, staff_id)

        self.users.append(staff)

        return staff

    # ---------------- BOOK MANAGEMENT ----------------

    def add_book(self, worker_id, isbn, title, author, price, book_type):
        success, worker = self.validate_staff(worker_id)
        if not success:
            return False, worker
        
        for b in self.books:
            if b.isbn == isbn:
                return False, "BOOK ALREADY EXISTS"

        book = Book(isbn, title, author, price, book_type)

        self.books.append(book)

        return True, book

    def add_book_item(self, worker_id, isbn, barcode):

        success, worker = self.validate_staff(worker_id)
        if not success:
            return False, worker

        success, book = self.validate_book(isbn)
        if not success:
            return False, book

        # เช็ค barcode ซ้ำ
        for b in self.books:
            for item in b.bookitems:
                if item.barcode == barcode:
                    return False, "BARCODE EXISTS"

        item = book.addBookItem(barcode)

        return True, item

    def add_rack(self, worker_id, floor, row):
        success, worker = self.validate_staff(worker_id)
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

    def place_book_in_rack(self, worker_id, barcode, floor, row):
        success, worker = self.validate_staff(worker_id)
        if not success:
            return False, worker

        success, item = self.validate_book_item(barcode)
        if not success:
            return False, item

        success, rack = self.validate_rack(floor, row)
        if not success:
            return False, rack

        for r in self.racks:
            if item in r.items:
                return False, "BOOK ITEM ALREADY PLACED"

        rack.add_item(item)

        return True, "BOOK PLACED"

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
                matched_books.append(book)

        results = []

        for book in matched_books:

            location = self.find_location(book)
            available = book.getAvailableAmount()

            result = SearchResult(book, location, available)

            results.append(result.to_dict())

        return results

    # ---------------- BORROW ----------------

    def countBorrowedBooks(self, user):

        count = 0

        for lending in self.lendings:
            if lending.user == user and lending.status == "BORROWED":
                count += 1

        return count

    def requestBorrow(self, user_id, isbn):

        success, user = self.validate_user(user_id)

        if not success:
            return False, user

        success, book = self.validate_book(isbn)

        if not success:
            return False, book

        if isinstance(user, Member):
            if user.getScore() <= 0:
                return False, "MEMBER BANNED"

        if book.getBookType() == BookType.PREMIUM and isinstance(user, NormalUser):
            return False, "MEMBER ONLY"

        item = book.getAvailableItem()

        if not item:
            return False, "BOOK NOT AVAILABLE"

        if self.countBorrowedBooks(user) >= user.borrowLimit():
            return False, "LIMIT REACHED"

        return True, self.createLending(user, item)

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
