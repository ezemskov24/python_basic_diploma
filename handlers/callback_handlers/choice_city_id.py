from loader import bot
from states.states_info import FindInfoState
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def hotel_id(call: CallbackQuery) -> None:
    if call.data:
        bot.set_state(call.message.chat.id, FindInfoState.destinationId)
        with bot.retrieve_data(call.message.chat.id) as data:
            data["destination_id"] = call.data
        bot.set_state(call.message.chat.id, FindInfoState.min_price)
        bot.send_message(call.message.chat.id, "Введите минимальную цену за ночь")
        bot.set_state(call.from_user.id, FindInfoState.max_price)