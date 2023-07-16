import requests
import json
import random
from loguru import logger

from config_data.config import RAPID_API_KEY, RAPID_API_HOST
from loader import bot
from telebot.types import Message, Dict


def api_request_hotel_id(data: dict, message: Message, attempts=3) -> Dict:

    """
    Выполняет запрос к API для получения информации о доступных отелях.

    :param data: Словарь с данными для запроса.
    :type data: Dict
    :param message: Объект сообщения от пользователя.
    :type message: Message
    :param attempts: Количество попыток выполнения запроса (по умолчанию 3).
    :type attempts: Int
    :return: Словарь с информацией о доступных отелях.
    :rtype: Dict
    """

    if attempts <= 0:
        bot.send_message(message.chat.id, "Произошла ошибка, повторите выбор команды")
        raise SystemExit

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
                "adults": 2,
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": int(data["max_price"]),
            "min": int(data["min_price"])
        }}
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)

    if response.status_code == requests.codes.ok:
        logger.info(f"Ответ сервера: {response.status_code}")
        data_hotel = json.loads(response.text)
        logger.info(f"Ключи в словаре: {data_hotel.keys()}")

        hotel_info = dict()

        if "data" in data_hotel and isinstance(data_hotel["data"], dict):

            for i_data in data_hotel["data"]["propertySearch"]["properties"]:
                hotel_info[i_data["id"]] = {
                    "name": i_data["name"],
                    "price": round(i_data['price']['lead']['amount'], 2),
                    "distance": i_data["destinationInfo"]["distanceFromDestination"]["value"]
                }

            if data["command"] == "/bestdeal":

                distance_from = int(data["distance_from"])
                distance_to = int(data["distance_to"])
                hotels_for_del = list()

                for hotel_id, hotel_data in hotel_info.items():
                    distance = hotel_data["distance"]
                    if not (distance_from < float(distance) < distance_to):
                        hotels_for_del.append(hotel_id)

                for hotel_id in hotels_for_del:
                    del hotel_info[hotel_id]

            return hotel_info

        else:
            return api_request_hotel_id(data, message, attempts - 1)

    else:
        logger.info(f"Ошибка при выполнении запроса: {response.status_code}")
        raise SystemExit


def api_request_detail(hotel_data: dict, data: dict, message: Message) -> Dict:

    """
    Выполняет запрос к API для получения детальной информации о выбранных отелях.

    :param hotel_data: Словарь с информацией о доступных отелях.
    :type hotel_data: Dict
    :param data: Словарь с данными для запроса.
    :type data: Dict
    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return: Словарь с детальной информацией о выбранных отелях.
    :rtype: Dict
    """

    hotel_variants = int(data["hotel_variants"])
    hotel_keys = list(hotel_data.keys())
    logger.info(f"Ключей в словаре: {len(hotel_data.keys())}")

    if hotel_variants <= 0 or hotel_variants > len(hotel_data):
        bot.send_message(message.chat.id, "Не удалось найти варианты с заданными параметрами.\n"
                                          "Повторите команду с другими значениями")
        raise SystemExit

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
                logger.info(f"Ответ сервера: {response_detail.status_code}")

                data_detail = json.loads(response_detail.text)

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

            else:
                logger.info(f"Ошибка при выполнении запроса: {response_detail.status_code}")
                raise SystemExit

        return hotel_detail
