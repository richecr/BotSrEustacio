from duck_orm.model import Model
from duck_orm.sql import fields as Field

from database.db import database


class User(Model):
    __tablename__ = "users"
    __db__ = database.db

    id: str = Field.String(primary_key=True)
    name: str = Field.String(not_null=True)
