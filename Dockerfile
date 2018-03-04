# VERSION 1.0.0-1
# AUTHOR: Diego Rabatone Oliveira (@diraol)
# DESCRIPTION: Radar Parlamentar main container
# BUILD: docker build --rm -t radar-parlamentar
# SOURCE: https://github.com/radar_parlamentar/radar
FROM radarparlamentar/base:1.0.0

COPY radar_parlamentar/requirements.txt /tmp/requirements.txt
# git é uma dependência do projeto, utilizamos no código para pegar a versão
# corrente do projeto pelo commit.
# postgresql-dev é necessário para instalar a lib que vai fazer a conexão com
# o postgres.
# musl-dev é usada apenas apra compilação da lib python psycopg2.
RUN set -ex \
    && pip install -U pip setuptools wheel \
    && pip install -r /tmp/requirements.txt \
    && rm -rf ~/.cache/pip/*

# Forward uwsgi logs to the docker log collector
# RUN ln -sf /dev/stdout /var/log/uwsgi/djangoapp.log \
#     && ln -sf /dev/stdout /var/log/uwsgi/emperor.log
COPY deploy/entrypoint.sh /usr/bin/entrypoint.sh
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
