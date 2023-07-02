import requests
import json
import random

from config_data.config import RAPID_API_KEY, RAPID_API_HOST
from loader import bot
from telebot.types import Message, Dict


def api_request_hotel_id(data: dict) -> Dict:

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

		hotel_info = dict()
		for i_data in data_hotel["data"]["propertySearch"]["properties"]:
			try:
				hotel_info[i_data["id"]] = {
					"name": i_data["name"],
					"price": round(i_data['price']['lead']['amount'], 2),
					"distance": i_data["destinationInfo"]["distanceFromDestination"]["value"]
				}
			except (KeyError, TypeError):
				continue

		return hotel_info


def api_request_detail(hotel_data: dict, data: dict, message: Message):

	count = 0

	for hotel_id in list(hotel_data.keys()):

		while count < int(data["hotel_variants"]):

			count += 1

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

				for i_data in data_detail["data"]["propertyInfo"]["summary"]:

					hotel_data[hotel_id] = {"address": i_data["location"]["addressLine"]}
					bot.send_message(message.chat.id, "Творится магия")

		else:
			break

