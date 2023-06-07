import requests
import keyboards.inline
import datetime

from keyboards.inline.city_button import city_markup
from keyboards.inline.need_photo_inline import yes_or_no
from loader import bot
from states.states_info import FindInfoState
from telebot.types import Message
from datetime import datetime
from keyboards.inline.calendar import CallbackData, Calendar
from telebot.types import CallbackQuery


@bot.message_handler(commands=["lowprice"], content_types=['text'])
def low_price(message: Message) -> None:

    bot.set_state(message.from_user.id, FindInfoState.city, message.chat.id)
    bot.send_message(message.from_user.id, "Введите город, в котором будет производиться поиск")


@bot.message_handler(state=FindInfoState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        with bot.retrieve_data(message.chat.id) as data:
            data["city"] = message.text
        bot.send_message(message.from_user.id, "Выберете один из предложенных вариантов",
                         reply_markup=city_markup(message.text))

    else:
        bot.send_message(message.from_user.id, "Что-то пошло не так, попробуйте ввести еще раз")


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def hotel_id(call):
    if call.data:
        bot.set_state(call.message.chat.id, FindInfoState.destinationId)
        with bot.retrieve_data(call.message.chat.id) as data:
            data["destination_id"] = call.data
        bot.set_state(call.message.chat.id, FindInfoState.min_price)
        bot.send_message(call.message.chat.id, "Введите минимальную цену за ночь")
        bot.set_state(call.from_user.id, FindInfoState.max_price)


@bot.message_handler(state=FindInfoState.max_price)
def min_price(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data["min_price"] = message.text
        bot.send_message(message.from_user.id, "Введите максимальную цену за ночь")
        bot.set_state(message.from_user.id, FindInfoState.hotel_count, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Ошибка, вы ввели не число")


calendar = Calendar()


def my_calendar(message: Message, word: str) -> None:
    bot.send_message(message.from_user.id, f'Введите дату {word}',
                     reply_markup=calendar.create_calendar())


@bot.message_handler(state=FindInfoState.hotel_count)
def get_hotel_count(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            if int(data["min_price"]) < int(message.text):
                data["max_price"] = message.text
            else:
                bot.send_message(message.from_user.id, "Максимальная цена не может быть меньше минимальной. "
                                                       "Повторите ввод")
        my_calendar(message, "заезда")
        # bot.send_message(message.from_user.id, "Сколько вариантов показать? Но не больше 10")
        # bot.set_state(message.from_user.id, FindInfoState.need_photo, message.chat.id)

    else:
        bot.send_message(message.from_user.id, "Ошибка, вы ввели не число")



@bot.message_handler(state=FindInfoState.need_photo)
def need_photo(message: Message) -> None:
    if message.text.isdigit() and int(message.text) <= 10:
        bot.send_message(message.from_user.id, "Загрузить фото отелей?", reply_markup=yes_or_no())
        bot.set_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Вы указали неверное значение")


@bot.callback_query_handler(func=lambda call: True)
def photo_amount(call) -> None:
    if call.data == "yes":
        bot.send_message(call.from_user.id, "Сколько фотографий вывести. Но не больше 10")
        bot.set_state(call.from_user.id, FindInfoState.how_many_photo)
    elif call.data == "no":
        bot.send_message(call.from_user.id, "Результат согласно вашего запроса")


@bot.message_handler(state=FindInfoState.how_many_photo)
def how_many_photo(message: Message) -> None:
    if message.text.isdigit() and int(message.text) <= 10:
        bot.send_message(message.from_user.id, "Результат согласно вашего запроса")
    else:
        bot.send_message(message.from_user.id, "Вы ввели неверное значение")

