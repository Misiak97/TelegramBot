import sqlite3


class User:

    users = dict()

    def __init__(self, id, name, username):
        self.id = id
        self.name = name
        self.username = username
        self.city = None
        self.hotels_atm = None
        self.city_id = None
        self.photos_answer = False
        self.photos_atm = None
        self.hotel_id = None
        self.user_filter = None
        self.user_command = None
        self.arrival_date = None
        self.date_of_departure = None
        self.distance = None
        self.min_price = None
        self.max_price = None

    @classmethod
    def get_user(cls, id, name, username):
        if id in cls.users.keys():
            return cls.users[id]
        else:
            return cls.add_user(id, name, username)

    @classmethod
    def add_user(cls, id, name, username):
        cls.users[id] = User(id, name, username)
        return cls.users[id]


