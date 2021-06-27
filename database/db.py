from databases import Database
from models.User import User
from models.Greeting import Greeting


class DB:
    def __init__(self) -> None:
        self.db = Database('sqlite:///bot_sr_eustacio.db')

    async def connect(self):
        await self.db.connect()

    async def create_table_user(self):
        sql = "CREATE TABLE IF NOT EXISTS users (" + \
            "id INTEGER NOT NULL PRIMARY KEY," + \
            "name TEXT NOT NULL);"
        await self.db.execute(sql)

    async def create_table_greeting(self):
        sql = "CREATE TABLE IF NOT EXISTS greetings (" + \
            "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, " + \
            "greeting TEXT NOT NULL, " + \
            "id_user INTEGER NOT NULL, " + \
            "FOREIGN KEY (id_user) " + \
            "REFERENCES users (id) " + \
            "ON DELETE CASCADE " + \
            "ON UPDATE NO ACTION" + \
            ");"
        await self.db.execute(sql)

    async def add_user(self, id: int, name: str):
        sql = "INSERT INTO users(id, name) VALUES(:id, :name);"
        values = {
            "id": id,
            "name": name
        }
        await self.db.execute(sql, values)

    async def add_greeting(self, greeting: str, id_user: int):
        sql = "INSERT INTO greetings(greeting, id_user) " + \
              "VALUES(:greeting, :id_user);"
        values = {
            "greeting": greeting,
            "id_user": id_user
        }
        await self.db.execute(sql, values)

    async def get_users(self, where: dict[str, any] = {}):
        sql = "SELECT * FROM users"
        if where:
            sql += " WHERE "
            sqls_where = []
            for key in where.keys():
                sql_where = "{key} = :{key}".format(key=key)
                sqls_where.append(sql_where)
            sql += " AND ".join(sqls_where)

        results = await self.db.fetch_all(sql, where)
        users: list[User] = []
        for result in results:
            user_dict = dict(result.items())
            users.append(User(**user_dict))

        return users

    async def get_greetings(self, where: dict[str, any] = {}):
        sql = "SELECT * FROM greetings"
        if where:
            sql += " WHERE "
            sqls_where = []
            for key in where.keys():
                sql_where = "{key} = :{key}".format(key=key)
                sqls_where.append(sql_where)
            sql += " AND ".join(sqls_where)

        results = await self.db.fetch_all(sql, where)
        greetings: list[Greeting] = []
        for result in results:
            greeting_dict = dict(result.items())
            greetings.append(Greeting(**greeting_dict))

        return greetings
