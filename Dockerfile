FROM python:3.8

LABEL maintainer="Hossam Hammady <github@hammady.net>"

ENV CRON_USER prayertimes

RUN apt update && \
    apt install -y cron && \
    adduser --system ${CRON_USER} && \
    mv /etc/localtime /etc/localtime.old && \
    ln -s /usr/share/zoneinfo/Canada/Eastern /etc/localtime

WORKDIR /home/${CRON_USER}

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV CSV_FILE prayers-timetable.csv

COPY . .

ENTRYPOINT ["./docker-entrypoint.sh", "/home/prayertimes/app.py"]
