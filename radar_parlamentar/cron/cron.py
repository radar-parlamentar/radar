from django_cron import Schedule, CronJobBase
from importadores import importador
from modelagem.models import TesteCron

class ImportadorAnaliseCron(CronJobBase):

#Colocar horario para executar o importador
    RUN_AT_TIMES= ['20:09'] 
    schedule = Schedule(run_at_times = RUN_AT_TIMES) 
    code = "cron.ImportadorAnaliseCron"      

    def do(self):
        #armazena flag no banco de dados para testes
        teste_cron = TesteCron()
        teste_cron.save()
        #importador.main deve receber uma lista com o nome curto da(s) casas a ser(em) importada(s)
        importador.main(['cdep'])
