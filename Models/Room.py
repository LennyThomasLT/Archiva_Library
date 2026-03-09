from Models.TimeSlot import TimeSlot

class Room:

    def __init__(self, room_id, name, capacity):
        self.room_id = room_id
        self.name = name
        self.capacity = capacity
        self.timeslots = []
        self.deleted = False

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