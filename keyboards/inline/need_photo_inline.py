from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_or_no() -> InlineKeyboardMarkup:

    """
    Создает встроенную клавиатуру с кнопками "Да" и "Нет".

    :return: Встроенная клавиатура с кнопками "Да" и "Нет".
    :rtype: InlineKeyboardMarkup
    """

    yes_or_no_button = InlineKeyboardMarkup()
    yes_or_no_button.add(InlineKeyboardButton(text="Да", callback_data="yes"),
                         InlineKeyboardButton(text="Нет", callback_data="no"))
    return yes_or_no_button
