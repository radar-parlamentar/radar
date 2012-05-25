#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, Leonardo Leite
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Script analise_tipos -- faz uma análise dos tipos de proposições votadas em 2011"""

import proposicoes

proposicoes = proposicoes.parse_html()
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
