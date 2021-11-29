import telebot
import logging
import flask
import datetime
from user import User
from dotenv import load_dotenv
import os
import sqlite3


load_dotenv()


token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

start_message = 'Привет! Я бот для поиска подходящих вам отелей!\nВот список доступных комманд:'
commands = '/help - Помощь\n' \
           '/lowprice - самые дешёвые отелей в городе\n' \
           '/highprice - самые дорогие отели в городе\n' \
           '/bestdeal - отели наиболее подходящие по цене и расположению от центра города\n' \
           '/history - история поиска'

user_inquiry = dict()


@bot.message_handler(commands='start')
def start(message):
    user = User(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    print(user)
    bot.send_message(message.from_user.id, f'Здравтсвуйте, {user.get_name}\n{start_message}\n{commands}')


@bot.message_handler(commands='help')
def helping_commands(message):
    bot.send_message(message.from_user.id, f'Список команд:\n{commands}')


@bot.message_handler(commands='lowprice')
def lowprice(message):
    bot.send_message(message.from_user.id, 'Введите название города, в котором искать отель:')
    bot.register_next_step_handler(message, hotel_request)


@bot.message_handler(content_types='text')
def hotel_request(message):
    needed_city = message.text
    bot.send_message(message.from_user.id, 'Введите кол-во отелей для поиска:')
    bot.register_next_step_handler(message, date_picker)


@bot.message_handler(content_types='text')
def date_picker(message):
    pass


bot.polling(none_stop=True, interval=0)
