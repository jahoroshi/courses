# 🐳 Django Docker Учебный проект

Этот репозиторий содержит учебный проект на базе Django, с использованием Docker для оркестрации и Postgres в качестве базы данных.

## 🛠️ Используемые технологии и библиотеки

Проект построен на следующих технологиях:

- **Django 3.x** — основной фреймворк для разработки веб-приложений на Python.
- **PostgreSQL** — система управления базами данных, использующая SQL.
- **Docker** — инструмент для контейнеризации приложений.
- **Docker Compose** — инструмент для упрощения запуска многокомпонентных приложений в контейнерах Docker.
- **psycopg2** — библиотека для взаимодействия с PostgreSQL из Django.

## 🎯 Цель проекта

Цель данного проекта — получить практический опыт работы с:

1. **Docker** для контейнеризации приложений.
2. **Docker Compose** для оркестрации многокомпонентных систем (Django-приложение и база данных).
3. Работа с **Django** и использование его возможностей для создания веб-приложений.
4. Подключение и управление базой данных **PostgreSQL** с использованием **psycopg2** и визуализация через **Adminer**.

## 📂 Структура проекта

- **`cards/`** — каталог, содержащий Django-приложение с моделями и бизнес-логикой.
- **`djangoProject/`** — основной каталог с настройками проекта Django.
- **`templates/`** — каталог с HTML-шаблонами.
- **`.venv/`** — виртуальная среда Python.
- **`Dockerfile`** — файл для создания Docker-образа приложения.
- **`docker-compose.yml`** — файл для оркестрации контейнеров Docker.
- **`manage.py`** — скрипт для управления Django-проектом.
- **`requirements.txt`** — файл с перечислением зависимостей Python.

## 📦 Контейнеры

- **Django-сервис** — веб-приложение, доступное по порту 8001.
- **PostgreSQL** — база данных, которая хранит данные приложения.
- **Adminer** — инструмент для управления базой данных, доступный по порту 8080.

---

Учебный проект предназначен для отработки навыков работы с Docker и Docker Compose в контексте разработки на Django.