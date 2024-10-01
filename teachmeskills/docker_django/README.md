# 🐳 Django Docker Educational Project

This repository contains an educational project based on Django, using Docker for orchestration and Postgres as the database.

## 🛠️ Technologies and Libraries Used

The project is built using the following technologies:

- **Django 3.x** — the main framework for developing web applications in Python.
- **PostgreSQL** — a database management system using SQL.
- **Docker** — a tool for containerizing applications.
- **Docker Compose** — a tool for simplifying the launch of multi-container applications in Docker.
- **psycopg2** — a library for interacting with PostgreSQL from Django.

## 🎯 Project Goals

The goal of this project is to gain practical experience with:

1. **Docker** for containerizing applications.
2. **Docker Compose** for orchestrating multi-container systems (Django application and database).
3. Working with **Django** and utilizing its features to build web applications.
4. Connecting and managing the **PostgreSQL** database using **psycopg2**, and visualizing the data via **Adminer**.

## 📂 Project Structure

- **`cards/`** — a directory containing the Django app with models and business logic.
- **`djangoProject/`** — the main directory with Django project settings.
- **`templates/`** — a directory with HTML templates.
- **`.venv/`** — Python virtual environment.
- **`Dockerfile`** — file for building the Docker image for the application.
- **`docker-compose.yml`** — file for orchestrating Docker containers.
- **`manage.py`** — script for managing the Django project.
- **`requirements.txt`** — file listing the Python dependencies.

## 📦 Containers

- **Django Service** — the web application, accessible on port 8001.
- **PostgreSQL** — the database that stores the application's data.
- **Adminer** — a tool for managing the database, accessible on port 8080.

---

This educational project is designed to practice working with Docker and Docker Compose in the context of Django development.
