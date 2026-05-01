class LogMixin:
    def __init__(self, *args, **kwargs):
        print(f"Создан {self.__class__.__name__} с параметрами: {args}, {kwargs}")
        # Не вызываем super().__init__, если в MRO дальше только object
        # super().__init__(*args, **kwargs)