FROM python:3.10.7-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /bill_manager

COPY ./requirements.txt .

RUN apt-get update -y && apt-get install -y python3-pip python3-dev libpq-dev && pip3 install -r requirements.txt

EXPOSE 8000
