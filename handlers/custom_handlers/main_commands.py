from telebot.types import Message

from loader import bot
from states.states_info import FindInfoState
from keyboards.inline.city_button import city_markup
from keyboards.inline.need_photo_inline import yes_or_no
from keyboards.inline.calendar import Calendar
from utils.send_message_with_variants import send_message


@bot.message_handler(commands=["lowprice", "highprice", "bestdeal"], content_types=['text'])
def low_price(message: Message) -> None:
    bot.set_state(message.from_user.id, FindInfoState.command, message.chat.id)
    with bot.retrieve_data(message.chat.id) as data:
        data["command"] = message.text
        data["sort"] = check_command(message.text)
    bot.set_state(message.from_user.id, FindInfoState.city, message.chat.id)
    bot.send_message(message.from_user.id, "Введите город, в котором будет производиться поиск.\n"
                                           "Поиск по городам России временно не производится.")


def check_command(command: str) -> str:
    if command == "/lowprice" or command == "/highprice":
        return "PRICE_LOW_TO_HIGH"

    elif command == "/bestdeal":
        return "DISTANCE"


@bot.message_handler(state=FindInfoState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        with bot.retrieve_data(message.chat.id) as data:
            data["city"] = message.text
        bot.send_message(message.from_user.id, "Выберете один из предложенных вариантов",
                         reply_markup=city_markup(message.text, message))

    else:
        bot.send_message(message.from_user.id, "Что-то пошло не так, попробуйте ввести еще раз")


@bot.message_handler(state=FindInfoState.min_price)
def min_price(message: Message) -> None:
    bot.send_message(message.from_user.id, "Введите минимальную цену за ночь(в долларах США)")
    bot.set_state(message.from_user.id, FindInfoState.max_price)


@bot.message_handler(state=FindInfoState.max_price)
def max_price(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data["min_price"] = message.text
        bot.send_message(message.from_user.id, "Введите максимальную цену за ночь(в долларах США)")
        bot.set_state(message.from_user.id, FindInfoState.input_date, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Ошибка, вы ввели не число")


calendar = Calendar()


def my_calendar(message: Message, word: str) -> None:
    bot.send_message(message.chat.id, f'Выберете дату {word}',
                     reply_markup=calendar.create_calendar())


@bot.message_handler(state=FindInfoState.input_date)
def get_date(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            if int(data["min_price"]) < int(message.text):
                data["max_price"] = message.text
                my_calendar(message, "заезда")
            else:
                bot.send_message(message.from_user.id, "Максимальная цена не может быть меньше минимальной. "
                                                       "Повторите ввод")
    else:
        bot.send_message(message.from_user.id, "Ошибка, вы ввели не число")


@bot.message_handler(state=FindInfoState.distance_from)
def distance_from(message: Message) -> None:
    bot.send_message(message.from_user.id, "Введите минимальное расстояние до центра(в милях)")
    bot.set_state(message.from_user.id, FindInfoState.distance_to)


@bot.message_handler(state=FindInfoState.distance_to)
def distance_to(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data["distance_from"] = message.text
        bot.send_message(message.from_user.id, "Введите максимальное расстояние до центра(в милях)")
        bot.set_state(message.from_user.id, FindInfoState.total_distance)
    else:
        bot.send_message(message.from_user.id, "Ошибка, вы ввели не число")


@bot.message_handler(state=FindInfoState.total_distance)
def get_hotel_count_with_distance(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            if float(data["distance_from"]) < float(message.text):
                data["distance_to"] = message.text
                bot.send_message(message.from_user.id, "Сколько вариантов показать? (Не больше 10)")
                bot.set_state(message.from_user.id, FindInfoState.need_photo)
            else:
                bot.send_message(message.from_user.id, "Максимальная дистанция не может быть меньше минимальной. "
                                                       "Повторите ввод")


@bot.message_handler(state=FindInfoState.hotel_count)
def get_hotel_count(message: Message) -> None:
    bot.send_message(message.from_user.id, "Сколько вариантов показать? (Не больше 10)")
    bot.set_state(message.from_user.id, FindInfoState.need_photo)


@bot.message_handler(state=FindInfoState.need_photo)
def need_photo(message: Message) -> None:
    if message.text.isdigit() and int(message.text) <= 10:
        with bot.retrieve_data(message.chat.id) as data:
            data["hotel_variants"] = message.text
        bot.send_message(message.from_user.id, "Загрузить фото отелей?", reply_markup=yes_or_no())
    else:
        bot.send_message(message.from_user.id, "Вы указали неверное значение")


@bot.message_handler(state=FindInfoState.how_many_photo)
def how_many_photo(message: Message):
    if message.text.isdigit() and int(message.text) <= 10:
        with bot.retrieve_data(message.chat.id) as data:
            data["count_photo"] = message.text

        text = "Вы выбрали:\n" \
               f"Город: {data['city'].title()}\n" \
               f"Минимальная цена за ночь: {data['min_price']}$\n" \
               f"Максимальная цена за ночь: {data['max_price']}$\n" \
               f"Дата заезда: " \
               f"{data['checkInDate']['day']}.{data['checkInDate']['month']}.{data['checkInDate']['year']}\n" \
               f"Дата выезда: " \
               f"{data['checkOutDate']['day']}.{data['checkOutDate']['month']}.{data['checkOutDate']['year']}\n\n"
        bot.send_message(message.from_user.id, text)
        send_message(data, message)

    else:
        bot.send_message(message.from_user.id, "Вы ввели неверное значение")
