#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Guilherme Januário
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
from modelagem import models
import re
import xml.etree.ElementTree as etree

# arquivos com os dados fornecidos pela cmsp
XML2010 = 'importers/dados/cmsp2010.xml'
XML2011 = 'importers/dados/cmsp2011.xml'
XML2012 = 'importers/dados/cmsp2012.xml'

# tipos de proposições encontradas nos XMLs da cmsp (2010, 2011, 2012)
# esta lista ajuda a identificar as votações que são de proposições
# Exemplos de votações que não são de proposições: Adiamento do Prolong. do Expediente; Adiamento dos Demais itens da Pauta. 
TIPOS_PROPOSICOES = ['PL', 'PLO', 'PDL']

# regex que captura um nome de proposição (ex: PL 12/2010)
PROP_REGEX = '([a-zA-Z]{1,3}) ([0-9]{1,4}) ?/([0-9]{4})' 

# @parlamentares: Mapeia um ID de parlamentar incluso nalguma votacao a um OBJETO parlamentar.
# TODO: caso o parlamentar pertenca a partidos distintos, ou, mais generciamente,
#       se sua "legislatura" mudar, caso seu ID, provindo do XML de entrada,
#       continue o mesmo, a primeira legislatura que sobrevalecerah para as demais
#       votacoes tambem. Mas, se o ID corretamente mudar, entao tudo estarah perfeito.
#TODO   Como a LEGISLATURA eh many to many, parece que o parlamentar pode ter varias
#       legislaturas (e ainda por cima no mesmo arquivo entrada). Assim, talvez
#       fosse interessante armazenar a legislatura no VOTO, e não numa lista de legislatura.
#       A nao ser q, a cada voto, o parlamentar esteja relacionada tb a todas as suas legislaturas.

parlamentares = {}

def _prop_nome(texto):
    """Procura "tipo num/ano" no texto"""
    res = re.search(PROP_REGEX, texto)
    if res and res.group(1).upper() in TIPOS_PROPOSICOES:
            return res.group(0).upper()
    else:
        return None

def tipo_num_anoDePropNome(prop_nome):
    """Extrai ano de "tipo num/ano" """
    res = re.search(PROP_REGEX, prop_nome)
    if res:
        return res.group(1),res.group(2),res.group(3)
    else:
        return None, None, None


def _voto_cmsp_to_model(voto):
    """Interpreta voto como tá no XML e responde em adequação a modelagem em models.py
    Em especial, "Não votou" é mapeado para abstenção
    """
    
    if voto == 'Não':
        return models.OPCOES[1][0]
    if voto == 'Sim':
        return models.OPCOES[0][0]
    if voto == 'Não votou':
        return models.OPCOES[2][0] 

def _votos_from_tree(vot_tree):
    """Extrai lista de votos do XML da votação.
        Preenche tambem um vetor contendo a descricao de cada parlamentar."""
    votos = []

    for ver_tree in vot_tree.getchildren():
        if ver_tree.tag == 'Vereador':
            key = ver_tree.get('IDParlamentar')
            print 'procurando por ',key
            if parlamentares.has_key(key):
                print 'achou'
                votante = parlamentares[key]
            else:
                votante = models.Parlamentar() # TODO classe Deputado deve virar Parlamentar
                votante.id_parlamentar = key
                votante.nome = ver_tree.get('NomeParlamentar')
                parlamentares[key] = votante
                #TODO genero, legislatura - da pra preencher +- a legislatura

            voto = models.Voto()
            voto.parlamentar = votante
            voto.opcao = _voto_cmsp_to_model(ver_tree.get('Voto'))
            votos.append(voto)
    return votos
          

def from_xml(xml_file=XML2011):

    f = open(xml_file, 'r')
    xml = f.read()
    f.close()
    tree = etree.fromstring(xml)

    proposicoes = {} # chave é string (ex: 'pl 127/2004'); valor é objeto do tipo Proposicao
    votacoes = []

    for vot_tree in tree.getchildren():
        if vot_tree.tag == 'Votacao' and vot_tree.get('TipoVotacao') == 'Nominal': # se é votação nominal
            resumo = '%s -- %s' % (vot_tree.get('Materia'), vot_tree.get('Ementa'))

            # Prop_nome eh como se identificam internamente por ora as propostas.
            # Queremos saber a que proposicao estah associada a votacao analisanda.
            prop_nome = _prop_nome(resumo) # vai retornar prop_nome se votação for de proposição

            # se a votacao for associavel a uma proposicao, entao..
            if (prop_nome):
                # a proposicao aa qual a votacao sob analise se refere jah estava no dicionario (eba!)
                if proposicoes.has_key(prop_nome):
                    prop = proposicoes[prop_nome]
                # a prop. nao estava ainda, entao devemo-la tanto  criar qnt cadastrar no dicionario. 
                else:
                    prop = models.Proposicao()
                    prop.sigla, prop.numero, prop.ano = tipo_num_anoDePropNome(prop_nome)

                    proposicoes[prop_nome] = prop

                vot = models.Votacao()
                vot.save() # só pra criar a chave primária e poder atribuir o votos
                vot.id_vot = vot_tree.get('VotacaoID')
                vot.descricao = resumo
                vot.data = vot_tree.get('DataDaSessao')
                vot.resultado = vot_tree.get('Resultado')
                vot.votos= _votos_from_tree(vot_tree)
                vot.proposicao = prop
                
                votacoes.append(vot)

    return votacoes

if __name__ == "__main__":

    vots = from_xml(XML2010)
    for v in vots:
        print '%s (%s)' % (v.descricao, v.data) 
        for voto in v.votos:
            print voto.parlamentar.nome

#    for v in vots:
#        p = v.proposicao
#        print '%s' % (p.nome())



    print '**************'
    print '**************'
#    vereadores = props[0].votacoes[0].deputados
#    for v in vereadores:
#        print v


