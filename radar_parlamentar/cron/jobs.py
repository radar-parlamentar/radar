from django_cron import CronJobBase, Schedule
import logging

logger = logging.getLogger("radar")

# Isso é chamada a cada 2 min contanto que
# python manage.py runcrons seja constantemente executado
class CashRefresherJob(CronJobBase):

    RUN_EVERY_MINS = 2

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'job.CashRefresherJob'    # a unique code

    def do(self):
        logger.info('CashRefresherJob got executed')
