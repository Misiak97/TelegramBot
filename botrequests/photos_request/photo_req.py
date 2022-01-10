from telebot.types import InputMediaPhoto
import json
import requests
import os
from dotenv import load_dotenv


load_dotenv()

req_key = os.getenv('REQUEST_KEY')

request_settings = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': req_key
        }


def get_photo(hotel_id, photo_atm):

    photos_url_list = list()
    media_group = list()

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    headers = request_settings

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
