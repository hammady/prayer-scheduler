FROM ghcr.io/hammady/butt-client:0.1.34 AS butt-image
FROM python:3.8
COPY --from=butt-image /usr/local/bin/butt-client /usr/local/bin/butt-client

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

COPY . .

HEALTHCHECK --interval=20s --timeout=3s --start-period=60s --retries=6 CMD [ "/home/prayertimes/healthz.sh" ]

ENTRYPOINT ["./docker-entrypoint.sh", "/home/prayertimes/app.py"]
