# -*- coding: utf-8 -*-

# Copyright (C) 2012, Leonardo Leite, Diego Rabatone
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

"""Módulo camaraws -- requisições para os Web Services da câmara

Funcões:
obter_votacao -- obtém votacões e detalhes de uma proposicão
"""

from model import Proposicao
import urllib2
import xml.etree.ElementTree as etree
import io

OBTER_VOTACOES_PROPOSICAO = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=%s&numero=%s&ano=%s'
OBTER_INFOS_PROPOSICAO = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicao?tipo=%s&numero=%s&ano=%s'

def obter_votacao(tipo, num, ano):
    """Obtém votacões e detalhes de uma proposicão

    Argumentos:
    tipo, num, ano -- strings que caracterizam a proposicão

    Retorna:
    Uma proposicão como um objeto da classe model.Proposicao
    Caso a proposição não seja encontrada ou não possua votações, retorna None
    """
    url  = OBTER_VOTACOES_PROPOSICAO % (tipo, num, ano)
    try:
        request = urllib2.Request(url)
        xml = urllib2.urlopen(request).read()
    except urllib2.URLError:
        return None

    try:
        prop = Proposicao.fromxml(xml)
    except:
        return None
    if not isinstance(prop, Proposicao): 
        return None

    xml = obter_proposicao(tipo, num, ano) #aqui é o xml com mais detalhes sobre a proposição
    tree = etree.fromstring(xml)
    prop.id = tree.find('idProposicao').text
    prop.ementa = tree.find('Ementa').text
    prop.explicacao = tree.find('ExplicacaoEmenta').text
    prop.situacao = tree.find('Situacao').text 
    return prop

def obter_proposicao(tipo, num, ano):
    """Obtém detalhes da proposição por tipo, número e ano

    Argumentos:
    tipo, num, ano -- strings que caracterizam a proposicão

    Retorna:
    Um xml represenando a proposicão como um objeto da classe bytes
    """
    url = OBTER_INFOS_PROPOSICAO % (tipo, num, ano)
    request = urllib2.Request(url)
    xml = urllib2.urlopen(request).read()
    return xml

