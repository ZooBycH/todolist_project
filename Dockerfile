FROM python:3.10-slim

WORKDIR todolist/

RUN pip install "poetry==1.2.2"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi --no-root

COPY . .

CMD python manage.py runserver 0.0.0.0:8000