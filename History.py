from peewee import *
from datetime import datetime


db = SqliteDatabase('Search_result')


class AllSearchHistory(Model):
    name = TextField(null=True)
    user_id = TextField(null=True)
    command_time = DateTimeField(null=True)
    command = TextField(null=True)
    hotels = TextField(null=True)

    class Meta:
        database = db


class LastSearch(Model):
    name = TextField(null=True)
    user_id = TextField(null=True)
    command_time = DateTimeField(null=True)
    command = TextField(null=True)
    hotels = TextField(null=True)

    class Meta:
        database = db


def change_db_cmd_name(my_db, somebody):
    print(my_db.__name__)

    if my_db.__name__ == 'LastSearch':
        fst_user_search_db = my_db.select().where(my_db.user_id == somebody.id).get()
        fst_user_search_db.command = somebody.user_command
        fst_user_search_db.command_time = datetime.now()
        fst_user_search_db.save()
        for i_user in my_db.select().where(my_db.user_id == somebody.id):
            print(i_user.name, i_user.user_id, i_user.command_time, i_user.command, i_user.hotels)
    elif my_db.__name__ == 'AllSearchHistory':
        fst_user_search_db = my_db.select().where(my_db.user_id == somebody.id).get()
        update = fst_user_search_db.insert(command_time=datetime.now(), command=somebody.user_command)
        update.execute()
        for i_user in my_db.select().where(my_db.user_id == somebody.id):
            print(i_user.name, i_user.user_id, i_user.command_time, i_user.command, i_user.hotels)
