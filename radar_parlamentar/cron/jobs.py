from django_cron import CronJobBase, Schedule
import logging
from importadores.celery_tasks import importar_assincronamente
from datetime import date

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
    code = 'job.CashRefresherJob'    # a unique code

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

# TODO class CashRefresherJob - Executado diariamente às 1h
# TODO class DbDumperJob - Executado segunda às 4h
