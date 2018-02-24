# VERSION 1.0.0-1
# AUTHOR: Diego Rabatone Oliveira (@diraol)
# DESCRIPTION: Radar Parlamentar main container
# BUILD: docker build --rm -t radar-parlamentar
# SOURCE: https://github.com/radar_parlamentar/radar

FROM python:3.6-stretch
MAINTAINER DiRaOL

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

RUN mkdir -p ${RADAR_HOME} ${DJANGO_CACHE_DIR} /var/log/uwsgi
WORKDIR ${RADAR_HOME}

RUN set -ex \
    && apt-get update -yqq \
    && apt-get upgrade -yqq --no-install-recommends \
    && apt-get install -yqq --no-install-recommends \
        curl \
        locales \
        rabbitmq-server \
    && pip install -U pip setuptools wheel \
    && pip install -U $(pip freeze) \
    && pip install uwsgi \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY radar_parlamentar/requirements.txt /tmp/requirements.txt

RUN set -ex && pip install -r /tmp/requirements.txt

# Forward uwsgi logs to the docker log collector
# RUN ln -sf /dev/stdout /var/log/uwsgi/djangoapp.log \
#     && ln -sf /dev/stdout /var/log/uwsgi/emperor.log
