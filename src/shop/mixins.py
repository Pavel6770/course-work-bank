class LogMixin:
    def __init__(self, *args, **kwargs):
        print(f"Создан {self.__class__.__name__} с параметрами: {args}, {kwargs}")