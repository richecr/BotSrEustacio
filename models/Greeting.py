from models.Model import Model


class Greeting(Model):
    id: int = None
    greeting: str = None
    id_user: int = None
