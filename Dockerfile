FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 8000:8000

ADD . /app
