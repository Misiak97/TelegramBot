# -*- coding: utf-8 -*-

import requests
import json
import os

import telebot

import settings

from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(settings.token)

req_key = os.getenv('REQUEST_KEY')

request_settings = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': req_key
        }


def id_city_selection(city: str, user_id: int):
    """
    Парсер всех городов название которых совпадает с названием введенным пользователем
    :param city: String. Название города
    :param user_id: Int. Айди пользователя
    :return: Dict. Словарь с ключом - адрес, название города и значением - айди города
    """
    cities = dict()

    url = "https://hotels4.p.rapidapi.com/locations/search"

    querystring = {"query": f'{city}', "locale": "ru_RU"}

    headers = request_settings
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=30)
        req = json.loads(response.text)
        result = req.get('suggestions')
    except TimeoutError:
        bot.send_message(user_id, 'К сожалению сервис временно недоступен, попробуйте повторить попытку позже!')
        return

    for cities_info in result:
        for i_city in cities_info['entities']:
            if i_city.get('name') == city:
                address = i_city.get('caption').split(',')
                cities[f'{address[1].lstrip()}, {i_city["name"]}'] = i_city['destinationId']

    return cities
