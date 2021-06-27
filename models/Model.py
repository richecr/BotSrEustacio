class Model:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __getitem__(self, key):
        return getattr(self, key)
