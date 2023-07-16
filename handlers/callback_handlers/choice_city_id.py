from loader import bot
from states.states_info import FindInfoState
from telebot.types import CallbackQuery
from handlers.custom_handlers.main_commands import min_price


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def hotel_id(call: CallbackQuery) -> None:

    """
    Обработчик выбора id отеля из встроенной клавиатуры.

    :param call: Объект CallbackQuery, представляющий событие нажатия на кнопку.
    :type call: CallbackQuery
    :return: None
    """

    if call.data:
        bot.set_state(call.message.chat.id, FindInfoState.destinationId)
        with bot.retrieve_data(call.message.chat.id) as data:
            data["destination_id"] = call.data
        bot.set_state(call.message.chat.id, FindInfoState.min_price)
        min_price(call)
    else:
        bot.send_message(call.message.chat.id, "Что-то пошло не так, повторите выбор команды")
