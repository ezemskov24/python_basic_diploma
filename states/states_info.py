from telebot.handler_backends import State, StatesGroup


class FindInfoState(StatesGroup):
    city = State()
    destinationId = State()
    min_price = State()
    max_price = State()
    input_date = State()
    hotel_count = State()
    need_photo = State()
    how_many_photo = State()

