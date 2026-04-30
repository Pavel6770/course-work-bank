\# 💰 Анализ банковских транзакций



Веб-приложение для анализа банковских транзакций из Excel-файла.  

Проект выполнен в рамках курсовой работы.



\---



\## 📌 Функциональность



\### 📊 Основные возможности

\- Загрузка и обработка \*\*6705 транзакций\*\* из Excel

\- Фильтрация данных по периодам: \*\*неделя (W)\*\*, \*\*месяц (M)\*\*, \*\*год (Y)\*\*, \*\*всё время (ALL)\*\*

\- Расчёт \*\*кешбэка\*\* (1 рубль на каждые 100 рублей расходов)

\- \*\*Инвесткопилка\*\* — округление трат до 10/50/100 рублей

\- Поиск по описанию и категориям

\- Поиск телефонных номеров (регулярные выражения)

\- Поиск переводов физическим лицам



\### 📈 Отчёты (с сохранением в JSON)

\- Траты по выбранной категории за последние 3 месяца

\- Средние траты по дням недели

\- Средние траты в рабочий и выходной день



\### 🌐 API

\- Главная страница: `/api/main`

\- События (расходы/доходы): `/api/events`

\- Поиск: `/api/search`

\- Отчёты: `/api/reports/category`, `/api/reports/weekday`, `/api/reports/workday`



\---



\# ⚙️ Установка и запуск



\## 🚀 Быстрый старт



```bash

\# 1. Клонировать репозиторий

git clone https://github.com/Pavel6770/course-work-bank.git

cd course-work-bank



\# 2. Создать и активировать виртуальное окружение

python -m venv venv

source venv/bin/activate  # Linux/Mac

venv\\Scripts\\activate     # Windows



\# 3. Установить зависимости

pip install -r requirements.txt



\# 4. Запустить приложение

python main.py



\# 5. Открыть в браузере

http://127.0.0.1:5000/



\### 🗂️ Структура проекта



\# course-work-bank/

├── data/

│   └── operations.xlsx

├── modules/

│   ├── api\_client.py

│   ├── categories.py

│   ├── cashback.py

│   ├── greet.py

│   ├── reports.py

│   ├── search.py

│   ├── services.py

│   └── transactions.py

├── templates/

│   └── index.html

├── data\_loader.py

├── views.py

├── main.py

├── user\_settings.json

├── requirements.txt

└── README.md



\### 🧪 Тестирование

&#x20;# pytest tests/ -v



\### 📄 Пример JSON-ответа



\# {

&#x20; "greeting": "Добрый вечер",

&#x20; "cards": \[

&#x20;   {"last\_digits": "7197", "total\_spent": 24179.41, "cashback": 0},

&#x20;   {"last\_digits": "5091", "total\_spent": 15192.26, "cashback": 0},

&#x20;   {"last\_digits": "4556", "total\_spent": 3775.7, "cashback": 181.0}

&#x20; ],

&#x20; "top\_transactions": \[],

&#x20; "currency\_rates": \[

&#x20;   {"currency": "USD", "rate": 92.5},

&#x20;   {"currency": "EUR", "rate": 100.2}

&#x20; ],

&#x20; "stock\_prices": \[]

}


# 🛍️ Интернет-магазин: ООП-модель товаров

Проект демонстрирует объектно-ориентированное программирование на Python на примере системы управления товарами интернет-магазина.

## 📦 Основные возможности

- Базовый класс `Product` для всех товаров
- Классы-наследники:
  - `Smartphone` — смартфон (добавлены: производительность, модель, память, цвет)
  - `LawnGrass` — газонная трава (добавлены: страна-производитель, срок прорастания, цвет)
- Класс `Category` для группировки товаров
- Защита от сложения товаров разных типов (ошибка `TypeError`)
- Защита от добавления в категорию объектов, не являющихся товарами

## 🧪 Технологии

- Python 3.12
- pytest + coverage (покрытие 100%)
- ООП: наследование, полиморфизм, инкапсуляция

## 🚀 Запуск и тестирование

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Pavel6770/course-work-bank.git
cd course-work-bank

### 2. Установить зависимости
#pip install -r requirements.txt

### 3. Запустить тесты с проверкой покрытия
# pytest tests/test_shop.py --cov=shop --cov-report=term

### 🧱 Пример использования
# from shop.smartphone import Smartphone
from shop.lawn_grass import LawnGrass
from shop.category import Category

# Создание товаров
iphone = Smartphone("iPhone 15", 120000, 5, "A17 Pro", "15 Pro", 256, "Black")
grass = LawnGrass("Изумруд", 1500, 10, "Россия", 14, "Зелёный")

# Категория
cat = Category("Электроника")
cat.add_product(iphone)      # ✅ можно
# cat.add_product("не товар") # ❌ TypeError

# Сложение одинаковых товаров
print(iphone + iphone)       # ✅ 120000*5 + 120000*5

# Сложение разных — ошибка
# print(iphone + grass)      # ❌ TypeError



### Критерии выполнения
# Код соответствует PEP 8

Классы Smartphone и LawnGrass — наследники Product

Добавлены все требуемые атрибуты

__add__ ограничивает сложение через type()

add_product ограничивает типы через isinstance()

Написаны тесты на новую функциональность

Покрытие тестами — 100% (более 75%)


### Результат тестов
# ================= test session starts =================
collected 10 items
tests/test_shop.py ..........                    [100%]

Name                   Stmts   Miss  Cover
------------------------------------------
shop/base_product.py      11      0   100%
shop/category.py          12      0   100%
shop/lawn_grass.py         7      0   100%
shop/smartphone.py         8      0   100%
TOTAL                     38      0   100%

================= 10 passed in 0.10s ==================


