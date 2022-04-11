FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bot
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

RUN apt update && apt install tzdata -y
ENV TZ="Europe/Moscow"

COPY . /bot