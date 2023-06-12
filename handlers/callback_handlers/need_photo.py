from loader import bot
from states.states_info import FindInfoState
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda call: call.data.isalpha())
def photo_amount(call: CallbackQuery) -> None:
    if call.data == "yes":
        with bot.retrieve_data(call.message.chat.id) as data:
            data["need_photo"] = call.data
        bot.send_message(call.message.chat.id, "Сколько фотографий вывести. Но не больше 10")
        bot.set_state(call.message.chat.id, FindInfoState.how_many_photo)

    elif call.data == "no":
        with bot.retrieve_data(call.message.chat.id) as data:
            data["need_photo"] = call.data
            data["count_photo"] = 0
        bot.send_message(call.message.chat.id, "Результат согласно вашего запроса")
