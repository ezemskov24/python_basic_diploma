import datetime

import handlers.custom_handlers.main_commands

from loader import bot
from states.states_info import FindInfoState
from keyboards.inline.calendar import CallbackData, Calendar
from telebot.types import CallbackQuery
from handlers.custom_handlers.main_commands import distance_from, get_hotel_count


calendar = Calendar()
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")


def check_month_day(number: str) -> str:

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if int(number) in numbers:
        number = '0' + number
    return number


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def input_date(call: CallbackQuery) -> None:

    name, action, year, month, day = call.data.split(calendar_callback.sep)
    calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)

    if action == 'DAY':
        month = check_month_day(month)
        day = check_month_day(day)
        select_date = year + month + day

        now_year, now_month, now_day = datetime.datetime.now().strftime('%Y.%m.%d').split('.')
        now = now_year + now_month + now_day

        bot.set_state(call.message.chat.id, FindInfoState.input_date)
        with bot.retrieve_data(call.message.chat.id) as data:
            if 'checkInDate' in data:
                checkin = int(data['checkInDate']['year'] + data['checkInDate']['month'] + data['checkInDate']['day'])
                if int(select_date) > checkin:

                    data['checkOutDate'] = {'day': day, 'month': month, 'year': year}
                    bot.send_message(call.message.chat.id, f'Дата выезда: {day + "." + month + "." + year}')
                    if data["sort"] == "DISTANCE":
                        bot.set_state(call.message.chat.id, FindInfoState.distance_from)
                        distance_from(call)
                    else:
                        bot.set_state(call.message.chat.id, FindInfoState.hotel_count)
                        get_hotel_count(call)

                else:
                    bot.send_message(call.message.chat.id, 'Дата выезда не может быть раньше даты заезда! '
                                                           'Повторите выбор даты!')
                    handlers.custom_handlers.main_commands.my_calendar(call.message, 'выезда')
            else:
                if int(select_date) >= int(now):
                    data['checkInDate'] = {'day': day, 'month': month, 'year': year}
                    bot.send_message(call.message.chat.id, f'Дата заезда: {day + "." + month + "." + year}')
                    handlers.custom_handlers.main_commands.my_calendar(call.message, 'выезда')
                else:
                    bot.send_message(call.message.chat.id, 'Дата выезда не может быть раньше сегодняшней даты!'
                                                           'Повторите выбор даты!')
                    handlers.custom_handlers.main_commands.my_calendar(call.message, 'заезда')
