import random
from datetime import datetime

from telebot.types import Message, InputMediaPhoto

from loader import bot
from utils.api_requests import api_request_hotel_id, api_request_detail
from database.models import *


def send_message(data: dict, message: Message):
    result_id = api_request_hotel_id(data, message)
    result_detail = api_request_detail(result_id, data, message)



    for key in result_detail:
        result_detail[key].update(result_id[key])

    if data["command"] == "/lowprice":
        result_detail = sorted(result_detail.items(), key=lambda x: x[1]["price"])

    elif data["command"] == "/highprice":
        result_detail = sorted(result_detail.items(), key=lambda x: x[1]["price"], reverse=True)

    elif data["command"] == "/bestdeal":
        result_detail = sorted(result_detail.items(), key=lambda x: (x[1]["distance"], x[1]["price"]))

    with bot.retrieve_data(message.chat.id) as data:
        data["hotel_name"] = list()

        for hotel_key, hotel in result_detail:
            images = random.sample(hotel["images"], int(data["count_photo"]))

            data["hotel_name"].append(hotel['name'])

            message_text = f"Название отеля: {hotel['name']}\n" \
                           f"Адрес: {hotel['address']}\n" \
                           f"Расстояние до центра: {hotel['distance']} миль\n" \
                           f"Цена за ночь: {hotel['price']} $\n" \
                           f"Сумма проживания: {float(hotel['price']) * int(data['count_days'])} $\n"

            bot.send_message(message.chat.id, message_text)

            media_group = list()
            for image_url in images:
                media_group.append(InputMediaPhoto(image_url))

            if media_group:
                bot.send_media_group(message.chat.id, media=media_group)

    now = datetime.now()
    formatted_datetime = now.strftime("%d.%m.%Y %H:%M:%S")

    History(
        user_id=message.from_user.id,
        date_time=formatted_datetime,
        user_name=message.from_user.username,
        command=data["command"],
        city=data["city"],
        min_price=data["min_price"],
        max_price=data["max_price"],
        check_in_date=
        f"{data['checkInDate']['day']}.{data['checkInDate']['month']}.{data['checkInDate']['year']}",
        check_out_date=
        f"{data['checkOutDate']['day']}.{data['checkOutDate']['month']}.{data['checkOutDate']['year']}",
        distance_from=data["distance_from"],
        distance_to=data["distance_to"],
        hotel_variants=data["hotel_variants"],
        need_photo=data["need_photo"],
        count_photo=data["count_photo"],
        hotel_names=data["hotel_name"]
    ).save()
