# Parse do arquivo proposicoes.html
# Recupera uma lista com apenas a identificação das proposições (tipo número/ano, e id também)

# OBS
# PL - projeto de lei
# PLP - projeto de lei complementar
# PDC - projeto de decreto legislativo
# MPV - projeto de medida provisória
# PEC - proposta de emenda à constituição

import re
import codecs

def parse_proposicoes():
  file_name = 'recursos/proposicoes2011.htm'  # arquivo contem proposições votadas pela câmara em 2011
  prop_file = codecs.open(file_name, encoding='ISO-8859-15', mode='r')
  regexp = '<A HREF=http://.*?id=([0-9]*?)>([A-Z]*?) ([0-9]*?)/([0-9]{4}?)</A>'
  proposicoes = []
  for line in prop_file:
    res = re.search(regexp, line)
    if res:
      proposicoes.append({'id':res.group(1), 'tipo':res.group(2), 'num':res.group(3), 'ano':res.group(4)})
  return proposicoes


