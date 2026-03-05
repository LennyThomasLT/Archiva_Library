class BookRack:
    def __init__(self, floor, row):
        self.floor = floor
        self.row = row
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def has_book(self, book):
        for item in self.items:
            if item.book == book:
                return True
        return False

    def get_full_location(self):
        return f"Floor {self.floor}, Row {self.row}"