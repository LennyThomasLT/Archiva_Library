from fastapi import FastAPI, HTTPException
import uvicorn

from Service.Library import Library
from Models.Book import BookType
from datetime import datetime
from Models.TimeSlot import TimeSlot
from Models.BookLending import BookLending

app = FastAPI()

library = Library()

# ---------------- MOCK DATA ----------------

# -------- USERS --------

success, u1 = library.register_user("Alice", "alice", "1234") #68010001
success, u2 = library.register_user("Bob", "bob", "1234") # 68010002

success, m1 = library.upgrade_member(u1.id)
success, m2 = library.upgrade_member(u2.id)

success, n1 = library.register_user("Charlie", "charlie", "1234") #68010003
success, n2 = library.register_user("David", "david", "1234") #68010004

success, admin = library.create_staff("Admin", "admin", "admin123", "admin") #68010005
success, worker = library.create_staff("Worker", "worker", "worker123", "worker") #68010006


# -------- BOOKS --------

success, b1 = library.add_book(
    worker.id,
    "101",
    "Python Basics",
    "John Smith",
    100,
    BookType.GENERAL
)

success, b2 = library.add_book(
    worker.id,
    "102",
    "FastAPI Guide",
    "Jane Doe",
    120,
    BookType.GENERAL
)

success, b3 = library.add_book(
    worker.id,
    "103",
    "Advanced AI",
    "Elon Data",
    200,
    BookType.PREMIUM
)

success, b4 = library.add_book(
    worker.id,
    "104",
    "Machine Learning Pro",
    "Andrew Data",
    250,
    BookType.PREMIUM
)


# -------- BOOK ITEMS --------

library.add_book_item(worker.id, "101", "BC001")
library.add_book_item(worker.id, "102", "BC002")
library.add_book_item(worker.id, "103", "BC003")
library.add_book_item(worker.id, "104", "BC004")


# -------- RACK --------

success, rack = library.add_rack(worker.id, 1, "A")


# -------- PLACE BOOKS IN RACK --------

library.place_book_in_rack(worker.id, "BC001", 1, "A")
library.place_book_in_rack(worker.id, "BC002", 1, "A")
library.place_book_in_rack(worker.id, "BC003", 1, "A")
library.place_book_in_rack(worker.id, "BC004", 1, "A")

#--------- Add Room ----------

library.add_room(worker.id, "R001", "ECC-811", 20, 100)
library.add_room(worker.id, "R002", "ECC-812", 50, 150)
library.add_room(worker.id, "R003", "ECC-813", 100, 200)

#---------------- LENDING -------------------

# l1 = BookLending(
#     "LEN2026001",
#     m1,
#     b1.bookitems[0],
#     90,
#     datetime(2026,3,1),
#     datetime(2026,3,3),
#     None,
#     "BORROWED"
# )

# l2 = BookLending(
#     "LEN2026002",
#     n1,
#     b2.bookitems[0],
#     120,
#     datetime(2026,3,5),
#     datetime(2026,3,6),
#     None,
#     "BORROWED"
# )

# library.lendings.append(l1)
# library.lendings.append(l2)

# ---------------- REGISTER ----------------

@app.post("/register")
def register(name: str, username: str, password: str):

    success, result = library.register_user(name, username, password)

    if not success:
        raise HTTPException(status_code=400, detail=result)

    return {
        "message": "REGISTER SUCCESS",
        "user_id": result.id
    }


# ---------------- LOGIN ----------------

@app.post("/login")
def login(username: str, password: str):

    user = library.login(username, password)

    if not user:
        raise HTTPException(401, "INVALID LOGIN")

    return {
        "message": "LOGIN SUCCESS",
        "user_id": user.id,
        "role": user.getRole()
    }


# ---------------- UPGRADE MEMBER ----------------

@app.post("/upgrade_member")
def upgrade_member(user_id: str):

    success, result = library.upgrade_member(user_id)

    if not success:
        return {"error": result}

    return {
        "message": "UPGRADED",
        "member_id": result.member_id
    }


# ---------------- ADD BOOK ----------------

@app.post("/books")
def add_book(worker_id: str, isbn: str, title: str, author: str, price: float, book_type: str):

    success, result = library.add_book(
        worker_id,
        isbn,
        title,
        author,
        price,
        book_type
    )

    if not success:
        return {"error": result}

    return {"message": "BOOK ADDED"}


# ---------------- ADD BOOK ITEM ----------------

@app.post("/book_item")
def add_book_item(worker_id: str, isbn: str, barcode: str):

    success, result = library.add_book_item(worker_id, isbn, barcode)

    if not success:
        return {"error": result}

    return {"message": "BOOK ITEM ADDED"}

#----------------DELETE BOOK----------------

@app.delete("/books/{isbn}")
def delete_book(worker_id: str, isbn: str):

    success, result = library.deleteBook(worker_id, isbn)

    if not success:
        return {"error": result}

    return {
        "message": "BOOK REMOVED",
        "isbn": isbn
    }

# ---------------- ADD RACK ----------------

@app.post("/rack")
def add_rack(worker_id: str, floor: int, row: str):

    success, result = library.add_rack(worker_id, floor, row)

    if not success:
        return {"error": result}

    return {"message": "RACK ADDED"}


# ---------------- PLACE BOOK ----------------

@app.post("/place_book")
def place_book(worker_id: str, barcode: str, floor: int, row: str):
    success, result = library.place_book_in_rack(worker_id, barcode, floor, row)

    if not success:
        return {"error": result}

    return {"message": result}

# ---------------- SHOW BOOK ----------------

@app.get("/books/available")
def available_books():
    return library.getAvailableBooks()

# ---------------- SEARCH ----------------

@app.get("/books/search")
def search(keyword: str):
    result = library.find_book(keyword)
    if not result:
        return {"error": "BOOK NOT FOUND"}

    return result

# ---------------- BORROW ----------------

@app.post("/borrow")
def borrow(user_id: str, isbn: str, payment: str,
           card_number: str = None,
           holder: str = None,
           expiry: str = None,
           cvv: str = None):

    payment_data = None

    if payment == "credit":
        payment_data = {
            "card_number": card_number,
            "holder": holder,
            "expiry": expiry,
            "cvv": cvv
        }

    success, result = library.requestBorrow(
        user_id,
        isbn,
        payment,
        payment_data
    )

    if not success:
        return {"error": result}

    return result.to_dict()


# ---------------- LENDINGS ----------------

@app.get("/lendings")
def get_lendings():
    return [l.to_dict() for l in library.lendings]


# ---------------- USER LENDINGS ----------------

@app.get("/lendings/{user_id}")
def get_user_lendings(user_id: str):

    result = []

    for l in library.lendings:
        if l.user.id == user_id:
            result.append(l.to_dict())

    return result

# ---------------- USER RETURN ----------------

@app.post("/return")
def return_book(lending_id: str):

    success, result = library.returnRequest(lending_id)

    if not success:
        return {"error": result}

    return result

# ---------------- RESERVE BOOK ----------------

@app.post("/reserve")
def reserve_book(user_id: str,
                 isbn: str,
                 payment: str,
                 card_number: str = None,
                 holder: str = None,
                 expiry: str = None,
                 cvv: str = None):

    payment_data = None

    if payment == "credit":
        payment_data = {
            "card_number": card_number,
            "holder": holder,
            "expiry": expiry,
            "cvv": cvv
        }

    success, result = library.reserveBook(
        user_id,
        isbn,
        payment,
        payment_data
    )

    if not success:
        return {"error": result}

    return {
        "message": "RESERVED",
        "reservation_id": result.id,
        "book": result.book.title,
        "status": result.status,
        "deposit": result.deposit_amount
    }

# ---------------- CANCEL RESERVATION ----------------

@app.post("/cancel_reservation")
def cancel_reservation(user_id: str, reservation_id: str):

    success, result = library.cancelReservation(reservation_id, user_id)

    if not success:
        return {"error": result}

    return {
        "message": result
    }


# ---------------- RESERVATIONS ----------------

@app.get("/my_reservations/{user_id}")
def my_reservations(user_id: str):

    result = []

    for r in library.bookreservations:

        if r.user.id == user_id:

            result.append({
                "reservation_id": r.id,
                "book": r.book.title,
                "isbn": r.book.isbn,
                "status": r.status,
                "reserved_at": str(r.reservationDate),
                "expire_at": str(r.expireDate) if r.expireDate else None
            })

    return result

@app.get("/reservations/queue/{isbn}")
def get_reservation_queue(isbn: str):

    success, queue = library.getReservationQueue(isbn)

    if not success:
        raise HTTPException(status_code=404, detail=queue)

    return {
        "isbn": isbn,
        "queue": queue
    }

@app.post("/rooms/add")
def add_room(user_id: str, room_id: str, name: str, capacity: int, price: int):

    success, result = library.add_room(user_id, room_id, name, capacity, price)

    if not success:
        return {"success": False, "message": result}

    return {
        "success": True,
        "data": {
            "room_id": result.room_id,
            "name": result.name,
            "capacity": result.capacity,
            "price": result.price
        }
    }

@app.get("/rooms")
def get_rooms():
    return library.getRooms()

@app.delete("/rooms/{room_id}")
def delete_room(user_id: str, room_id: str):

    success, result = library.deleteRoom(user_id, room_id)

    if not success:
        return {"success": False, "message": result}

    return {
        "success": True,
        "message": "ROOM DELETED"
    }

@app.post("/rooms/reserve")
def reserve_room(user_id: str,
                 room_id: str,
                 reserve_date: str,
                 slot_time: str,
                 people: int,
                 payment: str,
                 card_number: str = None,
                 holder: str = None,
                 expiry: str = None,
                 cvv: str = None):
    payment_data = None

    if payment == "credit":
        payment_data = {
            "card_number": card_number,
            "holder": holder,
            "expiry": expiry,
            "cvv": cvv
        }

    success, result = library.requestRoomReservation(
        user_id,
        room_id,
        reserve_date,
        slot_time,
        people,
        payment,
        payment_data
    )

    if not success:
        return {"success": False, "message": result}

    return {
        "success": True,
        "data": result.to_dict()
    }

@app.post("/rooms/cancel")
def cancel_room_reservation(reservation_id: str, user_id: str):

    success, result = library.cancelRoomReservation(reservation_id, user_id)

    if not success:
        return {"success": False, "message": result}

    return {
        "success": True,
        "message": result
    }

@app.get("/rooms/reservations")
def get_reservations():

    return [r.to_dict() for r in library.room_reservations]

@app.delete("/delete_user/{user_id}")
def delete_user(admin_id: str, user_id: str):

    success, result = library.deleteUser(admin_id, user_id)

    if not success:
        return {"error": result}

    return {
        "message": "MEMBER REMOVED",
        "user_id": user_id
    }

@app.post("/pay_fine")
def pay_fine(lending_id: str,
             payment: str,
             card_number: str = None,
             holder: str = None,
             expiry: str = None,
             cvv: str = None):

    payment_data = None

    if payment == "credit":
        payment_data = {
            "card_number": card_number,
            "holder": holder,
            "expiry": expiry,
            "cvv": cvv
        }

    success, result = library.payFine(
        lending_id,
        payment,
        payment_data
    )

    if not success:
        return {"success": False, "message": result}

    return {
        "success": True,
        "message": "FINE PAID"
    }

if __name__ == "__main__":
    uvicorn.run("API.main:app", host="127.0.0.1", port=8000, reload=True)