from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):

    """
    Отвечает пользователю на сообщение "Привет".
    Если пользователь ввел что-то другое, то просит выбрать команду.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return : None
    """

    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "И вам привет")

    else:
        bot.send_message(message.chat.id, "Выберете одну из команд")
