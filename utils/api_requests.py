import requests
import json

from config_data.config import RAPID_API_KEY, RAPID_API_HOST
from loader import bot
from telebot.types import Message


def api_request_hotel_id(message: Message, data: dict):

	url = "https://hotels4.p.rapidapi.com/properties/v2/list"

	payload = {
		"currency": "USD",
		"eapid": 1,
		"locale": "en_US",
		"siteId": 300000001,
		"destination": { "regionId": data["destination_id"] },
		"checkInDate": {
			"day": int(data['checkInDate']['day']),
			"month": int(data['checkInDate']['month']),
			"year": int(data['checkInDate']['year'])
		},
		"checkOutDate": {
			"day": int(data['checkOutDate']['day']),
			"month": int(data['checkOutDate']['month']),
			"year": int(data['checkOutDate']['year'])
		},
		"rooms": [
			{
				"adults": 2,
				"children": [{ "age": 5 }, { "age": 7 }]
			}
		],
		"resultsStartingIndex": 0,
		"resultsSize": 200,
		"sort": data["sort"],
		"filters": { "price": {
				"max": int(data["max_price"]),
				"min": int(data["min_price"])
			} }
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": RAPID_API_KEY,
		"X-RapidAPI-Host": RAPID_API_HOST
	}

	response = requests.post(url, json=payload, headers=headers, timeout=10)

	if response.status_code == requests.codes.ok:
		data = response.json()
		hotels = list()
		for i_data in data["data"]["propertySearch"]["properties"]:
			hotels.append(i_data["id"])

		for hotel in hotels:

			url_detail = "https://hotels4.p.rapidapi.com/properties/v2/detail"

			payload_detail = {
				"currency": "USD",
				"eapid": 1,
				"locale": "en_US",
				"siteId": 300000001,
				"propertyId": hotel
			}

			response_detail = requests.post(url_detail, json=payload_detail, headers=headers, timeout=10)

			if response_detail.status_code == requests.codes.ok:

				data_hotel = response_detail.json()

				for _ in data_hotel:
					hotel_info = {"name": data_hotel["data"]["propertyInfo"]["summary"]["name"]}
					bot.send_message(message.chat.id, hotel_info.values())


