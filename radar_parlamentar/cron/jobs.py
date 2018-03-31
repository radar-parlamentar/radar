from django_cron import CronJobBase, Schedule
import logging
from importadores.celery_tasks import importar_assincronamente

logger = logging.getLogger("radar")

"""
Django Cron documentation:
http://django-cron.readthedocs.io/en/latest/installation.html
"""

# Isso é chamada a cada 2 min contanto que
# python manage.py runcrons seja constantemente executado
# TODO: colocar "python manage.py runcrons" no cron do container.
class DemoJob(CronJobBase):

    RUN_EVERY_MINS = 2
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'job.CashRefresherJob'    # a unique code

    def do(self):
        logger.info('DemoJob got executed')

class ImportadorJob(CronJobBase):

    # TODO apenas nas terças
    RUN_AT_TIMES = ['02:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'job.ImportadorJob'

    def do(self):
        logger.info('ImportadorJob got executed')
        importar_assincronamente.delay('cmsp')
        importar_assincronamente.delay('cdep')

# TODO
# class CashRefresherJob
# class DbDumperJob
