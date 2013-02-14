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
import logging

logger = logging.getLogger("radar")

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

    def __init__(self):
        """verbose (booleano) -- ativa/desativa prints na tela"""

        self.senado = None
        self.parlamentares = {} # mapeia um ID de parlamentar incluso em alguma votacao a um objeto Parlamentar.
        self.proposicoes = {} # chave é o nome da proposição (sigla num/ano), valor é objeto Proposicao

    def _gera_casa_legislativa(self):
        """Gera objeto do tipo CasaLegislativa representando o Senado"""

        if not models.CasaLegislativa.objects.filter(nome_curto='sen'):
            sen = models.CasaLegislativa()
            sen.nome = 'Senado'
            sen.nome_curto = 'sen'
            sen.esfera = models.FEDERAL
            sen.atualizacao = ULTIMA_ATUALIZACAO
            sen.save()
        else:
            sen = models.CasaLegislativa.objects.get(nome_curto='sen')
        return sen

    def _converte_data(self, data_str):
        """Converte string "aaaa-mm-dd para objeto datetime; retona None se data_str é inválido"""
        DATA_REGEX = '(\d{4})-(\d{2})-(\d{2})'
        res = re.match(DATA_REGEX, data_str)
        if res:
            new_str = '%s-%s-%s 0:0:0' % (res.group(1), res.group(2), res.group(3))
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

    def _partido(self, codigo_parlamentar):

        # TODO tem que consultar outro XML pra descobrir o partido!
        partido = models.Partido()
        partido.nome = 'Fake'
        partido.numero = 0
        return partido

    def _parlamentar_from_tree(self, voto_parlamentar_tree):
        
        codigo_parlamentar = voto_parlamentar_tree.find('CodigoParlamentar').text
        if self.parlamentares.has_key(codigo_parlamentar):
            votante = self.parlamentares[codigo_parlamentar]
        else:
            votante = models.Parlamentar()
            votante.save()
            votante.id_parlamentar = codigo_parlamentar
            votante.nome =  voto_parlamentar_tree.find('NomeParlamentar').text
            votante.genero = voto_parlamentar_tree.find('SexoParlamentar').text
            #votante.save()
            logger.debug('Senador %s salvo' % votante)
            self.parlamentares[codigo_parlamentar] = votante
        return votante
    
    def _legislatura_from_tree(self, voto_parlamentar_tree):
        """Cria e retorna uma legistura"""
        
        codigo_parlamentar = voto_parlamentar_tree.find('CodigoParlamentar').text
        partido = self._partido(codigo_parlamentar)
        parlamentar = self._parlamentar_from_tree(voto_parlamentar_tree)
        legs = models.Legislatura.objects.filter(parlamentar=parlamentar,partido=partido,casa_legislativa=self.senado)
        # TODO acima filtrar tb por inicio e fim
        if legs:
            leg = legs[0]
        else:
            leg = models.Legislatura()
            leg.parlamentar = parlamentar
            leg.partido = partido
            leg.casa_legislativa = self.senado
            leg.inicio = INICIO_PERIODO # TODO este período deve ser mais refinado para suportar caras que trocaram de partido
            leg.fim = FIM_PERIODO
            #leg.save()
        return leg

    def _votos_from_tree(self, votos_tree, votacao):
        """Faz o parse dos votos, salva no BD e devolve lista de votos"""
        
        for voto_parlamentar_tree in votos_tree:
            legislatura = self._legislatura_from_tree(voto_parlamentar_tree)
            voto = models.Voto()
            voto.legislatura = legislatura
            voto.votacao = votacao
            voto.opcao = self._voto_senado_to_model(voto_parlamentar_tree.find('Voto').text)
            #if voto.opcao != None:
            #    voto.save()

    def _nome_prop_from_tree(self, votacao_tree):
        
        sigla = votacao_tree.find('SiglaMateria').text
        numero = votacao_tree.find('NumeroMateria').text
        ano = votacao_tree.find('AnoMateria').text
        return '%s %s/%s' % (sigla, numero, ano)
    
    def _proposicao_from_tree(self, votacao_tree):
        
        prop_nome = self._nome_prop_from_tree(votacao_tree)
        if self.proposicoes.has_key(prop_nome):
            prop = self.proposicoes[prop_nome]
        else:
            prop = models.Proposicao()
            prop.sigla = votacao_tree.find('SiglaMateria').text
            prop.numero = votacao_tree.find('NumeroMateria').text
            prop.ano = votacao_tree.find('AnoMateria').text
            prop.casa_legislativa = self.senado
            self.proposicoes[prop_nome] = prop
        return prop
        

    def _from_xml_to_bd(self, xml_file):
        """Salva no banco de dados do Django e retorna lista das votações"""

        f = open(xml_file, 'r')
        xml = f.read()
        f.close()
        tree = etree.fromstring(xml)

        votacoes = []        
        # Pelo q vimos, nesses XMLs não há votações 'inúteis' (homenagens etc) como na cmsp (exceto as secretas)
        for votacao_tree in tree.find('Votacoes'):
            if votacao_tree.tag == 'Votacao' and votacao_tree.find('Secreta').text == 'N': # se votação não é secreta
                proposicao = self._proposicao_from_tree(votacao_tree)
                nome = '%s %s/%s' % (proposicao.sigla, proposicao.numero, proposicao.ano)
                logger.debug('Importando %s' % nome)
                votacao = models.Votacao()
                #votacao.save() # só pra criar a chave primária e poder atribuir o votos
                votacao.id_vot = votacao_tree.find('CodigoTramitacao').text
                votacao.descricao = votacao_tree.find('DescricaoVotacao').text
                votacao.data = self._converte_data(votacao_tree.find('DataSessao').text)
                votacao.resultado = votacao_tree.find('Resultado').text
                votacao.proposicao = proposicao
                votos_tree = votacao_tree.find('Votos')
                self._votos_from_tree(votos_tree, votacao)
                votacoes.append(votacao)
        
        return votacoes
    
    def progresso(self):
        """Indica progresso na tela"""
        print('.'),
        
    def _xml_file_names(self):
        """Retorna uma lista com os caminhos dos arquivos XMLs contidos na pasta DATA_FOLDER"""
        files = os.listdir(DATA_FOLDER)
        xmls = filter(lambda name: name.endswith('.xml'), files)
        xmls = map(lambda name: os.path.join(DATA_FOLDER, name), xmls)
        return xmls

    def importar(self):
        """Salva informações no banco de dados 
        Retorna lista das votações
        """
        self.senado = self._gera_casa_legislativa()
        votacoes = []
        #for xml_file in ['importadores/dados/senado/ListaVotacoes2007.xml']: # facilita debug 
        for xml_file in self._xml_file_names():
            logger.info('Importando %s' % xml_file)
            votacoes += self._from_xml_to_bd(xml_file)
        return votacoes

def main():

    logger.info('IMPORTANDO DADOS DO SENADO')
    importer = ImportadorSenado()
    votacoes = importer.importar()
    print votacoes
        

