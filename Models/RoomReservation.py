class RoomReservation:

    def __init__(self, id, user, room, date, timeslot):
        self.id = id
        self.user = user
        self.room = room
        self.date = date
        self.timeslot = timeslot
        self.status = "RESERVED"

    def to_dict(self):
        return {
            "reservation_id": self.id,
            "member": self.user.name,
            "room": self.room.name,
            "date": self.date.strftime("%Y-%m-%d"),
            "slot_time": self.timeslot.time,
            "status": self.status
        }