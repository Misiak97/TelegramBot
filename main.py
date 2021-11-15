import telebot
import logging
import flask
import datetime
from user import User
from dotenv import load_dotenv
import os


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
    bot.send_message(message.from_user.id, f'{start_message}\n{commands}')
    user = User(message.from_user.id)
    print(message.from_user)


@bot.message_handler(commands='help')
def helping_commands(message):
    bot.send_message(message.from_user.id, f'Список команд:\n{commands}')


@bot.message_handler(commands='lowprice')
def lowprice(message):
    bot.send_message(message.from_user.id, 'Введите название города, в котором искать отель:')
    bot.register_next_step_handler(message, hotel_request)


@bot.message_handler(content_types='text')
def hotel_request(message):
    hotel_count = 0
    bot.send_message(message.from_user.id, 'Введите кол-во отелей:')
    while hotel_count == 0:
        hotel_count = message.text
        try:
            hotel_count = int(message.text)
        except ValueError as error:
            logging.exception(f'Кол-во отелей должно быть числом {error}')


bot.polling(none_stop=True, interval=0)
