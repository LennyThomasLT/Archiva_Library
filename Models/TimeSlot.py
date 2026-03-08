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
        self.slot_id = slot_id
        self.room = room
        self.reserve_date = reserve_date
        self.time = TimeSlot.SLOT_TIMES[slot_id]

    @classmethod
    def get_slot_id(cls, slot_time):
        if not slot_time:
            return None

        slot_time = slot_time.replace(":", ".").strip()
        start = slot_time.split("-")[0]

        for i, t in enumerate(cls.SLOT_TIMES):
            if t.startswith(start):
                return i

        return None