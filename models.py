from peewee import *


db = SqliteDatabase('Search_result.db')


class LastSearch(Model):
    name = CharField(null=True)
    user_id = CharField(null=True)
    command = CharField(null=True)
    command_time = DateTimeField(null=True)
    hotels = CharField(null=True)

    class Meta:
        database = db
