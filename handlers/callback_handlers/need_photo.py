from loader import bot
from states.states_info import FindInfoState
from telebot.types import CallbackQuery, Message
from utils.send_message_with_variants import send_message


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
        
        text = "Вы выбрали:\n" \
               f"Город: {data['city'].title()}\n" \
               f"Минимальная цена за ночь: {data['min_price']}$\n" \
               f"Максимальная цена за ночь: {data['max_price']}$\n" \
               f"Дата заезда: " \
               f"{data['checkInDate']['day']}.{data['checkInDate']['month']}.{data['checkInDate']['year']}\n" \
               f"Дата выезда: " \
               f"{data['checkOutDate']['day']}.{data['checkOutDate']['month']}.{data['checkOutDate']['year']}\n\n"
        bot.send_message(call.from_user.id, text)

        send_message(data, call.message)
