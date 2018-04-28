from django_cron import CronJobBase, Schedule
import logging
from importadores.celery_tasks import importar_assincronamente
from datetime import date
from django.core.cache import cache
import requests
import os
from modelagem import models

logger = logging.getLogger("radar")

"""
Django Cron documentation:
http://django-cron.readthedocs.io/en/latest/installation.html
"""

# Isso é chamada a cada 2 min contanto que
# python manage.py runcrons seja constantemente executado
class DemoJob(CronJobBase):
    """Para testes"""

    RUN_EVERY_MINS = 2
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'job.DemoJob'    # a unique code

    def do(self):
        logger.info('DemoJob foi chamado.')

class ImportadorJob(CronJobBase):
    """Executado terça às 2h"""

    RUN_AT_TIMES = ['02:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'job.ImportadorJob'

    def do(self):
        logger.info('ImportadorJob foi chamado.')
        weekday = date.today().weekday()
        # segunda é o zero
        if weekday == 1:
            logger.info('ImportadorJob invocando importações.')
            importar_assincronamente.delay('cmsp')
            importar_assincronamente.delay('cdep')
        else:
            logger.info('Hoje não é o dia. ImportadorJob só trabalha às terças.')

class CashRefresherJob(CronJobBase):
    """Executado diariamente às 1h"""

    RUN_AT_TIMES = ['01:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'job.CashRefresherJob'

    def do(self):
        logger.info('CashRefresherJob foi chamado.')
        cache.clear()
        casas = [ casa.nome_curto for casa in models.CasaLegislativa.objects.all() ]
        periodicidades = [ periodo[0] for periodo in  models.PERIODOS ]
        if 'MES' in periodicidades:
            periodicidades.remove('MES')
        for casa in casas:
            for periodicidade in periodicidades:
                url = 'http://nginx/radar/json/%s/%s/' % (casa, periodicidade)
                # localhost não é alcançável, pois o django é acessado via socket
                logger.info('CashRefresherJob invocando', url)
                requests.get(url)
                # Retorno:
                # <h1>Bad Request (400)</h1>
                # Obs: Do host, 'GET http://localhost/radar/json/cmsp/ANO/'
                # funciona.


class DbDumperJob(CronJobBase):
    """Executado segunda às 4h"""

    RUN_AT_TIMES = ['04:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'job.DbDumperJob'

    def do(self):
        logger.info('DbDumperJob foi chamado.')
        weekday = date.today().weekday()
        # segunda é o zero
        if weekday == 0:
            logger.info('DbDumperJob fazendo dump do banco.')
        else:
            logger.info('Hoje não é o dia. DbDumperJob só trabalha às segundas.')

class DbDumperJob(CronJobBase):
    """Executado segunda às 4h"""

    RUN_AT_TIMES = ['04:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'job.DbDumperJob'

    def do(self):
        logger.info('DbDumperJob foi chamado.')
        weekday = date.today().weekday()
        # segunda é o zero
        if weekday == 0:
            logger.info('DbDumperJob fazendo dump do banco.')
        else:
            logger.info('Hoje não é o dia. DbDumperJob só trabalha às segundas.')

class DbDumper():

    # Roteiro:
    # OK Verificar que link em dados não tem dump
    # criar .pgpass
    # Execução de pg_dump retornou: pg_dump: aborting because of server version mismatch
    # Executar DbDumper sem collectstatic
    # Verificar que link em dados não tem dump
    # Executar DbDumper com collectstatic
    # Verificar que link em dados tem dump
    # Teste de DbDumper: 1o apaga arquivo se existir, executa, verifica se arquivo foi criado
    # publicar radar/base no docker hub

    DUMP_FILE = "/radar/radar_parlamentar/radar_parlamentar/static/db-dump/radar.sql"

    def dump(self):
        dump_command = 'pg_dump -h postgres -U radar -d radar -W --inserts -t modelagem_* -f %s' % DbDumper.DUMP_FILE
        os.system(dump_command)
        #compress_command = 'bzip2 -9 -f %s' % DbDumper.DUMP_FILE
        #os.system(compress_command)
        #collectstatic_command = 'python manage.py collectstatic --noinput' # necessário?
        #os.system(collectstatic_command)
