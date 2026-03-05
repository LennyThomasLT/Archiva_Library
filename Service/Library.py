from datetime import datetime, timedelta

from Models.Book import BookType
from Models.BookLending import BookLending
from Models.SearchResult import SearchResult
from Models.User import Member, Walkin, Worker, SystemAdmin

class Library:
    def __init__(self):

        self.books = []
        self.racks = []
        self.users = []
        self.lendings = []

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def register_member(self, name, username, password):
        new_id = len(self.users) + 1
        member_id = f"M{new_id:03d}"
        member = Member(new_id, name, username, password, member_id, 10)
        self.users.append(member)

        return member

    def add_staff(self, name, username, password, role="worker"):
        new_id = len(self.users) + 1
        staff_id = f"S{new_id:03d}"

        if role == "admin":
            staff = SystemAdmin(new_id, name, username, password, staff_id)
        else:
            staff = Worker(new_id, name, username, password, staff_id)

        self.users.append(staff)
        return staff

    def findUser(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user

        return None

    def find_book_in_rack(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book

        return None

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

    def countBorrowedBooks(self, user):
        count = 0
        for lending in self.lendings:
            if lending.user == user and lending.status == "BORROWED":
                count += 1

        return count

    def requestBorrow(self, user_id, isbn):
        user = self.findUser(user_id)
        book = self.find_book_in_rack(isbn)

        if not user or not book:
            return False, "NOT FOUND"

        if isinstance(user, Member):
            if user.memberScore() <= 0:
                return False, "MEMBER BANNED"

        if book.getBookType() == BookType.PREMIUM and isinstance(user, Walkin):
            return False, "MEMBER ONLY"

        item = book.getAvailableItem()

        if not item:
            return False, "BOOK NOT AVAILABLE"

        if self.countBorrowedBooks(user) >= user.borrowLimit():
            return False, "LIMIT REACHED"

        return True, self.createLending(user, item)

    def createLending(self, user, item):
        issueDate = datetime.now()

        if user.getRole() == "WALKIN":
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
            "-",
            "BORROWED",
        )

        item.bookBorrowed()
        self.lendings.append(lending)
        return lending