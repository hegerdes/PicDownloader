FROM python:3.8-buster

WORKDIR /usr/src/app

COPY . .

COPY crontab /etc/cron/crontab

RUN apt-get update && apt-get upgrade -y && apt-get install chromium-driver cron -y

RUN pip install -r requirments.txt

RUN crontab /etc/cron/crontab

CMD ["crond", "-f"]