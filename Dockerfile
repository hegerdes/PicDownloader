FROM ubuntu:latest

WORKDIR /usr/src/app

COPY . .

RUN sudo apt update && sudo apt upgrade -y

RUN sudo apt install python3.7 python3-pip chromium-driver

RUN sudo pip install -r requirments.txt