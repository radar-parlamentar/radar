#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# Pequeno script que baixa a votação do código florestal
# Fonte: http://rest.elkstein.org/2008/02/using-rest-in-python.html
import urllib.request
from model import Proposicao


tipo = 'pl'
num = '1876'
ano = '1999'
url = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=%s&numero=%s&ano=%s' % (tipo, num, ano)
xml = urllib.request.urlopen(url).read()
xml = str(xml, "utf-8")

prop = Proposicao()
prop.fromxml(xml)
print(prop)


