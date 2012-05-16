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

"""módulo cmsp (Câmara Municipal de São Paulo)

Funções:
from_xml -- importa as votações descritas no XML fornecido pela câmara
Argumentos:
xml_file - string que indica a localização do arquivo XML descrevendo as votações
Retorno:
uma lista de objetos do tipo Proposicao
"""

import model
import re
import xml.etree.ElementTree as etree

XML2010 = 'recursos/cmsp2010.xml'
XML2011 = 'recursos/cmsp2011.xml'
XML2012 = 'recursos/cmsp2012.xml'

def _prop_nome(texto):
    """Procura "tipo num/ano" no texto"""
    regex = '[a-zA-Z]{1,3} [0-9]{1,4}/[0-9]{4}'
    res = re.search(regex, texto)
    if res:
        return res.group(0)
    else:
        return None

def _tipo(prop_nome):
    """Extrai tipo de "tipo num/ano" """
    regex = '([a-zA-Z]{1,3}) [0-9]{1,4}/[0-9]{4}'
    res = re.search(regex, prop_nome)
    if res:
        return res.group(1)
    else:
        return None

def _num(prop_nome):
    """Extrai num de "tipo num/ano" """
    regex = '[a-zA-Z]{1,3} ([0-9]{1,4})/[0-9]{4}'
    res = re.search(regex, prop_nome)
    if res:
        return res.group(1)
    else:
        return None

def _ano(prop_nome):
    """Extrai ano de "tipo num/ano" """
    regex = '[a-zA-Z]{1,3} [0-9]{1,4}/([0-9]{4})'
    res = re.search(regex, prop_nome)
    if res:
        return res.group(1)
    else:
        return None

# TODO: desconsiderar votações simbólicas com declaração de voto
# TODO: como diferenciar votações de proposições de outras votações?
#        no momento estou verificando a existência da substring 'tipo num/ano' no resumo* da votação,
#        mas parece não ser suficiente
#        Além disso existem matérias como "Inversão da pauta do item 3 PL 96/2011 com o item 1 PL 358/2010" que quebram esse esquema
#       * resumo (do objeto votação) = matéria + ementa (do xml votação da cmsp)
def from_xml(xml_file=XML2011):

    f = open(xml_file, 'r')
    xml = f.read()
    f.close()
    tree = etree.fromstring(xml)

    proposicoes = {} # chave é string (ex: 'pl 127/2004'); valor é objeto do tipo Proposicao
    for vot_tree in tree.getchildren():
        if vot_tree.tag == 'Votacao' and vot_tree.getchildren(): # se é votação e contém votos
                resumo = '%s -- %s' % (vot_tree.get('Materia'), vot_tree.get('Ementa'))
                prop_nome = _prop_nome(resumo)
                if (prop_nome): # no XML da cmsp tem várias votações que não são de proposições; 
                                #exemplos: Adiamento do Prolong. do Expediente; Adiamento dos Demais itens da Pauta. 
                    if proposicoes.has_key(prop_nome):
                        prop = proposicoes[prop_nome]
                    else:
                        prop = model.Proposicao()
                        prop.sigla = _tipo(prop_nome)
                        prop.numero = _num(prop_nome)
                        prop.ano = _ano(prop_nome)
                        proposicoes[prop_nome] = prop
                    vot = model.Votacao()
                    vot.resumo = resumo
                    vot.data = vot_tree.get('DataDaSessao')
                    prop.votacoes.append(vot)

    return proposicoes.values()

if __name__ == "__main__":

    props = from_xml()
    for p in props:
        print "%s (%d)" % (p.nome(), len(p.votacoes))


