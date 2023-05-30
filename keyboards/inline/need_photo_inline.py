from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_or_no() -> InlineKeyboardMarkup:
    yes_or_no_button = InlineKeyboardMarkup()
    yes_or_no_button.add(InlineKeyboardButton(text="Да", callback_data="yes"),
                         InlineKeyboardButton(text="Нет", callback_data="no"))
    return yes_or_no_button
