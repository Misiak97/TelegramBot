# -*- coding: utf-8 -*-

import os
import json
import requests

import telebot

import settings

from dotenv import load_dotenv
from telebot.types import InputMediaPhoto


load_dotenv()

req_key = os.getenv('REQUEST_KEY')

bot = telebot.TeleBot(settings.token)

request_settings = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': req_key
        }


def get_photo(hotel_id: int, photo_atm: int, user_id: int):
    """
    Функция парсер получающая список url фотографий для дальнейшей отправки их пользователю
    :param hotel_id: Int. Айди отеля
    :param photo_atm: Int. Кол-во фото для поиска
    :param user_id: Int. Айди пользователя
    :return: List. Список url фото
    """

    photos_url_list = list()
    media_group = list()

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    headers = request_settings

    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=30)
        result = json.loads(response.text)
    except TimeoutError:
        bot.send_message(user_id, 'К сожалению сервис временно недоступен, попробуйте повторить попытку позже!')
        return

    for i_number, i_photo_info in enumerate(result.get('hotelImages')):
        if i_number == int(photo_atm):
            break
        photo_url = i_photo_info.get('baseUrl').format(
            size='z'
        )
        photos_url_list.append(photo_url)
    try:
        for i_url in photos_url_list:
            media_group.append(InputMediaPhoto(media=i_url))
    except TypeError:
        return 'К сожалению отель не предоставил фото'

    return media_group
