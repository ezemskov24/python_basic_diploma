from datetime import datetime

from peewee import *


db = SqliteDatabase('telegram_bot.db')


class BaseModel(Model):
    class Meta:
        database = db


class History(BaseModel):
    user_id = IntegerField(primary_key=True)
    command = CharField()
    city = CharField()
    min_price = IntegerField()
    max_price = IntegerField()
    check_in_date = TextField()
    check_out_date = TextField()
    distance_from = IntegerField()
    distance_to = IntegerField()
    hotel_variants = IntegerField()
    need_photo = TextField()
    count_photo = TextField()


if __name__ == "__main__":
    db.create_tables([History])
