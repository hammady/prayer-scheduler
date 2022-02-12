FROM python:3.8 AS butt-builder
ARG BUTT_VERSION=0.1.33
ENV BUTT_VERSION=$BUTT_VERSION
# Install requirements until butt source is fixed to remove the dependency
RUN apt update -q && \
    apt install -y \
    libmp3lame-dev libfltk1.3-dev portaudio19-dev libvorbis-dev libopus-dev libflac-dev
# Download, build and install butt-client
RUN wget -O butt-$BUTT_VERSION.tar.gz https://sourceforge.net/projects/butt/files/butt/butt-$BUTT_VERSION/butt-$BUTT_VERSION.tar.gz/download && \
    tar -xzf butt-$BUTT_VERSION.tar.gz && \
    cd butt-$BUTT_VERSION && \
    ./configure --without-butt && \
    make && \
    make install

FROM python:3.8

COPY --from=butt-builder /usr/local/bin/butt-client /usr/local/bin/butt-client

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

ENTRYPOINT ["./docker-entrypoint.sh", "/home/prayertimes/app.py"]
