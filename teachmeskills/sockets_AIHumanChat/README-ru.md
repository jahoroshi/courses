# 🧠 GPT-Чат Клиент-Серверная Архитектура

## 🚀 Используемые технологии и паттерны:
- **Языки программирования**: Python 🐍
- **Библиотеки**:
  - `socket`, `threading`, `sys` — для создания клиент-серверного взаимодействия 🔗.
  - `requests`, `urllib3`, `requests_html`, `selenium` — для работы с HTTP запросами, парсинга веб-страниц и прокси 🌐.
  - `openai` — для интеграции с OpenAI API 🤖.
  - `csv`, `json`, `os`, `re` — для работы с файлами и регулярными выражениями 📂.
  - `concurrent.futures.ThreadPoolExecutor` — для параллельного выполнения задач 🛠️.
- **Паттерны программирования**:
  - Абстрактные классы (`abc`).
  - Обработчики сообщений в клиент-серверной архитектуре.
  - Повторные попытки выполнения запросов с использованием `Retry` 🔄.

## 📋 Описание функционала:

### 1. **`client_human.py`** — клиентская программа для общения 🗣️
Клиент подключается к серверу, отправляет и получает сообщения через сокеты. Используется многопоточность для одновременного получения и отправки сообщений пользователем.

### 2. **`client_gpt_1.py` / `client_gpt_2.py`** — клиент с интеграцией GPT-3.5 🤖
Эти клиенты обрабатывают полученные сообщения с помощью OpenAI API и отправляют сгенерированный ответ обратно на сервер.

### 3. **`server.py`** — серверная часть программы 🖥️
Сервер принимает подключения от клиентов, управляет сессиями и пересылает сообщения между клиентами.

### 4. **`openai_chat.py`** — модуль для взаимодействия с OpenAI API 🌐
Реализует сессию с использованием прокси-серверов и повторными попытками подключения при ошибках. Использует библиотеку `requests`.

### 5. **`proxy_checker.py`** — программа для проверки прокси-серверов 🕵️‍♂️
Проверяет доступность прокси и измеряет их скорость ответа. Работает в многопоточном режиме для быстрого выполнения проверок.

### 6. **`parser_hw.py`** — парсер веб-страниц и API 📑
Парсит веб-страницы с помощью Selenium и Requests-HTML. Сохраняет результаты в формате CSV и JSON. Специализируется на сборе данных о прокси-серверах.

---

## 📂 Структура проекта:

- `client_human.py`: Клиент для общения между пользователями.
- `client_gpt_1.py` / `client_gpt_2.py`: Клиенты с интеграцией GPT-3.5.
- `server.py`: Сервер для обработки подключений клиентов.
- `openai_chat.py`: Модуль для работы с OpenAI API.
- `proxy_checker.py`: Инструмент для проверки прокси.
- `parser_hw.py`: Модуль для парсинга прокси с веб-страниц и через API.

