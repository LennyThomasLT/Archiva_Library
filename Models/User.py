class User:
    def __init__(self, id, name, username, password):
        self.id = id
        self.name = name
        self.username = username
        self.password = password

    def borrowLimit(self):
        raise NotImplementedError()

    def getDiscount(self):
        return 0

    def getRole(self):
        return "USER"


class NormalUser(User):

    def borrowLimit(self):
        return 1

    def getDiscount(self):
        return 0

    def getRole(self):
        return "NORMAL_USER"


class Member(User):

    def __init__(self, id, name, username, password, member_id, score):
        super().__init__(id, name, username, password)
        self.member_id = member_id
        self.score = score

    def borrowLimit(self):
        return 5

    def getDiscount(self):
        return 0.1

    def getScore(self):
        return self.score

    def getRole(self):
        return "MEMBER"


class Staff(User):

    def __init__(self, id, name, username, password, staff_id):
        super().__init__(id, name, username, password)
        self.staff_id = staff_id

    def borrowLimit(self):
        return 5

    def getDiscount(self):
        return 1.0

    def getRole(self):
        return "STAFF"


class Worker(Staff):

    def getRole(self):
        return "WORKER"


class SystemAdmin(Staff):

    def getRole(self):
        return "ADMIN"