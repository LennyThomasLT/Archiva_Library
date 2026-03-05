from fastapi import FastAPI, HTTPException
import uvicorn

from Service.Library import Library
from Models.User import Member, Walkin, Worker, SystemAdmin
from Models.Book import Book, BookType
from Models.BookItem import BookItem
from Models.BookRack import BookRack

app = FastAPI()

library = Library()

# ---------------- MOCK DATA ----------------

# ------------------ USERS ------------------

member1 = Member(1, "Ton", "ton123", "1234", "M001", 10)
member2 = Member(2, "Len", "len123", "1234", "M002", 5)
member3 = Member(3, "Aug", "aug123", "1234", "M003", 0)

walkin = Walkin(4, "Sun")

worker1 = Worker(5, "Bank", "bank123", "1234", "W001")
admin1 = SystemAdmin(6, "Boss", "boss123", "1234", "A001")

library.users.extend([member1, member2, member3, walkin, worker1, admin1])

book1 = Book("101", "Python", "OLALALLA", 250, BookType.GENERAL)
book2 = Book("102", "Diagram", "TN", 300, BookType.PREMIUM)
book3 = Book("103", "OOP", "Haha", 400, BookType.PREMIUM)
book4 = Book("104", "Thailand", "OLALALLA", 200, BookType.GENERAL)

item1 = BookItem("B001", book1)
item1_2 = BookItem("B001-2", book1)
item2 = BookItem("B002", book2)
item3 = BookItem("B003", book3)
item4 = BookItem("B004", book4)

book1.bookitems.extend([item1, item1_2])
book2.bookitems.append(item2)
book3.bookitems.append(item3)
book4.bookitems.append(item4)

library.books.extend([book1, book2, book3, book4])

rack1 = BookRack(1, "A")
rack2 = BookRack(2, "B")

rack1.add_item(item1)
rack1.add_item(item1_2)
rack1.add_item(item2)

rack2.add_item(item3)
rack2.add_item(item4)

library.racks.extend([rack1, rack2])

# ---------------- API ----------------
@app.post("/register")
def register(name: str, username: str, password: str):

    member = library.register_member(name, username, password)

    return {
        "message": "REGISTER",
        "user_id": member.id,
        "member_id": member.member_id,
        "username": member.username
    }

@app.post("/login")
def login(username: str, password: str):

    user = library.login(username, password)

    if not user:
        return {"error": "INVALID LOGIN"}

    return {
        "message": "LOGIN SUCCESS",
        "user_id": user.id,
        "role": user.getRole()
    }

@app.get("/books/search")
def search_book(keyword: str):

    result = library.find_book(keyword)

    if not result:
        raise HTTPException(status_code=404, detail="Book not found")

    return result


@app.post("/borrow")
def borrow(user_id: int, book_isbn: str):

    success, result = library.requestBorrow(user_id, book_isbn)

    if not success:
        return {"error": result}

    return result.to_dict()


@app.get("/lendings")
def get_lendings():
    return [l.to_dict() for l in library.lendings]


if __name__ == "__main__":
    uvicorn.run("API.API:app", host="127.0.0.1", port=8000, reload=True)