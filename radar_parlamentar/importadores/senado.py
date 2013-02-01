#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite
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

"""módulo senado

Classes:
    ImportadorSenado
"""

from __future__ import unicode_literals
from django.utils.dateparse import parse_datetime
from modelagem import models
import re
import sys
import os
import xml.etree.ElementTree as etree

# data em que os arquivos XMLs foram atualizados
ULTIMA_ATUALIZACAO = parse_datetime('2013-02-01 0:0:0')

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

# pasta com os arquivos com os dados fornecidos pelo senado
DATA_FOLDER = os.path.join(MODULE_DIR, 'dados/senado')


# TODO refinar períodos das legislaturas
INICIO_PERIODO = parse_datetime('2005-01-01 0:0:0')
FIM_PERIODO = parse_datetime('2012-12-31 0:0:0')

class ImportadorSenado:
    """Salva os dados dos arquivos XML do senado no banco de dados"""

    def __init__(self, verbose=False):
        """verbose (booleano) -- ativa/desativa prints na tela"""

        self.verbose = verbose
        self.senado = None
        
        self.parlamentares = {} # mapeia um ID de parlamentar incluso em alguma votacao a um objeto Parlamentar.

    def _gera_casa_legislativa(self):
        """Gera objeto do tipo CasaLegislativa representando o Senado"""

        sen = models.CasaLegislativa()
        sen.nome = 'Senado'
        sen.nome_curto = 'sen'
        sen.esfera = models.FEDERAL
        sen.atualizacao = ULTIMA_ATUALIZACAO
        sen.save()
        return sen

    def _converte_data(self, data_str):
        """Converte string "d/m/a para objeto datetime; retona None se data_str é inválido"""
        DATA_REGEX = '(\d\d?)/(\d\d?)/(\d{4})'
        res = re.match(DATA_REGEX, data_str)
        if res:
            new_str = '%s-%s-%s 0:0:0' % (res.group(3), res.group(2), res.group(1))
            return parse_datetime(new_str)
        else:
            return None

    def _voto_senado_to_model(self, voto):
        """Interpreta voto como tá no XML e responde em adequação a modelagem em models.py"""
        
        DESCULPAS = ['MIS', 'MERC', 'P-NRV', 'REP', 'AP', 'LA', 'LAP', 'LC', 'LG', 'LS', 'NA']
        
        if voto == 'Não':          # XML não tá em UTF-8, acho q vai dar probema nessas comparações!
            return models.NAO
        elif voto == 'Sim':
            return models.SIM
        elif voto == 'NCom':
            return models.AUSENTE
        elif voto in DESCULPAS:
            return models.AUSENTE
        elif voto == 'Abstenção':
            return models.ABSTENCAO
        elif voto == 'P-OD': # obstrução
            return models.ABSTENCAO
        else:
            print 'tipo de voto (%s) não mapeado!' % voto
            return models.ABSTENCAO

    def _from_xml_to_bd(self, xml_file):
        """Salva no banco de dados do Django e retorna lista das votações"""

        votacoes = []
        # Comece implementando aqui : )
        # Cuidado com as votações secretas! Devemos ignorá-las
        # Uma votação secreta tb tem uma lista de votos,
        # mas só pra dizer se o cara votou ou não
        # Pelo q vimos, nesses XMLs não há votações 'inúteis' (homenagens etc) como na cmsp (exceto as secretas)
        return votacoes
    
    def progresso(self):
        """Indica progresso na tela"""
        print('.'),
        
    def _xml_file_names(self):
        """Retorna uma lista com os caminhos dos arquivos XMLs contidos na pasta DATA_FOLDER"""
        raise NotImplemented

    def importar(self):
        """Salva informações no banco de dados 
        Retorna lista das votações
        """
        self.senado = self._gera_casa_legislativa()
        votacoes = []
        for xml_file in self._xml_files(): 
            if self.verbose:
                print 'Importando %s' % xml_file
            votacoes.append(self.from_xml_to_bd(xml_file))
        return votacoes

def main():

    print 'IMPORTANDO DADOS DO SENADO'
    importer = ImportadorSenado()
    importer.importar()
        

