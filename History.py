# -*- coding: utf-8 -*-
import models
from models import LastSearch


def check_history(user_name, user_id, user_command, time, user_hotels):
    LastSearch.create(name=user_name, user_id=user_id, command=user_command, command_time=time, hotels=user_hotels)
