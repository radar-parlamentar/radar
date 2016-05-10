# !/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Eduardo Hideo, Leonardo Leite
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

MOCK_PATH = os.path.join(cdep.RESOURCES_FOLDER, 'mocks')
XMLS = glob.glob(os.path.join(MOCK_PATH, '*.xml'))


def parse_arquivo_xml(nome_arquivo):
    """retorna etree"""
    for xml in XMLS:
        if nome_arquivo == os.path.basename(xml):
            with open(xml) as arquivo_xml:
                return etree.fromstring(arquivo_xml.read())
    raise ValueError


def mock_obter_proposicao(id_prop):
    """retorna etree"""
    return parse_arquivo_xml('proposicao_%s.xml' % id_prop)


def mock_listar_proposicoes(sigla, ano):
    """retorna etree"""
    return parse_arquivo_xml('proposicoes_%s%s.xml' % (sigla, ano))


def mock_obter_proposicoes_votadas_plenario(ano):
    """retorna etree"""
    return parse_arquivo_xml('proposicoes_votadas_%s.xml' % ano)


def mock_obter_votacoes(sigla, num, ano):
    """retorna etree"""
    return parse_arquivo_xml('votacoes_%s%s%s.xml' % (sigla, num, ano))

