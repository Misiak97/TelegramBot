import telebot
from telebot.types import InputMediaPhoto
import logging
import flask
import datetime
from user import User
from dotenv import load_dotenv
import os
from botrequests import lowprice_request
import sqlite3


load_dotenv()

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

start_message = 'Я бот для поиска подходящих вам отелей!\nВот список доступных комманд:'
commands = '/help - Помощь\n' \
           '/lowprice - самые дешёвые отелей в городе\n' \
           '/highprice - самые дорогие отели в городе\n' \
           '/bestdeal - отели наиболее подходящие по цене и расположению от центра города\n' \
           '/history - история поиска'


@bot.message_handler(commands='start')
def start(message):
    print(message.from_user)
    user = User.get_user(message.from_user.id, message.from_user.first_name)
    bot.send_message(user.id, f'Здравтсвуйте, {user.name}!\n{start_message}\n{commands}')


@bot.message_handler(commands='help')
def helping_commands(message):
    bot.send_message(message.from_user.id, f'Список команд:\n{commands}')


@bot.message_handler(commands='lowprice')
def lowprice(message):
    user = User.get_user(message.from_user.id, message.from_user.first_name)
    user.user_filter = 'PRICE'
    bot.send_message(user.id, 'Введите название города, в котором искать отель:')
    bot.register_next_step_handler(message, city_finder)


@bot.message_handler(commands='highprice')
def highprice(message):
    user = User.get_user(message.from_user.id, message.from_user.first_name)
    user.user_filter = 'PRICE_HIGHEST_FIRST'
    bot.send_message(user.id, 'Введите название города, в котором искать отель:')
    bot.register_next_step_handler(message, city_finder)


@bot.message_handler(content_types='text')
def city_finder(message):
    user = User.get_user(message.from_user.id, message.from_user.first_name)
    user.city = message.text
    bot.send_message(message.from_user.id, 'Выберете цифру соответствующую нужному вам городу:')
    for i_city_number, i_city in enumerate(lowprice_request.id_city_selection(user.city)):
        bot.send_message(user.id, f'{i_city_number + 1}. {i_city}')
    bot.register_next_step_handler(message, city_id_identification)


@bot.message_handler(content_types='text')
def city_id_identification(message):
    user = User.get_user(message.from_user.id, message.from_user.first_name)
    user.user_choice = int(message.text)
    for i_city_number, i_city in enumerate(lowprice_request.id_city_selection(user.city)):
        if user.user_choice == i_city_number + 1:
            user.city_id = lowprice_request.id_city_selection(user.city)[i_city]
    bot.send_message(user.id, 'Введите кол-во отелей для поиска:')
    bot.register_next_step_handler(message, loads_photo_choice)


@bot.message_handler(content_types='text')
def loads_photo_choice(message):
    user = User.get_user(message.from_user.id, message.from_user.first_name)
    user.hotels_atm = message.text
    bot.send_message(user.id, 'Нужны ли фото отелей?')
    bot.register_next_step_handler(message, photos_atm)


@bot.message_handler(content_types='text')
def photos_atm(message):
    user = User.get_user(message.from_user.id, message.from_user.first_name)
    answer = message.text
    if answer.title() == 'Да':
        user.photos_answer = True
        bot.send_message(user.id, 'Сколько фото загрузить?')
        bot.register_next_step_handler(message, number_of_photo)
    elif answer.title() != 'Да':
        user.photos_answer = False
        bot.register_next_step_handler(message, hotels_atm_choicer)


@bot.message_handler(content_types='text')
def number_of_photo(message):
    user = User.get_user(message.from_user.id, message.from_user.first_name)
    photos_counter = message.text
    user.photos_atm = photos_counter
    bot.register_next_step_handler(message, hotels_atm_choicer)


@bot.message_handler(content_types='text')
def hotels_atm_choicer(message):
    user = User.get_user(message.from_user.id, message.from_user.first_name)
    bot.send_message(user.id, 'Пожалуйста подождите, подбираю отели по вашему запросу!')

    for i_hotel, i_hotel_info in lowprice_request.lowprice_req(user.city_id, user.hotels_atm, user.user_filter).items():
        hotel = f'{i_hotel}\n{", ".join(i_hotel_info[0:-1])}'
        bot.send_message(user.id, hotel)
        if user.photos_answer:
            hotel_id = i_hotel_info[-1]
            media = lowprice_request.get_photo(hotel_id, user.photos_atm)
            bot.send_media_group(user.id, media=media)


bot.polling(none_stop=True, interval=0)
