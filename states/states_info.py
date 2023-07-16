from telebot.handler_backends import State, StatesGroup


class FindInfoState(StatesGroup):

    """
    Состояния пользователя внутри сценария.
    """

    command = State()
    city = State()
    destinationId = State()
    min_price = State()
    max_price = State()
    input_date = State()
    distance_from = State()
    distance_to = State()
    total_distance = State()
    hotel_count = State()
    need_photo = State()
    how_many_photo = State()

