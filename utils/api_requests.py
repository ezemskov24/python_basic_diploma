import requests
import json
import random

from config_data.config import RAPID_API_KEY, RAPID_API_HOST
from loader import bot
from telebot.types import Message, Dict


def api_request_hotel_id(data: dict, message: Message) -> Dict:

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

	response = requests.post(url, json=payload, headers=headers, timeout=15)

	if response.status_code == requests.codes.ok:
		data_hotel = json.loads(response.text)

		try:
			if data_hotel.get("data"):

				hotel_info = dict()
				for i_data in data_hotel["data"]["propertySearch"]["properties"]:
					hotel_info[i_data["id"]] = {
						"name": i_data["name"],
						"price": round(i_data['price']['lead']['amount'], 2),
						"distance": i_data["destinationInfo"]["distanceFromDestination"]["value"]
						}
				return hotel_info

			else:
				bot.send_message(message.chat.id, "Произошла ошибка, повторите выбор команды")

		except KeyError:
			print("Ошибка API запроса")


def api_request_detail(hotel_data: dict):

	print(hotel_data)

		# url_detail = "https://hotels4.p.rapidapi.com/properties/v2/detail"
		#
		# payload_detail = {
		# 	"currency": "USD",
		# 	"eapid": 1,
		# 	"locale": "en_US",
		# 	"siteId": 300000001,
		# 	"propertyId": int(hotel_id)
		# }
		#
		# headers = {
		# 	"content-type": "application/json",
		# 	"X-RapidAPI-Key": RAPID_API_KEY,
		# 	"X-RapidAPI-Host": RAPID_API_HOST
		# }
		#
		# response_detail = requests.post(url_detail, json=payload_detail, headers=headers, timeout=15)
		#
		# if response_detail.status_code == requests.codes.ok:
		#
		# 	data_detail = json.loads(response_detail.text)
		#
		# 	hotel_detail = dict()
		#
		# 	for hotel_info in data_detail["data"]["propertyInfo"]["summary"]:
		# 		address_line = hotel_info["location"]["address"]["addressLine"]
		# 		hotel_detail[hotel_info["id"]] = {
		# 			"address": address_line
		# 		}
		# 	print(hotel_detail)
		# 	return hotel_detail
