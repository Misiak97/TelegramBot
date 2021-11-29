class User:

    users = dict()

    def __init__(self, id: int, name: str, surname: str):
        self.id = id
        self.name = name
        self.surname = surname
        User.add_user(id, self)

    @classmethod
    def add_user(cls, id, user):
        cls.users[id] = user

    @property
    def get_name(self):
        return self.name
