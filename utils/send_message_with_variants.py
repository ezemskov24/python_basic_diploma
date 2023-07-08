import random
import requests
from io import BytesIO

from telebot.types import Message

from loader import bot
from utils.api_requests import api_request_hotel_id, api_request_detail


def send_message(data: dict, message: Message):
    result_id = api_request_hotel_id(data, message)
    result_detail = api_request_detail(result_id, data, message)

    for key in result_detail:
        result_detail[key].update(result_id[key])

    for hotel_key in result_detail:
        hotel = result_detail[hotel_key]
        images = random.sample(hotel["images"], int(data["count_photo"]))

        message_text = f"Название отеля: {hotel['name']}\n" \
                       f"Адрес: {hotel['address']}\n" \
                       f"Расстояние от центра: {hotel['distance']} миль\n" \
                       f"Сумма проживания: {hotel['price']} $\n"

        bot.send_message(message.chat.id, message_text)

        for image_url in images:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image_data.seek(0)
                bot.send_photo(message.chat.id, photo=image_data)


