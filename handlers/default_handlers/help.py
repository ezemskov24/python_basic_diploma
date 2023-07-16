from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:

    """
    Отправляет пользователю список доступных команд с их описанием.

    :param message: Объект сообщения от пользователя.
    :type message: Message
    :return: None
    """

    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
