from telebot.handler_backends import State, StatesGroup


class FindInfoState(StatesGroup):
    city = State()
    min_price = State()
    max_price = State()
    hotel_count = State()
    need_photo = State()
    how_many_photo = State()

