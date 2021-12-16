import requests
import json
from telebot.types import InputMediaPhoto


def id_city_selection(city):

    cities = dict()

    url = "https://hotels4.p.rapidapi.com/locations/search"

    querystring = {"query": f'{city}', "locale": "ru_RU"}

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "17ea7a1a28msh9ea283aba6fcc81p143e6ejsn1db502f95c28"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    req = json.loads(response.text)
    result = req.get('suggestions')

    for cities_info in result:
        for i_city in cities_info['entities']:
            if i_city.get('name') == city:
                address = i_city.get('caption').split(',')
                cities[f'{address[1]}, {i_city["name"]}'] = i_city['destinationId']

    return cities


def lowprice_req(city_id, city_atm, searching_filter):

    hotels_list = dict()

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": city_id, "pageNumber": "1", "pageSize": city_atm, "checkIn": "2021-12-03",
                   "checkOut": "2021-12-12", "adults1": "1", "sortOrder": searching_filter, "locale": "ru_RU",
                   "currency": "RUB"}

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "17ea7a1a28msh9ea283aba6fcc81p143e6ejsn1db502f95c28"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    req = json.loads(response.text)

    request_dict = req.get('data').get('body').get('searchResults').get('results')
    hotel_info = request_dict
    print(hotel_info)

    for i_elem in hotel_info:
        hotel_id = i_elem.get('id')
        hotel_name = i_elem.get('name')
        country = i_elem.get('address').get('countryName')
        city = i_elem.get('address').get('locality')
        address = i_elem.get('address').get('streetAddress')
        price = i_elem.get('ratePlan').get('price').get('current')
        hotels_list[hotel_name] = [country, city, address, price, hotel_id]

    return hotels_list


def get_photo(hotel_id, photo_atm):

    photos_url_list = list()
    media_group = list()

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "17ea7a1a28msh9ea283aba6fcc81p143e6ejsn1db502f95c28"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    result = json.loads(response.text)

    for i_number, i_photo_info in enumerate(result.get('hotelImages')):
        if i_number == int(photo_atm):
            break
        photo_url = i_photo_info.get('baseUrl').format(
            size='z'
        )
        photos_url_list.append(photo_url)

    for i_url in photos_url_list:
        media_group.append(InputMediaPhoto(media=i_url))

    return media_group
