import sqlite3


class User:

    users = dict()

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.city = None
        self.hotels_atm = None
        self.city_id = None
        self.photos_answer = False
        self.photos_atm = None
        self.hotel_id = None
        self.user_filter = None

    @classmethod
    def get_user(cls, id, name):
        if id in cls.users.keys():
            return cls.users[id]
        else:
            return cls.add_user(id, name)

    @classmethod
    def add_user(cls, id, name):
        cls.users[id] = User(id, name)
        return cls.users[id]

