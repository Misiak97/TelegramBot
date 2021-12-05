import requests
import json


url = "https://hotels4.p.rapidapi.com/locations/search"

querystring = {"query": "Samara", "locale": "Ru_ru"}

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': "17ea7a1a28msh9ea283aba6fcc81p143e6ejsn1db502f95c28"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

url = "https://hotels4.p.rapidapi.com/properties/list"

querystring = {"destinationId": "1161981", "pageNumber": "1", "pageSize": "25", "checkIn": "2021-12-03",
               "checkOut": "2021-12-12", "adults1": "1", "sortOrder": "PRICE", "locale": "ru", "currency": "RUB"}

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': "17ea7a1a28msh9ea283aba6fcc81p143e6ejsn1db502f95c28"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
req = json.loads(response.text)

with open('req.json', 'w', encoding='utf-8') as file:
    json.dump(req, file, indent=4, ensure_ascii=False)


