FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


RUN python manage.py migrate

USER django-user
