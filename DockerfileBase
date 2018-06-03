# VERSION 1.0.3
# AUTHOR: Diego Rabatone Oliveira (@diraol)
# DESCRIPTION: Radar Parlamentar main container
# BUILD: - docker build -t radarparlamentar/base:<VERSION>  -t radarparlamentar/base:latest -f DockerfileBase .
#    To push the base image to dockerhub run:
#    docker push radarparlamentar/base:<VERSION>
#    docker push radarparlamentar/base:latest
# SOURCE: https://github.com/radar_parlamentar/radar
FROM python:3.7-rc-alpine

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# https://docs.python.org/3.6/using/cmdline.html#envvar-PYTHONUNBUFFERED
# https://github.com/sclorg/s2i-python-container/issues/157
# Aparentemente esta opção envolve expor mensagens de prompt/console/logs do
# python para o container.
ENV PYTHONUNBUFFERED 1

# Radar
ENV RADAR_HOME=/radar/radar_parlamentar
ENV DJANGO_CACHE_DIR=/tmp/django_cache
ENV RADAR_LOG_DIR=/var/log/radar

RUN mkdir -p ${RADAR_HOME} ${DJANGO_CACHE_DIR} ${RADAR_LOG_DIR} /var/log/uwsgi
WORKDIR ${RADAR_HOME}

# git é uma dependência do projeto, utilizamos no código para pegar a versão
# corrente do projeto pelo commit.
# postgresql-dev é necessário para instalar a lib que vai fazer a conexão com
# o postgres.
# musl-dev é usada apenas apra compilação da lib python psycopg2.
RUN set -ex \
    && apk add --update \
        curl \
        postgresql-dev \
        postgresql \
        git \
    && apk --no-cache add --virtual _build_deps \
        build-base \
        python3-dev \
        gcc \
        libc-dev \
        linux-headers \
        musl-dev \
    && pip install -U pip setuptools wheel \
    && pip install uwsgi numpy psycopg2-binary\
    && apk del _build_deps \
    && rm -rf \
        ~/.cache/pip/* \
        /var/cache/apk/*
