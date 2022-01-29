# -*- coding: utf-8 -*-

import os
import re
import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime, date
from telebot import types
from loguru import logger
from dotenv import load_dotenv
import History
from History import *
from user import User
from keybord import add_keyboard
from botrequests import best_deal_request, lowprice_request, city_req, photo_req


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
