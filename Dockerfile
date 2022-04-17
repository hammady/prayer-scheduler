FROM ghcr.io/hammady/butt:latest AS butt-image
# TODO use a specific tag for the butt-image when butt 0.1.34 is released
FROM python:3.8
COPY --from=butt-image /usr/local/bin/butt-client /usr/local/bin/butt-client

LABEL maintainer="Hossam Hammady <github@hammady.net>"

ENV CRON_USER prayertimes

RUN apt update && \
    apt install -y cron && \
    adduser --system ${CRON_USER} && \
    mv /etc/localtime /etc/localtime.old && \
    ln -s /usr/share/zoneinfo/Canada/Eastern /etc/localtime

# TODO remove this layer when butt 0.1.34 is released
RUN apt-get install -y \
    libfltk1.3-dev \
    portaudio19-dev \
    libopus-dev \
    libmp3lame-dev \
    libvorbis-dev \
    libogg-dev \
    libflac-dev \
    libdbus-1-dev \
    libsamplerate0-dev \
    libssl-dev

WORKDIR /home/${CRON_USER}

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

HEALTHCHECK --interval=20s --timeout=3s --start-period=60s --retries=6 CMD [ "/home/prayertimes/healthz.sh" ]

ENTRYPOINT ["./docker-entrypoint.sh", "/home/prayertimes/app.py"]
