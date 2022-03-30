FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bot
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . /bot