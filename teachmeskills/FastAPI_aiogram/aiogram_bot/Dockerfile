FROM python:3.12-alpine

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/
EXPOSE 8001
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:8001", "-k", "uvicorn.workers.UvicornWorker", "asgi:application"]
#gunicorn --workers 1 --bind 0.0.0.0:8001 -k uvicorn.workers.UvicornWorker asgi:application

