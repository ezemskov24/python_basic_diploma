from database.utils.CRUD import CRUDInterFace
from database.common.models import db, History


db.connect()
db.create_tables([History])

crud = CRUDInterFace


if __name__ == "__main__":
    crud()
