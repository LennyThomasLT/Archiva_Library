from fastmcp import FastMCP
from Service.Library import Library
from Models.Book import BookType
from datetime import datetime

mcp = FastMCP("library")

library = Library()

print("MCP Server starting...")

#---------------DATA----------------

success, admin = library.create_staff("Admin", "admin", "admin123", "admin")
if not success:
    raise Exception(admin)

success, worker = library.create_staff("Worker", "worker", "worker123", "worker")
if not success:
    raise Exception(worker)


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


# ---------------- USER ----------------

@mcp.tool
def register(name: str, username: str, password: str):

    success, result = library.register_user(name, username, password)

    if not success:
        return {"error": result}

    return {"user_id": result.id}


@mcp.tool
def login(username: str, password: str):

    user = library.login(username, password)

    if not user:
        return {"error": "INVALID LOGIN"}

    return {
        "user_id": user.id,
        "role": user.getRole()
    }

@mcp.tool()
def logout(user_id: str):
    success, result = library.logout(user_id)

    if not success:
        return {"error": result}

    return {"message": result}


@mcp.tool
def upgrade_member(user_id: str):

    success, result = library.upgrade_member(user_id)

    if not success:
        return {"error": result}

    return {"member_id": result.member_id}


# ---------------- STAFF ----------------

@mcp.tool
def create_staff(admin_id: str, name: str, username: str, password: str, role: str):

    success, result = library.create_staff(
        name,
        username,
        password,
        role,
        admin_id
    )

    if not success:
        return {"error": result}

    return {
        "staff_id": result.staff_id,
        "user_id": result.id
    }


@mcp.tool
def delete_user(admin_id: str, user_id: str):

    success, result = library.deleteUser(admin_id, user_id)

    if not success:
        return {"error": result}

    return {
        "message": "MEMBER REMOVED",
        "user_id": user_id
    }


# ---------------- BOOK ----------------

@mcp.tool
def search_book(keyword: str):

    result = library.find_book(keyword)

    if not result:
        return {"error": "BOOK NOT FOUND"}

    return result


@mcp.tool
def available_books():
    return library.getAvailableBooks()


@mcp.tool
def add_book(worker_id: str, isbn: str, title: str, author: str, price: float, book_type: str):

    success, result = library.add_book(worker_id, isbn, title, author, price, book_type)

    if not success:
        return {"error": result}

    return {"message": "BOOK ADDED"}


@mcp.tool
def delete_book(worker_id: str, isbn: str):

    success, result = library.deleteBook(worker_id, isbn)

    if not success:
        return {"error": result}

    return {"message": "BOOK REMOVED"}


# ---------------- BOOK ITEM ----------------

@mcp.tool
def add_book_item(worker_id: str, isbn: str, barcode: str):

    success, result = library.add_book_item(worker_id, isbn, barcode)

    if not success:
        return {"error": result}

    return {"message": "BOOK ITEM ADDED"}


# ---------------- RACK ----------------

@mcp.tool
def add_rack(worker_id: str, floor: int, row: str):

    success, result = library.add_rack(worker_id, floor, row)

    if not success:
        return {"error": result}

    return {"message": "RACK ADDED"}


@mcp.tool
def place_book(worker_id: str, barcode: str, floor: int, row: str):

    success, result = library.place_book_in_rack(worker_id, barcode, floor, row)

    if not success:
        return {"error": result}

    return {"message": result}


# ---------------- BORROW ----------------

@mcp.tool
def borrow_book(
        user_id: str,
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

    success, result = library.requestBorrow(
        user_id,
        isbn,
        payment,
        payment_data
    )

    if not success:
        return {"error": result}

    return result.to_dict()


@mcp.tool
def return_book(lending_id: str):

    success, result = library.returnRequest(lending_id)

    if not success:
        return {"error": result}

    return result


@mcp.tool
def get_lendings():
    return [l.to_dict() for l in library.lendings]


@mcp.tool
def get_user_lendings(user_id: str):

    result = []

    for l in library.lendings:
        if l.user.id == user_id:
            result.append(l.to_dict())

    return result


# ---------------- RESERVATION ----------------

@mcp.tool
def reserve_book(
        user_id: str,
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
        "reservation_id": result.id,
        "book": result.book.title,
        "status": result.status,
        "deposit": result.deposit_amount
    }


@mcp.tool
def cancel_reservation(user_id: str, reservation_id: str):

    success, result = library.cancelReservation(reservation_id, user_id)

    if not success:
        return {"error": result}

    return {"message": result}


@mcp.tool
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


@mcp.tool
def reservation_queue(isbn: str):

    success, queue = library.getReservationQueue(isbn)

    if not success:
        return {"error": queue}

    return {
        "isbn": isbn,
        "queue": queue
    }


# ---------------- ROOM ----------------

@mcp.tool
def add_room(user_id: str, room_id: str, name: str, capacity: int, price: float):

    success, result = library.add_room(
        user_id,
        room_id,
        name,
        capacity,
        price
    )

    if not success:
        return {"error": result}

    return {
        "room_id": result.room_id,
        "name": result.name,
        "capacity": result.capacity,
        "price": result.price
    }

@mcp.tool
def get_rooms():
    return library.getRooms()

@mcp.tool
def delete_room(user_id: str, room_id: str):

    success, result = library.deleteRoom(user_id, room_id)

    if not success:
        return {"error": result}

    return {"message": "ROOM DELETED"}


@mcp.tool
def get_room_reservations():
    return [r.to_dict() for r in library.room_reservations]


@mcp.tool
def reserve_room(
        user_id: str,
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
        return {"error": result}

    return result.to_dict()


@mcp.tool
def cancel_room(reservation_id: str, user_id: str):

    success, result = library.cancelRoomReservation(reservation_id, user_id)

    if not success:
        return {"error": result}

    return {"message": result}


# ---------------- PAY FINE ----------------

@mcp.tool
def pay_fine(
        lending_id: str,
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
        return {"error": result}

    return {"message": "FINE PAID"}


if __name__ == "__main__":
    mcp.run()