from peewee import *


db = SqliteDatabase('telegram_bot.db')


class BaseModel(Model):
    class Meta:
        database = db


class History(BaseModel):
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
    db.create_tables([History])
