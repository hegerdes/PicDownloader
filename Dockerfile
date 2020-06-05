FROM python:3.8-buster

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get upgrade -y

RUN apt-get install chromium-driver -y

RUN pip install -r requirments.txt