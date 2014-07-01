# !/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Diego Rabatone
#
# This file is part of Radar Parlamentar.
#
# Radar Parlamentar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Radar Parlamentar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.

import os
import xml.etree.ElementTree as etree
import glob
from importadores import cdep

VOTADAS_FILE_PATH = cdep.RESOURCES_FOLDER + 'votadas_test.txt'
MOCK_PATH = os.path.join(cdep.RESOURCES_FOLDER, 'mocks')
MOCK_PROPOSICAO = glob.glob(os.path.join(MOCK_PATH, 'proposicao_*'))
MOCK_PROPOSICOES = glob.glob(os.path.join(MOCK_PATH, 'proposicoes_*'))
MOCK_VOTACOES = glob.glob(os.path.join(MOCK_PATH, 'votacoes_*'))
MOCK_PROPOSICOES_VOTADAS = glob.glob(
    os.path.join(MOCK_PATH, 'proposicoes_votadas_*'))


def verificar_xml(nome, lista_xmls):
    """verifica se existe um arquivo com determinado nome, dentro de uma
    lista de arquivos"""
    for xml in lista_xmls:
        if nome == os.path.basename(xml):
            with open(xml) as arquivo_xml:
                return etree.fromstring(arquivo_xml.read())
    raise ValueError


def mock_obter_proposicao(id_prop):
    """mock do método obter_proposicao de camaraWS.
        Recebe o id da proposição e retorna um xml"""
    return verificar_xml('proposicao_' + str(id_prop), MOCK_PROPOSICAO)


def mock_listar_proposicoes(sigla, ano):
    """mock do método listar_proposicoes de camaraWS.
        Recebe a sigla e o ano da proposicao e retorna um xml"""
    return verificar_xml('proposicoes_' + sigla + str(ano), MOCK_PROPOSICOES)


def mock_obter_proposicoes_votadas_plenario(ano):
    """mock do método mock_obter_proposicoes_com_votacoes de camaraWS.
        Recebe o ano da proposicao e retorna um xml"""
    return verificar_xml('proposicoes_votadas_' + str(
        ano), MOCK_PROPOSICOES_VOTADAS)


def mock_obter_votacoes(sigla, num, ano):
    """mock do método obter_votacoes de camaraWS.
        Recebe a sigla, o numero e o ano e retorna um xml"""
    return verificar_xml('votacoes_' + sigla + str(num) + str(
        ano), MOCK_VOTACOES)
