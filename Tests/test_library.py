# ผม Test ไม่ครบนะครับ!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!

from Service.Library import Library
from Models.Book import BookType

print("START TEST\n")

library = Library()

# ---------------- CREATE USERS ----------------

print("TEST 1: Register Users")

success, u1 = library.register_user("Alice", "alice", "1234")
print("Create user:", u1.id, u1.name)
assert success

success, u2 = library.register_user("Bob", "bob", "1234")
print("Create user:", u2.id, u2.name)
assert success

print("PASS\n")

print("TEST 2: Upgrade Member")

success, m1 = library.upgrade_member(u1.id)
print("Upgrade:", u1.id, "-> MEMBER")
assert success

success, m2 = library.upgrade_member(u2.id)
print("Upgrade:", u2.id, "-> MEMBER")
assert success

print("PASS\n")

print("TEST 3: Register Normal Users")

success, n1 = library.register_user("Charlie", "charlie", "1234")
print("Create normal user:", n1.id)

success, n2 = library.register_user("David", "david", "1234")
print("Create normal user:", n2.id)

assert success
print("PASS\n")

# ---------------- STAFF ----------------

print("TEST 4: Create Staff")

admin = library._create_staff("Admin", "admin", "admin123", "admin")
worker = library._create_staff("Worker", "worker", "worker123", "worker")

print("Admin:", admin.id, admin.getRole())
print("Worker:", worker.id, worker.getRole())

assert admin.getRole() == "ADMIN"
assert worker.getRole() == "WORKER"

print("PASS\n")

# ---------------- ADD BOOK ----------------

print("TEST 5: Add Books")

success, b1 = library.add_book(worker.id, "101", "Python Basics", "John Smith", 100, BookType.GENERAL)
print("Add book:", b1.isbn, b1.title)
assert success

success, b2 = library.add_book(worker.id, "102", "FastAPI Guide", "Jane Doe", 120, BookType.GENERAL)
print("Add book:", b2.isbn, b2.title)
assert success

success, b3 = library.add_book(worker.id, "103", "Advanced AI", "Elon Data", 200, BookType.PREMIUM)
print("Add book:", b3.isbn, b3.title)
assert success

success, b4 = library.add_book(worker.id, "104", "Machine Learning Pro", "Andrew Data", 250, BookType.PREMIUM)
print("Add book:", b4.isbn, b4.title)
assert success

print("PASS\n")

print("TEST 6: Duplicate Book")

success, result = library.add_book(worker.id, "101", "Duplicate", "X", 100, BookType.GENERAL)

print("Try add duplicate ISBN 101 ->", success)

assert success == False

print("PASS\n")

# ---------------- ADD BOOK ITEM ----------------

print("TEST 7: Add Book Items")

success, item1 = library.add_book_item(worker.id, "101", "BC001")
print("Add BC001 to ISBN 101")

success, item3 = library.add_book_item(worker.id, "102", "BC003")
print("Add BC003 to ISBN 102")

success, item4 = library.add_book_item(worker.id, "103", "BC004")
print("Add BC004 to ISBN 103")

success, item5 = library.add_book_item(worker.id, "104", "BC005")
print("Add BC005 to ISBN 104")

assert success
print("PASS\n")

print("TEST 8: Duplicate Barcode")

success, result = library.add_book_item(worker.id, "101", "BC001")

print("Try duplicate barcode BC001 ->", success)

assert success == False

print("PASS\n")

print("TEST 9: Book Not Exist")

success, result = library.add_book_item(worker.id, "999", "BC999")

print("Try add item to ISBN 999 ->", success)

assert success == False

print("PASS\n")

# ---------------- ADD RACK ----------------

print("TEST 10: Add Rack")

success, rack = library.add_rack(worker.id, 1, "A")

print("Create rack Floor:", rack.floor, "Row:", rack.row)

assert success

print("PASS\n")

print("TEST 11: Duplicate Rack")

success, result = library.add_rack(worker.id, 1, "A")

print("Try duplicate rack (1,A) ->", success)

assert success == False

print("PASS\n")

print("TEST 12: Negative Floor Rack")

success, result = library.add_rack(worker.id, -1, "B")

print("Try add rack floor -1 ->", success)

assert success == False

print("PASS\n")

# ---------------- PLACE BOOK ----------------

print("TEST 13: Place Books")

print("Place BC001 -> Rack (1,A)")
success, result = library.place_book_in_rack(worker.id, "BC001", 1, "A")
assert success

print("Place BC003 -> Rack (1,A)")
success, result = library.place_book_in_rack(worker.id, "BC003", 1, "A")
assert success

print("Place BC004 -> Rack (1,A)")
success, result = library.place_book_in_rack(worker.id, "BC004", 1, "A")
assert success

print("Place BC005 -> Rack (1,A)")
success, result = library.place_book_in_rack(worker.id, "BC005", 1, "A")
assert success

print("PASS\n")

print("TEST 14: Place Duplicate Book")

success, result = library.place_book_in_rack(worker.id, "BC001", 1, "A")

print("Try place BC001 again ->", success)

assert success == False

print("PASS\n")

print("TEST 15: Rack Not Exist")

success, result = library.place_book_in_rack(worker.id, "BC001", 9, "Z")

print("Try place to rack (9,Z) ->", success)

assert success == False

print("PASS\n")

# ---------------- SEARCH ----------------

print("TEST 16: Search Book")

result = library.find_book("Python")

print("Search 'Python' -> result count:", len(result))

assert len(result) == 1

print("PASS\n")

print("TEST 17: Search Not Found")

result = library.find_book("Unknown")

print("Search 'Unknown' ->", result)

assert result == []

print("PASS\n")

# ---------------- BORROW ----------------

print("TEST 18: Normal User Borrow General Book")

success, lending1 = library.requestBorrow(n1.id, "101")

print("User", n1.id, "borrow ISBN 101 ->", success)

assert success

print("PASS\n")

print("TEST 19: Normal User Borrow Premium")

success, result = library.requestBorrow(n1.id, "103")

print("User", n1.id, "borrow premium 103 ->", success)

assert success == False

print("PASS\n")

print("TEST 20: Member Borrow Premium")

success, lending2 = library.requestBorrow(m1.id, "103")

print("Member", m1.id, "borrow premium 103 ->", success)

assert success

print("PASS\n")

print("TEST 21: Borrow Book Not Available")

success, result = library.requestBorrow(n2.id, "101")

print("User", n2.id, "borrow 101 again ->", success)

assert success == False

print("PASS\n")

print("TEST 22: Borrow Limit Reached")

success, result = library.requestBorrow(n1.id, "102")

print("User", n1.id, "borrow another book ->", success)

assert success == False

print("PASS\n")

# ---------------- RETURN ----------------

print("TEST 23: Return Book")

success, result = library.returnRequest(lending1.id)

print("Return lending:", lending1.id, "->", success)

assert success

print("PASS\n")

print("TEST 24: Return Same Book Again")

success, result = library.returnRequest(lending1.id)

print("Return again ->", success)

assert success == False

print("PASS\n")

print("TEST 25: Return Invalid ID")

success, result = library.returnRequest(9999)

print("Return invalid id ->", success)

assert success == False

print("PASS\n")

print("TEST 26: Member Score Check")

print("Member score:", m1.score)

assert m1.score >= 0

print("PASS\n")

print("ALL TESTS PASSED")

from datetime import datetime, timedelta

print("TEST 27: Return Late (Fine Test)")

# borrow ก่อน
success, lending_late = library.requestBorrow(m2.id, "104")
assert success

# ทำให้ overdue
lending_late.dueDate = datetime.now() - timedelta(days=1)

old_score = m2.score

success, result = library.returnRequest(lending_late.id)

print("Fine:", result["fine"])
print("Old Score:", old_score)
print("New Score:", result["member_score"])

assert success
assert result["fine"] > 0
assert result["member_score"] < old_score

print("PASS\n")


print("TEST 28: Reservation Create")

# borrow book ให้ unavailable ก่อน
success, lending_res = library.requestBorrow(m1.id, "102")
assert success

# member อีกคน reserve
success, res1 = library.reserveBook(m2.id, "102")

print("Reserve book 102 by", m2.id, "->", success)

assert success
assert res1.status == "WAITING"

print("PASS\n")


print("TEST 29: Reservation Queue")

success, queue = library.getReservationQueue("102")

print("Queue:", queue)

assert success
assert len(queue) == 1
assert queue[0]["position"] == 1

print("PASS\n")


print("TEST 30: Second Reservation")

success, res2 = library.reserveBook(m1.id, "102")

print("Second reserve ->", success)

assert success

success, queue = library.getReservationQueue("102")

print("Queue after second reserve:", queue)

assert len(queue) == 2
assert queue[1]["position"] == 2

print("PASS\n")


print("TEST 31: Return Book Trigger READY")

success, result = library.returnRequest(lending_res.id)

assert success

success, queue = library.getReservationQueue("102")

print("Queue after return:", queue)

assert queue[0]["status"] == "READY"

print("PASS\n")


print("TEST 32: Reserved User Borrow")

success, lending_reserved = library.requestBorrow(m2.id, "102")

print("Reserved user borrow ->", success)

assert success

success, queue = library.getReservationQueue("102")

print("Queue after borrow:", queue)

assert len(queue) == 1

print("PASS\n")


print("TEST 33: Cancel Reservation")

success, temp_lending = library.requestBorrow(m1.id, "101")
assert success

success, res3 = library.reserveBook(m2.id, "101")
assert success

success, msg = library.cancelReservation(res3.id, m2.id)

print("Cancel reservation ->", success)

assert success

print("PASS\n")
print("TEST 34: Reservation Limit")

books = ["201","202","203","204","205"]

# create books
for isbn in books:
    library.add_book(worker.id, isbn, f"Book {isbn}", "X", 100, BookType.GENERAL)
    library.add_book_item(worker.id, isbn, f"BC{isbn}")

# ใช้ user ใหม่ borrow
success, temp_user = library.register_user("Temp", "temp", "1234")
success, temp_member = library.upgrade_member(temp_user.id)

# borrow เพื่อทำให้ unavailable
for isbn in books:
    success, _ = library.requestBorrow(temp_member.id, isbn)
    assert success

# reserve 5 เล่ม
for isbn in books:
    success, _ = library.reserveBook(m2.id, isbn)
    assert success

# reserve เล่มที่ 6
success, result = library.reserveBook(m2.id, "101")

print("Try reserve more than 5 ->", success)

assert success == False

print("PASS\n")


print("ALL RESERVATION TESTS PASSED")