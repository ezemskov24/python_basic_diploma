from loader import bot
from states.states_info import FindInfoState
from telebot.types import CallbackQuery
from utils.api_requests import api_request_hotel_id


@bot.callback_query_handler(func=lambda call: call.data.isalpha())
def photo_amount(call: CallbackQuery) -> None:
    if call.data == "yes":
        with bot.retrieve_data(call.message.chat.id) as data:
            data["need_photo"] = call.data
        bot.send_message(call.message.chat.id, "Сколько фотографий показать? (Не больше 10)")
        bot.set_state(call.message.chat.id, FindInfoState.how_many_photo)

    elif call.data == "no":
        with bot.retrieve_data(call.message.chat.id) as data:
            data["need_photo"] = call.data
            data["count_photo"] = 0
        bot.send_message(call.message.chat.id, "На этом пока все, но работа продолжается")
        api_request_hotel_id(data)
