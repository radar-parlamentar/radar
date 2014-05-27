from django_cron import Schedule, CronJobBase
from importadores import importador


class ImportadorAnaliseCron(CronJobBase):

        #Colocar horario para executar o importador
        RUN_AT_TIMES= ['01:00'] 
        schedule = Schedule(run_at_times = RUN_AT_TIMES) 
        code = "Importa cdep"            
        def do(self):
                # Importador cdep
                importador.main(False, False, False, True)
                #Importador cmsp (Mais curto)
                #importador.main(False, True, False, False)
                


