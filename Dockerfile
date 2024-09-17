FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

RUN pip install poetry==1.8.3

COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

RUN poetry install

COPY ./lib /app/lib
COPY ./apps /app/apps

RUN pip cache purge && poetry cache clear --all .

CMD ["poetry", "run", "fastapi", "run", "apps/cart_api/main.py", "--port", "8080"]
