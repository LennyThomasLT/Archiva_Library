class BookRack:
    def __init__(self, floor, row):
        self.__floor = floor
        self.__row = row
        self.__items = []

    @property
    def floor(self):
        return self.__floor

    @property
    def row(self):
        return self.__row

    @property
    def items(self):
        return self.__items

    def add_item(self, item):
        self.__items.append(item)
        item.rack = self

    def has_book(self, book):
        return any(
            item.book == book and item.checkAvailable() and not item.deleted
            for item in self.__items
        )

    def get_full_location(self):
        return f"Floor {self.__floor}, Row {self.__row}"