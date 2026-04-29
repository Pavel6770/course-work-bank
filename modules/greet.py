from datetime import datetime


def get_greeting() -> str:
    current_hour = datetime.now().hour
    
    if 6 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def print_greeting() -> None:
    greeting = get_greeting()
    print(f"{greeting}, Bro!")
    print("Welcome to Transaction Analysis Program!")

