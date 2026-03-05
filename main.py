from fastapi import FastAPI
from pydantic import BaseModel
from borrowBook import *
import uvicorn

app = FastAPI()
library = Library()

# ------------------ FAKE DATA ------------------

member1 = Member(1, "Ton", "M001", 10)
member2 = Member(2, "Len", "M002", 5)
member3 = Member(3, "Aug", "M003", 0)
walkin = Walkin(4, "Sun")

book1 = Book("101", "Python", "Me", 250, BookType.GENERAL)
book2 = Book("102", "Diagram", "TN", 300, BookType.PREMIUM)
book3 = Book("103", "OOP", "Haha", 400, BookType.PREMIUM)
book4 = Book("104", "Thailand", "OLALALLA", 200, BookType.GENERAL)

item1 = BookItem("B001", book1)
item1_2 = BookItem("B001-2", book1)
item2 = BookItem("B002", book2)
item3 = BookItem("B003", book3)
item4 = BookItem("B004", book4)

book1.bookitem.append(item1)
book1.bookitem.append(item1_2)
book2.bookitem.append(item2)
book3.bookitem.append(item3)
book4.bookitem.append(item4)

library.User.extend([member1, member2, member3, walkin])
library.Book.extend([book1, book2, book3, book4])

@app.post("/borrow")
def borrow(user_id: int, book_isbn: str):

    success, result = library.requestBorrow(
        user_id, 
        book_isbn
    )

    if not success:
        return {"error": result}

    return result.to_dict()

@app.get("/lendings")
def get_lendings():
    return [lending.to_dict() for lending in library.Lending]

@app.get("/lendings/{user_id}")
def get_user_lendings(user_id: int):

    user = library.findUser(user_id)
    if not user:
        return {"error": "USER NOT FOUND"}

    user_lendings = [
        l.to_dict()
        for l in library.Lending
        if l.user.id == user_id
    ]

    return user_lendings


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
