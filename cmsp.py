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

from __future__ import unicode_literals
import model
import re
import xml.etree.ElementTree as etree

# arquivos com os dados fornecidos pela cmsp
XML2010 = 'recursos/cmsp2010.xml'
XML2011 = 'recursos/cmsp2011.xml'
XML2012 = 'recursos/cmsp2012.xml'

# tipos de proposições encontradas nos XMLs da cmsp (2010, 2011, 2012)
# esta lista ajuda a identificar as votações que são de proposições
# Exemplos de votações que não são de proposições: Adiamento do Prolong. do Expediente; Adiamento dos Demais itens da Pauta. 
TIPOS_PROPOSICOES = ['PL', 'PLO', 'PDL']

# regex que captura um nome de proposição (ex: PL 12/2010)
PROP_REGEX = '([a-zA-Z]{1,3}) ([0-9]{1,4}) ?/([0-9]{4})' 

def _prop_nome(texto):
    """Procura "tipo num/ano" no texto"""
    res = re.search(PROP_REGEX, texto)
    if res and res.group(1).upper() in TIPOS_PROPOSICOES:
            return res.group(0).upper()
    else:
        return None

def _tipo(prop_nome):
    """Extrai tipo de "tipo num/ano" """
    res = re.search(PROP_REGEX, prop_nome)
    if res:
        return res.group(1)
    else:
        return None

def _num(prop_nome):
    """Extrai num de "tipo num/ano" """
    res = re.search(PROP_REGEX, prop_nome)
    if res:
        return res.group(2)
    else:
        return None

def _ano(prop_nome):
    """Extrai ano de "tipo num/ano" """
    res = re.search(PROP_REGEX, prop_nome)
    if res:
        return res.group(3)
    else:
        return None

def _voto_cmsp_to_model(voto):
    """Interpreta voto como tá no XML e responde em adequação a modelagem em model.py
    Em especial, "Não votou" é mapeado para abstenção
    """
    if voto == 'Não':
        return model.NAO
    if voto == 'Sim':
        return model.SIM
    if voto == 'Não votou':
        return model.ABSTENCAO 

def _vereadores_from_tree(vot_tree):
    """Extrai lista de vereadores do XML da votação"""
    
    vereadores = []
    for ver_tree in vot_tree.getchildren():
        if ver_tree.tag == 'Vereador':
            vereador = model.Deputado() # TODO classe Deputado deve virar Parlamentar
            vereador.nome = ver_tree.get('NomeParlamentar')
            vereador.partido = ver_tree.get('Partido')
            voto = ver_tree.get('Voto')
            vereador.voto =  _voto_cmsp_to_model(voto)
            vereadores.append(vereador)
    return vereadores
          

def from_xml(xml_file=XML2011):

    f = open(xml_file, 'r')
    xml = f.read()
    f.close()
    tree = etree.fromstring(xml)

    proposicoes = {} # chave é string (ex: 'pl 127/2004'); valor é objeto do tipo Proposicao
    for vot_tree in tree.getchildren():
        if vot_tree.tag == 'Votacao' and vot_tree.get('TipoVotacao') == 'Nominal': # se é votação nominal
            resumo = '%s -- %s' % (vot_tree.get('Materia'), vot_tree.get('Ementa'))
            prop_nome = _prop_nome(resumo) # vai retornar prop_nome se votação for de proposição
            if (prop_nome):  
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
                vot.deputados = _vereadores_from_tree(vot_tree)
                prop.votacoes.append(vot)

    return proposicoes.values()

if __name__ == "__main__":

    props = from_xml(XML2010)
    for p in props:
        print '%s (%d)' % (p.nome(), len(p.votacoes))

    print '**************'
    props = from_xml(XML2011)
    for p in props:
        print '%s (%d)' % (p.nome(), len(p.votacoes))

    print '**************'
    props = from_xml(XML2012)
    for p in props:
        print '%s (%d)' % (p.nome(), len(p.votacoes))

    print '**************'
    print '**************'
    vereadores = props[0].votacoes[0].deputados
    for v in vereadores:
        print v

