class User:

    user_info = dict()

    def __init__(self, id):
        self.id = id
        if self.id not in self.user_info.keys():
            User.add_user(id, self)

    @classmethod
    def add_user(cls, id, user):
        cls.user_info[id] = user
        print(type(user))

    @property
    def get_user(self):
        return self.id