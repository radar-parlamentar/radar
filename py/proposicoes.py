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

"""Módulo proposicoes -- funções para processamento de proposições
Possui script que lista proposições com votações

Funcões:
parse_html -- parse do arquivo recusrsos/proposicoes.html
com_votacao -- verifica pelo web service lista de proposições que possuem votações
proposicoes_com_votacao -- retorna lista de proposições que possuem votações baseado no arquivo votadas.txt
"""

import re
import codecs
import camaraws

# PL - projeto de lei
# PLP - projeto de lei complementar
# PDC - projeto de decreto legislativo
# MPV - projeto de medida provisória
# PEC - proposta de emenda à constituição

def parse_html():
    """Parse do arquivo recusrsos/proposicoes.htmll
    Retorna:
    Uma lista com a identificação das proposições encontradas no htmll
    Cada posição da lista é um dicionário com chaves \in {id, tipo, num, ano}
    As chaves e valores desses dicionários são strings
    """
    file_name = 'recursos/proposicoes2011.html'  # arquivo contem proposições votadas pela câmara em 2011
    prop_file = codecs.open(file_name, encoding='ISO-8859-15', mode='r')
    regexp = '<A HREF=http://.*?id=([0-9]*?)>([A-Z]*?) ([0-9]*?)/([0-9]{4})</A>'
    proposicoes = []
    for line in prop_file:
        res = re.search(regexp, line)
        if res:
            proposicoes.append({'id':res.group(1), 'tipo':res.group(2), 'num':res.group(3), 'ano':res.group(4)})
    return proposicoes

def parse():
    """Parse do arquivo recursos/votadas.txt
    Retorna:
    Uma lista com a identificação das proposições encontradas no txt
    Cada posição da lista é um dicionário com chaves \in {id, tipo, num, ano}
    As chaves e valores desses dicionários são strings
    """
    file_name = 'resultados/votadas.txt'  # arquivo contem proposições votadas pela câmara em 2011 para as quais obtivemos o xml da votação
    prop_file = open(file_name, 'r')
    # ex: "485262: MPV 501/2010"
    regexp = '^([0-9]*?): ([A-Z]*?) ([0-9]*?)/([0-9]{4})'
    proposicoes = []
    for line in prop_file:
        res = re.search(regexp, line)
        if res:
            proposicoes.append({'id':res.group(1), 'tipo':res.group(2), 'num':res.group(3), 'ano':res.group(4)})
    return proposicoes

def com_votacao(proposicoes): 
    """Verifica quais proposições possuem votações no web service da câmara
    É somente sobre essas proposições que faremos nossas análises
    Essa verificação é feita invocando o web service da câmara 
    Argumentos:
    proposicoes -- lista de proposições; cada proposição é um dicionário com chaves \in {id, tipo, num, ano}; chaves e valores são strings

    Retorna:
    Lista com proposições que apresentam lista de votações
    Cada proposição é um dicionário com chaves \in {id, tipo, num, ano}; chaves e valores são strings     
    """
    votadas = []
    for prop in proposicoes:
        print "requisitando " + prop['id']
        vot = camaraws.obter_votacao(prop['tipo'], prop['num'], prop['ano']) 
        if vot != None:
            votadas.append(prop)
    return votadas

def proposicoes_com_votacao():
    """Retorna a lista de proposições para as quais é possível obter o xml da votação
    Esta lista é retirada do arquivo resultados/votadas.txt
    Retorna:
    Uma lista de proposições
    Cada posição da lista é um dicionário com chaves \in {id, tipo, num, ano}
    As chaves e valores desses dicionários são strings    
    """
    return parse()


if __name__ == "__main__":
    proposicoes = parse_html()
    votadas = com_votacao(proposicoes)
    print("# Documento entregue pela câmara continha %d proposições votadas em 2011" % len(proposicoes))
    print("# %d proposições retornaram informações sobre suas votações pelo web service" % len(votadas))
    print("# Proposições que retornaram a votação:")
    for prop in votadas:
        print("%s: %s %s/%s" % (prop['id'],prop['tipo'],prop['num'],prop['ano']))



