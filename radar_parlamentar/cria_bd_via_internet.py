# para criar o banco de dados vazio:
# ./manage.py syncdb
#
# para importar os dados da internet:
# ./manage.py shell
# e do shell rodar este script.

# Para cdep, isso irá supor que já existe o arquivo
# importadores/dados/cdep/votadas.txt e ele será usado.
# Caso queira atualizar a lista de votadas, deve-se primeiramente fazer:
# $ from importadores import camara
# $ finder = camara.ProposicoesFinder()
# $ finder.find_props_que_existem() # vai gerar dados/cdep/ids_que_existem.txt
# $ props = finder.find_props_com_votacoes() # vai gerar dados/cdep/votadas.txt

import time

comeco = time.time()

from importadores import cmsp
cmsp.main()

etcmsp = time.time() - comeco
comeco = time.time()

from importadores import camara
camara.main()

etcdep = time.time() - comeco
comeco = time.time()

from importadores import senado
senado.main()

etsen = time.time() - comeco

print 'CMSP demorou (h:mm:ss): %d:%d:%d' % (etcmsp/3600,(etcmsp/60)%60,etcmsp%60)
print 'CDEP demorou (h:mm:ss): %d:%d:%d' % (etcdep/3600,(etcdep/60)%60,etcdep%60)
print 'SEN demorou (h:mm:ss): %d:%d:%d' % (etsen/3600,(etsen/60)%60,etsen%60)
