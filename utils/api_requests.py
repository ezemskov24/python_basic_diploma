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
		"destination": {
			"regionId": data["destination_id"]
			},
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
				"adults": 1,
			}
		],
		"resultsStartingIndex": 0,
		"resultsSize": 10,
		"sort": data["sort"],
		"filters": {"price": {
			"max": data["max_price"],
			"min": data["min_price"]
		}}
	}

	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": RAPID_API_KEY,
		"X-RapidAPI-Host": RAPID_API_HOST
	}

	response = requests.post(url, json=payload, headers=headers, timeout=15)

	if response.status_code == requests.codes.ok:
		data_hotel = json.loads(response.text)

		hotel_info = dict()

		try:

			if "data" in data_hotel and isinstance(data_hotel["data"], dict):

				for i_data in data_hotel["data"]["propertySearch"]["properties"]:
					hotel_info[i_data["id"]] = {
						"name": i_data["name"],
						"price": round(i_data['price']['lead']['amount'], 2),
						"distance": i_data["destinationInfo"]["distanceFromDestination"]["value"]
						}

				return hotel_info

			else:
				bot.send_message(message.chat.id, "Произошла ошибка, повторите выбор команды")
				raise SystemExit

		except KeyError:
			print("Ошибка запроса")

	else:
		print("Ошибка при выполнении запроса:", response.status_code)


def api_request_detail(hotel_data: dict, data: dict, message: Message):

	hotel_variants = int(data["hotel_variants"])
	hotel_keys = list(hotel_data.keys())

	if hotel_variants <= 0 or hotel_variants > len(hotel_data):
		bot.send_message(message.chat.id, "Произошла ошибка, повторите команду с другими параметрами")

	else:

		random_keys = random.sample(hotel_keys, hotel_variants)
		hotel_detail = dict()

		for hotel_id in random_keys:

			url_detail = "https://hotels4.p.rapidapi.com/properties/v2/detail"

			payload_detail = {
				"currency": "USD",
				"eapid": 1,
				"locale": "en_US",
				"siteId": 300000001,
				"propertyId": hotel_id
			}

			headers = {
				"content-type": "application/json",
				"X-RapidAPI-Key": RAPID_API_KEY,
				"X-RapidAPI-Host": RAPID_API_HOST
			}

			response_detail = requests.post(url_detail, json=payload_detail, headers=headers, timeout=15)

			if response_detail.status_code == requests.codes.ok:

				data_detail = json.loads(response_detail.text)

				try:
					summary = data_detail["data"]["propertyInfo"]["summary"]
					address_line = summary["location"]["address"]["addressLine"]

					image_urls = list()
					for image_data in data_detail["data"]["propertyInfo"]["propertyGallery"]["images"]:
						image_url = image_data["image"]["url"]
						image_urls.append(image_url)

					hotel_detail[summary["id"]] = {
						"address": address_line,
						"images": image_urls
					}

				except KeyError:
					print("Ошибка запроса")

			else:
				print("Ошибка при выполнении запроса:", response_detail.status_code)

		return hotel_detail
