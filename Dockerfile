FROM ubuntu:latest

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get upgrade -y

RUN apt-get install python3.7 python3-pip chromium-driver -y

RUN pip install -r requirments.txt