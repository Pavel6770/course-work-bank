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

