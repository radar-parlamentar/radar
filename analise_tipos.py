#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#
# faz uma análise dos tipos de proposições votadas em 2011

import parser

proposicoes = parser.parse_proposicoes()
pl = plp = pdc = mpv = pec = 0 
for prop in proposicoes:
  if (prop['tipo'] == 'PL'):
    pl += 1
  elif (prop['tipo'] == 'PLP'):
    plp += 1
  elif (prop['tipo'] == 'PDC'):
    pdc += 1
  elif (prop['tipo'] == 'MPV'):
    mpv += 1
  elif (prop['tipo'] == 'PEC'):
    pec += 1

total = len(proposicoes)
print('Votações na câmara em 2011')
print('%d proposições' % total)
print('%d PLs (%d%s)' % (pl, pl/total*100, '%'))
print('%d PLPs (%d%s)' % (plp, plp/total*100, '%'))
print('%d PDCs (%d%s)' % (pdc, pdc/total*100, '%'))
print('%d MPVs (%d%s)' % (mpv, mpv/total*100, '%'))
print('%d PECs (%d%s)' % (pec, pec/total*100, '%'))
#print('Checksum: %d' % (pl+plp+pdc+mpv+pec))
