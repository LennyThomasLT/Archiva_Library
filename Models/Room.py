from Models.TimeSlot import TimeSlot

class Room:

    def __init__(self, room_id, name, capacity, price):
        self.__room_id = room_id
        self.__name = name
        self.__capacity = capacity
        self.__timeslots = []
        self.__deleted = False
        self.__price = price

    @property
    def room_id(self):
        return self.__room_id

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value


    @property
    def capacity(self):
        return self.__capacity
    
    @capacity.setter
    def capacity(self, value):
        self.__capacity = value

    @property
    def timeslots(self):
        return self.__timeslots

    @property
    def deleted(self):
        return self.__deleted

    @deleted.setter
    def deleted(self, value):
        self.__deleted = value

    @property
    def price(self):
        return self.__price

    def clear_timeslots(self):
        self.timeslots.clear()

    def over_capacity(self, people):
        return people > self.capacity

    def reserve_timeslot(self, reserve_date, slot_id):
        for t in self.timeslots:
            if t.reserve_date == reserve_date and t.slot_id == slot_id:
                return None

        timeslot = TimeSlot(slot_id, self, reserve_date)
        self.timeslots.append(timeslot)

        return timeslot

    def remove_timeslot(self, timeslot):

        if timeslot in self.timeslots:
            self.timeslots.remove(timeslot)