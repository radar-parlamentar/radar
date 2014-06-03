from django_cron import Schedule, CronJobBase
from importadores import importador

class ImportadorAnaliseCron(CronJobBase):

        #Colocar horario para executar o importador
        RUN_AT_TIMES= ['00:00'] 
        schedule = Schedule(run_at_times = RUN_AT_TIMES) 
        code = "Importa cdep"            
        def do(self):
                # Importador cdep
                importador.main(camara = True)     