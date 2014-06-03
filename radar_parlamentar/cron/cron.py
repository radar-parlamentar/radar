from django_cron import Schedule, CronJobBase
from importadores import importador
from modelagem.models import TesteCron

class ImportadorAnaliseCron(CronJobBase):

        #Colocar horario para executar o importador
        RUN_AT_TIMES= ['01:00'] 
        schedule = Schedule(run_at_times = RUN_AT_TIMES) 
        code = "Importa cdep"      

        def do(self):
			#armazena flag no banco de dados para testes
			teste_cron = TesteCron()
			teste_cron.save()
			
			#Importador cdep
			importador.main(camara = True)