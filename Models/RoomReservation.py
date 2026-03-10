class RoomReservation:

    def __init__(self, id, user, room, date, timeslot):
        self.__id = id
        self.__user = user
        self.__room = room
        self.__date = date
        self.__timeslot = timeslot
        self.__status = "RESERVED"

    @property
    def id(self):
        return self.__id

    @property
    def user(self):
        return self.__user

    @property
    def room(self):
        return self.__room

    @property
    def date(self):
        return self.__date

    @property
    def timeslot(self):
        return self.__timeslot

    @property
    def status(self):
        return self.__status
    
    def to_dict(self):
        return {
            "reservation_id": self.id,
            "user_id": self.user.id,
            "user_name": self.user.name,
            "room_id": self.room.room_id,
            "room_name": self.room.name,
            "date": str(self.date),
            "timeslot": self.timeslot.slot_id,
            "time": self.timeslot.time,
            "status": self.status
        }