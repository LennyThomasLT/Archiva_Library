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

# success, item2 = library.add_book_item(worker.id, "101", "BC002")
# print("Add BC002 to ISBN 101")

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

# ---------------- PLACE BOOK ----------------

print("TEST 12: Place Books")

print("Place BC001 -> Rack (1,A)")
success, result = library.place_book_in_rack(worker.id, "BC001", 1, "A")
assert success

# print("Place BC002 -> Rack (1,A)")
# success, result = library.place_book_in_rack(worker.id, "BC002", 1, "A")
# assert success

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

print("TEST 13: Place Duplicate Book")

success, result = library.place_book_in_rack(worker.id, "BC001", 1, "A")

print("Try place BC001 again ->", success)

assert success == False

print("PASS\n")

print("TEST 14: Rack Not Exist")

success, result = library.place_book_in_rack(worker.id, "BC001", 9, "Z")

print("Try place to rack (9,Z) ->", success)

assert success == False

print("PASS\n")

# ---------------- SEARCH ----------------

print("TEST 15: Search Book")

result = library.find_book("Python")

print("Search 'Python' -> result count:", len(result))

assert len(result) == 1

print("PASS\n")

print("TEST 16: Search Not Found")

result = library.find_book("Unknown")

print("Search 'Unknown' ->", result)

assert result == []

print("PASS\n")

# ---------------- BORROW ----------------

print("TEST 17: Normal User Borrow General Book")

success, lending = library.requestBorrow(n1.id, "101")

print("User", n1.id, "borrow ISBN 101 ->", success)

assert success

print("PASS\n")

print("TEST 18: Normal User Borrow Premium")

success, result = library.requestBorrow(n1.id, "103")

print("User", n1.id, "borrow premium 103 ->", success)

assert success == False

print("PASS\n")

print("TEST 19: Member Borrow Premium")

success, lending = library.requestBorrow(m1.id, "103")

print("Member", m1.id, "borrow premium 103 ->", success)

assert success

print("PASS\n")

print("TEST 20: Borrow Book Not Available")

success, result = library.requestBorrow(n2.id, "101")

print("User", n2.id, "borrow 101 again ->", success)

assert success == False

print("PASS\n")

print("TEST 21: Borrow Limit Reached")

success, result = library.requestBorrow(n1.id, "102")

print("User", n1.id, "borrow another book ->", success)

assert success == False

print("PASS\n")

print("ALL TESTS PASSED")