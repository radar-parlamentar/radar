# -*- coding: utf8 -*-

import subprocess
import settings
from django import template
register = template.Library()
import logging

logger = logging.getLogger("radar")

@register.simple_tag
def versao_radar():
    time_zone = settings.defaults.TIME_ZONE
    versao_radar = ''

    try:
        cmd_data_ultimo_commit = 'TZ={0} date -d @$(git log -n1 --format="%at") "+%d/%m/%Y"'.format(time_zone)
        data_ultimo_commit = subprocess.check_output(cmd_data_ultimo_commit, shell=True)

        cmd_hash_ultimo_commit = 'git log --pretty=format:"%h" -n 1'
        hash_ultimo_commit = subprocess.check_output(cmd_hash_ultimo_commit, shell=True)

        versao_radar = 'Versão: <a href="https://github.com/radar-parlamentar/radar/commit/{0}">{0}</a> de {1}'.format(hash_ultimo_commit, data_ultimo_commit)
    except subprocess.CalledProcessError, e:
        logger.error('Erro ao pegar o hash ou a data do ultimo commit (versao sera omitida)')

    return versao_radar