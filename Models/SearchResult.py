class SearchResult:

    def __init__(self, book, location, available_count):
        self.__id = book.isbn
        self.__title = book.title
        self.__author = book.author
        self.__price = book.price
        self.__book_type = book.booktype.value
        self.__location = location
        self.__available_amount = available_count

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def price(self):
        return self.__price

    @property
    def book_type(self):
        return self.__book_type

    @property
    def location(self):
        return self.__location

    @property
    def available_amount(self):
        return self.__available_amount

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "book_type": self.book_type,
            "location": self.location,
            "available_amount": self.available_amount
        }