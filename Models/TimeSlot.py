class TimeSlot:

    SLOT_TIMES = [
        "08.00-09.00",
        "09.00-10.00",
        "10.00-11.00",
        "11.00-12.00",
        "12.00-13.00",
        "13.00-14.00",
        "14.00-15.00",
        "15.00-16.00",
        "16.00-17.00"
    ]

    def __init__(self, slot_id, room, reserve_date):
        if slot_id < 0 or slot_id >= len(TimeSlot.SLOT_TIMES):
            raise ValueError("INVALID SLOT ID")

        self.__slot_id = slot_id
        self.__room = room
        self.__reserve_date = reserve_date
        self.__time = TimeSlot.SLOT_TIMES[slot_id]

    @property
    def slot_id(self):
        return self.__slot_id

    @property
    def room(self):
        return self.__room

    @property
    def reserve_date(self):
        return self.__reserve_date

    @property
    def time(self):
        return self.__time

    @classmethod
    def get_slot_id(cls, slot_time):
        if not slot_time:
            return None

        slot_time = slot_time.strip().replace(":", ".")
        start = slot_time.split("-")[0]
        if "." not in start:
            start = f"{start}.00"

        for i, t in enumerate(cls.SLOT_TIMES):
            if t.startswith(start):
                return i

        return None