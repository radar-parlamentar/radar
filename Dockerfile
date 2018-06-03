# VERSION 1.0.0-2
# AUTHOR: Diego Rabatone Oliveira (@diraol)
# DESCRIPTION: Radar Parlamentar main container
# BUILD: docker build -t radarparlamentar/radar:<VERSION> -t radarparlamentar/radar:latest  .
# To push the image to dockerhub run:
#   docker push radarparlamentar/radar:<VERSION>
#   docker push radarparlamentar/radar:latest
# SOURCE: https://github.com/radar_parlamentar/radar
FROM radarparlamentar/base:1.0.3

COPY radar_parlamentar/requirements.txt /tmp/requirements.txt
RUN set -ex \
    && pip install -U pip setuptools wheel \
    && pip install -r /tmp/requirements.txt \
    && rm -rf ~/.cache/pip/*

COPY deploy/entrypoint.sh /usr/bin/entrypoint.sh
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
