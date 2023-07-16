import re

from telebot.types import Message

from loader import bot
from states.states_info import FindInfoState
from keyboards.inline.city_button import city_markup
from keyboards.inline.need_photo_inline import yes_or_no
from keyboards.inline.calendar import Calendar
from utils.send_message_with_variants import send_message
from handlers.custom_handlers.history import send_data_from_database


@bot.message_handler(commands=["lowprice", "highprice", "bestdeal", "history"], content_types=['text'])
def start_command(message: Message) -> None:

    """
    Обработчик команд, срабатывает на три команды /lowprice, /highprice, /bestdeal
    и запоминает выбранную. Запрашивает у пользователя - какой город искать.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    bot.set_state(message.from_user.id, FindInfoState.command, message.chat.id)
    with bot.retrieve_data(message.chat.id) as data:
        data.clear()
        data["command"] = message.text

    if data["command"] == "/history":
        send_data_from_database(message)

    else:
        bot.set_state(message.from_user.id, FindInfoState.city, message.chat.id)
        if message.from_user.username is not None:
            bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.username}!\n"
                                                   "Введите город, в котором будет производиться поиск.\n"
                                                   "Поиск по городам России временно не производится.")
        else:
            bot.send_message(message.from_user.id, f"Здравствуйте!\n"
                                                   "Введите город, в котором будет производиться поиск.\n"
                                                   "Поиск по городам России временно не производится.")


@bot.message_handler(state=FindInfoState.city)
def get_city(message: Message) -> None:

    """
    Проверяет, ввел ли пользователь допустимые символы,
    после чего вызывается кнопка с предложенным вариантом.
    В случае ошибки просит повторить попытку ввода.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    pattern = r'^[a-zA-Z\s\-]+$'
    if re.match(pattern, message.text):
        with bot.retrieve_data(message.chat.id) as data:
            data["city"] = message.text
        bot.send_message(message.from_user.id, "Выберете один из предложенных вариантов",
                         reply_markup=city_markup(message.text, message))

    else:
        bot.send_message(message.from_user.id, "Что-то пошло не так, попробуйте ввести еще раз")


@bot.message_handler(state=FindInfoState.min_price)
def min_price(message: Message) -> None:

    """
    Ввод минимальной стоимости проживания за сутки.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    bot.send_message(message.from_user.id, "Введите минимальную цену за ночь(в долларах США)")
    bot.set_state(message.from_user.id, FindInfoState.max_price)


@bot.message_handler(state=FindInfoState.max_price)
def max_price(message: Message) -> None:

    """
    Проверяет, ввел ли пользователь целое число.
    В случае ошибки предупреждает об этом и просит ввести еще раз.
    Ввод максимальной стоимости проживания за сутки.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data["min_price"] = message.text
        bot.send_message(message.from_user.id, "Введите максимальную цену за ночь(в долларах США)")
        bot.set_state(message.from_user.id, FindInfoState.input_date, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Ошибка, вы ввели не число.\n"
                                               "Повторите ввод.")


calendar = Calendar()


def my_calendar(message: Message, word: str) -> None:

    """
    Открывает календарь.
    И предлагает выбрать дату заезда / выезда.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :param word: Слово, которое описывает дату (например, "заезда" или "выезда").
    :type word: Str
    :return : None
    """

    bot.send_message(message.chat.id, f'Выберете дату {word}',
                     reply_markup=calendar.create_calendar())


@bot.message_handler(state=FindInfoState.input_date)
def get_date(message: Message) -> None:

    """
    Проверяет, ввел ли пользователь целое число.
    В случае ошибки предупреждает об этом и просит ввести еще раз.
    Проверка на то, чтобы максимальное число было больше минимального.
    Выбор даты заезда.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            if int(data["min_price"]) < int(message.text):
                data["max_price"] = message.text
                my_calendar(message, "заезда")
            else:
                bot.send_message(message.from_user.id, "Максимальная цена не может быть меньше минимальной.\n"
                                                       "Повторите ввод")
    else:
        bot.send_message(message.from_user.id, "Ошибка, вы ввели не число.\n"
                                               "Повторите ввод.")


@bot.message_handler(state=FindInfoState.distance_from)
def distance_from(message: Message) -> None:

    """
    Ввод пользователем минимального расстояния до центра.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    bot.send_message(message.from_user.id, "Введите минимальное расстояние до центра(в милях)")
    bot.set_state(message.from_user.id, FindInfoState.distance_to)


@bot.message_handler(state=FindInfoState.distance_to)
def distance_to(message: Message) -> None:

    """
    Проверяет, ввел ли пользователь целое число.
    В случае ошибки предупреждает об этом и просит ввести еще раз.
    Ввод пользователем максимального расстояния до центра.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data["distance_from"] = message.text
        bot.send_message(message.from_user.id, "Введите максимальное расстояние до центра(в милях)")
        bot.set_state(message.from_user.id, FindInfoState.total_distance)
    else:
        bot.send_message(message.from_user.id, "Ошибка, вы ввели не число.\n"
                                               "Повторите ввод.")


@bot.message_handler(state=FindInfoState.total_distance)
def get_hotel_count_with_distance(message: Message) -> None:

    """
    Запускается в случае, если была выбрана команда bestdeal.
    Проверяет, ввел ли пользователь целое число.
    В случае ошибки предупреждает об этом и просит ввести еще раз.
    Проверка на то, чтобы максимальное число было больше минимального.
    Ввод пользователем количества предлагаемых вариантов.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            if float(data["distance_from"]) < float(message.text):
                data["distance_to"] = message.text
                bot.send_message(message.from_user.id, "Сколько вариантов показать? (Не больше 10)")
                bot.set_state(message.from_user.id, FindInfoState.need_photo)
            else:
                bot.send_message(message.from_user.id, "Максимальная дистанция не может быть меньше минимальной.\n"
                                                       "Повторите ввод.")


@bot.message_handler(state=FindInfoState.hotel_count)
def get_hotel_count(message: Message) -> None:

    """
    Запускается в случае, если была выбрана команда lowprice или highprice.
    Ввод пользователем количества предлагаемых вариантов.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    bot.send_message(message.from_user.id, "Сколько вариантов показать? (Не больше 10)")
    bot.set_state(message.from_user.id, FindInfoState.need_photo)


@bot.message_handler(state=FindInfoState.need_photo)
def need_photo(message: Message) -> None:

    """
    Проверяет, ввел ли пользователь целое число не больше 10.
    В случае ошибки предупреждает об этом и просит ввести еще раз.
    Предлагает показать фото отелей.
    Запускается кнопка с вариантами "Да" и "Нет".

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    if message.text.isdigit() and int(message.text) <= 10:
        with bot.retrieve_data(message.chat.id) as data:
            data["hotel_variants"] = message.text
        bot.send_message(message.from_user.id, "Загрузить фото отелей?", reply_markup=yes_or_no())
    else:
        bot.send_message(message.from_user.id, "Вы указали неверное значение.\n"
                                               "Повторите ввод.")


@bot.message_handler(state=FindInfoState.how_many_photo)
def how_many_photo(message: Message) -> None:

    """
    Проверяет, ввел ли пользователь целое число не больше 10.
    В случае ошибки предупреждает об этом и просит ввести еще раз.
    Отправляет сообщение пользователю с тем, какие варианты он ранее указал.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

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
               f"{data['checkOutDate']['day']}.{data['checkOutDate']['month']}.{data['checkOutDate']['year']}\n" \
               f"Количество ночей: {data['count_days']}\n" \
               f"Количество вариантов: {data['hotel_variants']}\n" \
               f"Количество фотографий: {data['count_photo']}"

        bot.send_message(message.from_user.id, text)
        send_message(data, message)

    else:
        bot.send_message(message.from_user.id, "Вы ввели неверное значение.\n"
                                               "Повторите ввод.")
