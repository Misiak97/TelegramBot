# -*- coding: utf-8 -*-

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


def lowprice_req(city_id: int, hotels_atm: int, searching_filter: str, fst_date: str, sec_date: str):
    """
    Функция парсер для получения списка отелей найденных по введенным критериям
    :param city_id: Int. Айди города
    :param hotels_atm: Int. Кол-во отелей
    :param searching_filter: String. Фильтр для поиска
    :param fst_date: String. Дата заезда
    :param sec_date: String. Дата выезда
    :return: Dict. Словарь где ключ - название отеля, значение - адрес и стоимость за ночь
    """

    hotels_dict = dict()
    hotels_list = list()

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": city_id, "pageNumber": "1", "pageSize": hotels_atm, "checkIn": fst_date,
                   "checkOut": sec_date, "adults1": "1", "sortOrder": searching_filter, "locale": "ru_RU",
                   "currency": "RUB"}

    headers = request_settings

    response = requests.request("GET", url, headers=headers, params=querystring)
    req = json.loads(response.text)

    request_dict = req.get('data').get('body').get('searchResults').get('results')

    for i_elem in request_dict:
        hotel_id = i_elem.get('id')
        hotel_name = i_elem.get('name')
        country = i_elem.get('address').get('countryName')
        city = i_elem.get('address').get('locality')

        if i_elem.get('address').get('streetAddress'):
            address = i_elem.get('address').get('streetAddress')
        else:
            address = 'К сожалению не удалось найти адрес данного отеля'

        price = i_elem.get("ratePlan").get("price").get("current")
        hotels_dict[hotel_name] = [f'Адресс {country}, {city}, {address}\n',
                                   f'Цена за выбранный промежуток: {price}\n'
                                   f'Ссылка на отель: https://ru.hotels.com/ho{hotel_id}', hotel_id]

        hotels_list.append(f'{hotel_name} {city} {address}\nЦена за выбранный промежуток: {price}\n'
                           f'Ссылка на отель: https://ru.hotels.com/ho{hotel_id}')
    hotels_for_db = '\n\n'.join(hotels_list)

    if len(hotels_dict) == 0:
        return None

    return hotels_dict, hotels_for_db
