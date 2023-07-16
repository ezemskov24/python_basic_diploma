import ast

from telebot.types import Message
from loader import bot
from database.models import *


@bot.message_handler(commands=["history"], content_types=['text'])
def send_data_from_database(message: Message) -> None:

    """
    Отправляет пользователю данные из базы данных по истории поиска.
    В случае отсутствия id пользователя в БД, предупреждает, что него еще нет истории поиска.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return: None
    """

    user_id = message.from_user.id

    with db:
        my_history = History.select().where(History.user_id == str(user_id))

        if my_history:
            history_text = "Ваша история поиска:\n"

            for item in my_history:
                hotel_names_list = ast.literal_eval(item.hotel_names)

                text = f"Вы выбрали команду: {item.command}\n" \
                       f"Время запроса: {item.date_time}\n" \
                       f"Показанные отели: {', '.join(hotel_names_list)}\n"

                history_text += text + '\n'

            bot.send_message(message.chat.id, history_text)

        else:
            bot.send_message(message.chat.id, "У вас нет истории поиска")


if __name__ == '__main__':
    send_data_from_database()
