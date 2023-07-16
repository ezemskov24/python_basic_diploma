from peewee import *


db = SqliteDatabase('telegram_bot.db')


class BaseModel(Model):
    class Meta:
        database = db


class History(BaseModel):

    """
    Модель для хранения истории запросов пользователя.

    :param user_id: Id пользователя.
    :type user_id: Str
    :param date_time: Дата и время запроса.
    :type date_time: Str
    :param user_name: Имя пользователя (может быть пустым).
    :type user_name: Str or None
    :param command: Выбранная команда.
    :type command: Str
    :param city: Город, в котором выполнялся поиск.
    :type city: Str
    :param min_price: Минимальная цена.
    :type min_price: Itr
    :param max_price: Максимальная цена.
    :type max_price: Int
    :param check_in_date: Дата заезда.
    :type check_in_date: Str
    :param check_out_date: Дата выезда.
    :type check_out_date: Str
    :param distance_from: Расстояние от центра.
    :type distance_from: Str
    :param distance_to: Расстояние до центра.
    :type distance_to: Str
    :param hotel_variants: Количество вариантов отелей.
    :type hotel_variants: Int
    :param need_photo: Необходимость фотографии (да/нет).
    :type need_photo: Str
    :param count_photo: Количество фотографий.
    :type count_photo: Str
    :param hotel_names: Список названий отелей.
    :type hotel_names: Str
    """

    user_id = CharField()
    date_time = CharField()
    user_name = CharField(null=True)
    command = CharField()
    city = CharField()
    min_price = IntegerField()
    max_price = IntegerField()
    check_in_date = CharField()
    check_out_date = CharField()
    distance_from = CharField()
    distance_to = CharField()
    hotel_variants = IntegerField()
    need_photo = CharField()
    count_photo = CharField()
    hotel_names = TextField()


if __name__ == "__main__":

    """
    Создает таблицу History в базе данных при запуске файла.
    """

    db.create_tables([History])
