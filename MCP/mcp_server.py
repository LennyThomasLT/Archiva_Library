from fastmcp import FastMCP
from Service.Library import Library
from Models.Book import BookType
from datetime import datetime

mcp = FastMCP("library")

library = Library()

print("MCP Server starting...")

#---------------DATA----------------

success, admin = library.create_staff("Admin", "admin", "admin123", "admin")
success, worker = library.create_staff("Worker", "worker", "worker123", "worker")

# ---------------- USER ----------------

@mcp.tool()
def register(name: str, username: str, password: str):

    success, result = library.register_user(name, username, password)

    if not success:
        return {"error": result}

    return {"user_id": result.id}

@mcp.tool()
def login(username: str, password: str):

    user = library.login(username, password)

    if not user:
        return {"error": "INVALID LOGIN"}

    return {
        "user_id": user.id,
        "role": user.getRole()
    }

@mcp.tool()
def upgrade_member(user_id: str):

    success, result = library.upgrade_member(user_id)

    if not success:
        return {"error": result}

    return {"member_id": result.member_id}

# --------------Create Admin------------

@mcp.tool()
def create_staff(admin_id: str, name: str, username: str, password: str, role: str):

    success, result = library.create_staff(
        admin_id,
        name,
        username,
        password,
        role
    )

    if not success:
        return {"error": result}

    return {
        "staff_id": result.staff_id,
        "user_id": result.id
    }

# ---------------- DELETE USER ---------

@mcp.tool()
def delete_user(admin_id: str, user_id: str):

    success, result = library.deleteUser(admin_id, user_id)

    if not success:
        return {"error": result}

    return {
        "message": "MEMBER REMOVED",
        "user_id": user_id
    }

# ---------------- BOOK ----------------

@mcp.tool()
def search_book(keyword: str):
    return library.find_book(keyword)

@mcp.tool()
def available_books():
    return library.getAvailableBooks()

@mcp.tool()
def add_book(worker_id: str, isbn: str, title: str, author: str, price: float, book_type: str):
    book_type_enum = BookType(book_type.upper())
    success, result = library.add_book(
        worker_id, isbn, title, author, price, book_type_enum
    )
    if not success:
        return {"error": result}

    return {"message": "BOOK ADDED"}

@mcp.tool()
def delete_book(worker_id: str, isbn: str):
    success, result = library.deleteBook(worker_id, isbn)
    if not success:
        return {"error": result}

    return {"message": "BOOK REMOVED"}

# ---------------- ADD BOOK ITEM --------------------

@mcp.tool()
def add_book_item(worker_id: str, isbn: str, barcode: str):
    success, result = library.add_book_item(worker_id, isbn, barcode)
    if not success:
        return {"error": result}

    return {"message": "BOOK ITEM ADDED"}

# ---------------- ADD RACK --------------

@mcp.tool()
def add_rack(worker_id: str, floor: int, row: str):
    success, result = library.add_rack(worker_id, floor, row)
    if not success:
        return {"error": result}

    return {"message": "RACK ADDED"}


@mcp.tool()
def place_book(worker_id: str, barcode: str, floor: int, row: str):
    success, result = library.place_book_in_rack(worker_id, barcode, floor, row)
    if not success:
        return {"error": result}

    return {"message": result}

# ---------------- BORROW ----------------

@mcp.tool()
def borrow_book(user_id: str, isbn: str, payment: str):
    success, result = library.requestBorrow(user_id, isbn, payment)
    if not success:
        return {"error": result}

    return result.to_dict()

@mcp.tool()
def return_book(lending_id: str):
    success, result = library.returnRequest(lending_id)
    if not success:
        return {"error": result}

    return result

@mcp.tool()
def get_lendings():
    return [l.to_dict() for l in library.lendings]

@mcp.tool()
def get_user_lendings(user_id: str):
    result = []

    for l in library.lendings:
        if l.user.id == user_id:
            result.append(l.to_dict())

    return result

# ---------------- RESERVATION ----------------

@mcp.tool()
def reserve_book(user_id: str, isbn: str):

    success, result = library.reserveBook(user_id, isbn)

    if not success:
        return {"error": result}

    return {
        "reservation_id": result.id,
        "book": result.book.title
    }

@mcp.tool()
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

@mcp.tool()
def reservation_queue(isbn: str):
    success, queue = library.getReservationQueue(isbn)

    if not success:
        return {"error": queue}

    return {
        "isbn": isbn,
        "queue": queue
    }

@mcp.tool()
def cancel_reservation(user_id: str, reservation_id: str):

    success, result = library.cancelReservation(reservation_id, user_id)

    if not success:
        return {"error": result}

    return {"message": result}

# ---------------- ROOM ----------------

@mcp.tool()
def add_room(user_id: str, room_id: str, name: str, capacity: int):
    success, result = library.add_room(user_id, room_id, name, capacity)
    if not success:
        return {"error": result}

    return {
        "room_id": result.room_id,
        "name": result.name,
        "capacity": result.capacity
    }

@mcp.tool()
def available_rooms():
    return library.getRooms()

@mcp.tool()
def delete_room(user_id: str, room_id: str):
    success, result = library.deleteRoom(user_id, room_id)
    if not success:
        return {"error": result}

    return {"message": "ROOM DELETED"}

@mcp.tool()
def get_room_reservations():
    return [r.to_dict() for r in library.room_reservations]

@mcp.tool()
def reserve_room(user_id: str, room_id: str, reserve_date: str, slot_time: str, people: int):

    date = datetime.strptime(reserve_date, "%Y-%m-%d")

    success, result = library.requestRoomReservation(
        user_id, room_id, date, slot_time, people
    )

    if not success:
        return {"error": result}

    return result.to_dict()

@mcp.tool()
def cancel_room(reservation_id: str, user_id: str):

    success, result = library.cancelRoomReservation(reservation_id, user_id)

    if not success:
        return {"error": result}

    return {"message": result}

# ---------------- PAY FINE ----------------

@mcp.tool()
def pay_fine(lending_id: str, payment: str):

    success, result = library.payFine(lending_id, payment)

    if not success:
        return {"error": result}

    return {"message": "FINE PAID"}

if __name__ == "__main__":
    mcp.run()