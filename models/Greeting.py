from duck_orm.model import Model
from duck_orm.sql import fields as Field
from duck_orm.sql.relationship import ForeignKey

from database.db import database
from models.User import User


class Greeting(Model):
    __tablename__ = 'greetings'
    __db__ = database.db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    greeting: str = Field.String(not_null=True)
    id_user: int = ForeignKey(model=User, name_in_table_fk='id')
