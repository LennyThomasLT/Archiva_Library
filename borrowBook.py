from enum import Enum
from datetime import datetime, timedelta

class BookType(Enum):
    GENERAL = "GENERAL"
    PREMIUM = "PREMIUM"

class User():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def borrowLimit(self):
        raise NotImplementedError()


class Member(User):
    def __init__(self, id, name, member_id, score):
        super().__init__(id, name)
        self.member_id = member_id
        self.score = score

    def borrowLimit(self):
        return 5
    
    def memberScore(self):
        return self.score

class Walkin(User):
    def borrowLimit(self):
        return 1


class Book():
    def __init__(self, isbn, title, author, price, booktype):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
        self.booktype = booktype
        self.bookitem = []
    
    def getBookType(self):
        return self.booktype
    
    def getAvailableItem(self):
        for item in self.bookitem:
            if item.checkAvailable():
                return item
        return None


class BookItem():
    def __init__(self, barcode, book):
        self.barcode = barcode
        self.status = True
        self.book = book

    def checkAvailable(self):
        return self.status
    
    def bookBorrowed(self):
        self.status = False

    def bookReturned(self):
        self.status = True


class BookLending():
    def __init__(self, id, user, bookitem, price, issueDate, dueDate, returnDate, status):
        self.id = id
        self.user = user
        self.bookitem = bookitem
        self.price = price
        self.issueDate = issueDate
        self.dueDate = dueDate
        self.returnDate = returnDate
        self.status = status

    # def __str__(self):
    #     return (
    #         f"{self.user.name}, "
    #         f"{self.bookitem.barcode}, "
    #         f"{self.id}, "
    #         f"{self.issueDate}, "
    #         f"{self.dueDate}, "
    #         f"{self.returnDate}, "
    #         f"{self.status})"
    #     )

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


class Library():
    def __init__(self):
        self.Lending = []
        self.User = []
        self.Book = []
    
    def findUser(self, user_id):
        for user in self.User:
            if user.id == user_id:
                return user
        return None

    def findBook(self, book_isbn):
        for book in self.Book:
            if book.isbn == book_isbn:
                return book
        return None

    def requestBorrow(self, user_id, book_isbn):
        user = self.findUser(user_id)
        book = self.findBook(book_isbn)

        if isinstance(user, Member):
            if user.memberScore() <= 0:
                return False, "MEMBER BANNED"

        if book.getBookType() == BookType.PREMIUM:
            if not isinstance(user, Member):
                return False, "MEMBER ONLY"

        item = book.getAvailableItem()
        if not item:
            return False, "BOOK NOT AVAILABLE"

        current = self.countBorrowedBooks(user)
        if current >= user.borrowLimit():
            return False, "LIMIT REACHED"

        lending = self.createLending(user, item)

        return True, lending
    
    def createLending(self, user, item):
        issueDate = datetime.now()
        
        if isinstance(user, Member):
            dueDate = datetime.now() + timedelta(days=7)
        else:
            dueDate = datetime.now() + timedelta(days=1)
        
        price = item.book.price
        year = issueDate.year
        running = len(self.Lending) + 1
        lending_id = f"LEN{year}{running:03d}"
        lending = BookLending(lending_id, user, item, price, issueDate, dueDate, "-", "BORROWED")
        item.bookBorrowed()
        self.Lending.append(lending)
        return lending
    
    def countBorrowedBooks(self, user):
        count = 0
        for lending in self.Lending:
            if lending.user == user and lending.status == "BORROWED":
                count += 1
        return count


 #====================TEST-FROM-GPT=========================
# print("\n========== TEST CASES ==========")

# library = Library()

# member = Member(1, "Alice", "M001", 10)
# banned_member = Member(3, "Eve", "M999", -1)
# walkin = Walkin(2, "Bob")

# # ---------- create books ----------
# book_general = Book("111", "Python Basics", "Guido", BookType.GENERAL)
# book_premium = Book("555", "Hee", "banana", BookType.PREMIUM)

# item1 = BookItem("B001", book_general)
# item2 = BookItem("B002", book_premium)

# book_general.bookitem.append(item1)
# book_premium.bookitem.append(item2)


# # =========================================================
# print("\n1) SUCCESS BORROW (member -> general)")
# success, result = library.requestBorrow(member, book_general)
# print(success, result)


# # =========================================================
# print("\n2) WALKIN BORROW PREMIUM (should fail)")
# success, result = library.requestBorrow(walkin, book_premium)
# print(success, result)


# # =========================================================
# print("\n3) BOOK NOT AVAILABLE (already borrowed)")
# success, result = library.requestBorrow(member, book_general)
# print(success, result)


# # =========================================================
# print("\n4) MEMBER BANNED")
# success, result = library.requestBorrow(banned_member, book_premium)
# print(success, result)


# # =========================================================
# print("\n5) BORROW LIMIT REACHED (walkin limit = 1)")

# # สร้างหนังสือใหม่ให้ walkin ยืมเล่มแรก
# book2 = Book("222", "Math", "Newton", BookType.GENERAL)
# item3 = BookItem("B003", book2)
# book2.bookitem.append(item3)

# success, result = library.requestBorrow(walkin, book2)
# print("first:", success, result)

# # พยายามยืมอีกเล่ม (ต้องเกิน limit)
# book3 = Book("333", "Sci", "Einstein", BookType.GENERAL)
# item4 = BookItem("B004", book3)
# book3.bookitem.append(item4)

# success, result = library.requestBorrow(walkin, book3)
# print("second:", success, result)




            
        
            




        
