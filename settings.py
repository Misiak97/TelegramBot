# -*- coding: utf-8 -*-

import os

from dotenv import load_dotenv


load_dotenv()
token = os.getenv('TOKEN')

logger_settings = ['log_file.log', '{time} {level} {message}', "DEBUG"]

start_message = 'Я бот для поиска подходящих вам отелей!\nВот список доступных комманд:'

commands = '/help - Помощь\n' \
           '/lowprice - Самые дешёвые отелей в городе\n' \
           '/highprice - Самые дорогие отели в городе\n' \
           '/bestdeal - Отели наиболее подходящие по цене и расположению от центра города\n' \
           '/history - История поиска'

normal_symbols = "^[a-zA-Zа-яА-Я -]+$"

commands_list = ['/bestdeal', '/highprice', '/lowprice']
