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


def bestdeal_req(city_id, hotels_atm, fst_date, sec_date, distance, min_price, max_price):
    hotels_list = dict()

    needed_distance = distance

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {
        "destinationId": city_id, "pageNumber": "1", "pageSize": hotels_atm, "checkIn": fst_date,
        "checkOut": sec_date, "adults1": "1", "priceMin": min_price, "priceMax": max_price,
        "locale": "ru_RU", "currency": "RUB"
    }

    headers = request_settings

    response = requests.request("GET", url, headers=headers, params=querystring)
    req = json.loads(response.text)

    request_dict = req.get('data').get('body').get('searchResults').get('results')
    hotel_info = request_dict

    for i_elem in hotel_info:
        distance_to_center = i_elem.get('landmarks')[0].get('distance').split(' ')[0]
        if ',' in distance_to_center:
            needed_sym = distance_to_center.index(',')
            distance_to_center = distance_to_center[:needed_sym] + '.' + distance_to_center[needed_sym + 1:]

        if float(needed_distance) >= float(distance_to_center):
            hotel_id = i_elem.get('id')
            hotel_name = i_elem.get('name')
            country = i_elem.get('address').get('countryName')
            city = i_elem.get('address').get('locality')

            if i_elem.get('address').get('streetAddress'):
                address = i_elem.get('address').get('streetAddress')
            else:
                address = 'К сожалению не удалось найти адрес данного отеля'

            price = i_elem.get("ratePlan").get("price").get("current")
            hotels_list[hotel_name] = [f'Адресс {country}, {city}, {address}\n',
                                       f'Цена за выбранный промежуток: {price}\n'
                                       f'Расстояние до центра {distance_to_center} км.', hotel_id]

    if len(hotels_list) == 0:
        return 'К сожалению по данному запросу найти отели не удалось'

    return hotels_list
