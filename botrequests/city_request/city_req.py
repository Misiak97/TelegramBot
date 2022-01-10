import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()

req_key = os.getenv('REQUEST_KEY')

request_settings = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': req_key
        }


def id_city_selection(city):
    """
    Парсер всех городов название которых совпадает с названием введенным пользователем
    :param city: String. Название города
    :return: Dict. Словарь с ключом - адрес, название города и значением - айди города
    """
    cities = dict()

    url = "https://hotels4.p.rapidapi.com/locations/search"

    querystring = {"query": f'{city}', "locale": "ru_RU"}

    headers = request_settings

    response = requests.request("GET", url, headers=headers, params=querystring)
    req = json.loads(response.text)
    result = req.get('suggestions')

    for cities_info in result:
        for i_city in cities_info['entities']:
            if i_city.get('name') == city:
                address = i_city.get('caption').split(',')
                cities[f'{address[1].lstrip()}, {i_city["name"]}'] = i_city['destinationId']

    return cities
