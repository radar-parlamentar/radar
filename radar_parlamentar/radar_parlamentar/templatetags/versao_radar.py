# -*- coding: utf8 -*-

import subprocess
import settings
import logging
from django import template
register = template.Library()


logger = logging.getLogger("radar")


@register.simple_tag
def versao_radar():
    time_zone = settings.defaults.TIME_ZONE
    versao_radar = ''

    try:
        cmd_data_ultimo_commit = 'TZ={0} date -d @$(git log \-n1 --format='
        cmd_data_ultimo_commit += '"%at") "+%d/%m/%Y"'.format(time_zone)
        data_ultimo_commit = subprocess.check_output(cmd_data_ultimo_commit,
                                                     shell=True)

        cmd_hash_ultimo_commit = 'git log --pretty=format:"%H" -n 1'
        hash_ultimo_commit = subprocess.check_output(cmd_hash_ultimo_commit,
                                                     shell=True)
        hash_abrev_ultimo_commit = hash_ultimo_commit[:7]

        versao_radar = 'Versão: <a href="https://github.com/radar-parlamentar/'
        versao_radar += 'radar/commit/{0}" target="_blank">{1}</a> de {2}' \
                        .format(hash_ultimo_commit, hash_abrev_ultimo_commit,
                                data_ultimo_commit)

    except (IndexError, subprocess.CalledProcessError) as e:
        logger.error('Erro ao pegar o hash ou' +
                     'a data do ultimo commit (versao sera omitida)')

    return versao_radar
