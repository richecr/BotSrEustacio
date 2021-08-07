from databases import Database


class DB:
    def __init__(self) -> None:
        self.db = Database('sqlite:///bot_sr_eustacio.db')

    async def connect(self):
        await self.db.connect()


database = DB()
