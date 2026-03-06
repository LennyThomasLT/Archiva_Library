class BookRack:
    def __init__(self, floor, row):
        self.floor = floor
        self.row = row
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        item.rack = self

    def has_book(self, book):
        return any(item.book == book for item in self.items)

    def get_full_location(self):
        return f"Floor {self.floor}, Row {self.row}"