import telebot
import telebot
import datetime
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


@bot.message_handler(commands='start')
def start(message):
    bot.send_message(message.from_user.id, f'{start_message}\n{commands}')


@bot.message_handler(commands='help')
def helping_commands(message):
    bot.send_message(message.from_user.id, f'Список команд:\n{commands}')


bot.polling(none_stop=True, interval=0)
