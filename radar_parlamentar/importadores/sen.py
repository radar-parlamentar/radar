# !/usr/bin/python
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
    CasaLegislativaGerador
    ImportadorVotacoesSenado
"""

from __future__ import unicode_literals
from datetime import date
from modelagem import models
from django.core.exceptions import ObjectDoesNotExist
from chefes_executivos import ImportadorChefesExecutivos
import re
import os
import sys
import xml.etree.ElementTree as etree
import logging

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

# pasta com os arquivos com os dados fornecidos pelo senado
DATA_FOLDER = os.path.join(MODULE_DIR, 'dados/senado')
VOTACOES_FOLDER = os.path.join(DATA_FOLDER, 'votacoes')

NOME_CURTO = 'sen'

XML_FILE = 'dados/chefe_executivo/chefe_executivo_sen.xml'

logger = logging.getLogger("radar")


class CasaLegislativaGerador:

    def gera_senado(self):
        """Gera objeto do tipo CasaLegislativa representando o Senado"""

        if not models.CasaLegislativa.objects.filter(nome_curto=NOME_CURTO):
            sen = models.CasaLegislativa()
            sen.nome = 'Senado'
            sen.nome_curto = NOME_CURTO
            sen.esfera = models.FEDERAL
            sen.save()
        else:
            sen = models.CasaLegislativa.objects.get(nome_curto=NOME_CURTO)
        return sen


class ImportadorVotacoesSenado:

    """Salva os dados dos arquivos XML do senado no banco de dados"""

    def __init__(self):
        self.senado = models.CasaLegislativa.objects.get(nome_curto=NOME_CURTO)
        self.parlamentares = self._init_parlamentares()
        self.proposicoes = self._init_proposicoes()

    def _init_parlamentares(self):
        """retorna dicionário
           (nome_parlamentar, nome_partido, localidade) -> Parlamentar"""
        parlamentares = {}
        for p in models.Parlamentar.objects.filter(
                casa_legislativa=self.senado):
            parlamentares[self._key(p)] = p
        return parlamentares

    def _key(self, parlamentar):
        return (parlamentar.nome,
                parlamentar.partido.nome,
                parlamentar.localidade)

    def _init_proposicoes(self):
        """retorna dicionário "sigla num/ano" -> Proposicao"""
        proposicoes = {}
        for p in models.Proposicao.objects.filter(
                casa_legislativa=self.senado):
            proposicoes[p.nome()] = p
        return proposicoes

    def _converte_data(self, data_str):
        """Converte string "aaaa-mm-dd para objeto datetime;
        retona None se data_str é inválido"""
        DATA_REGEX = '(\d{4})-(\d{2})-(\d{2})'
        res = re.match(DATA_REGEX, data_str)
        if res:
            return date(int(res.group(1)), int(res.group(2)),
                        int(res.group(3)))
        else:
            raise ValueError

    def _voto_senado_to_model(self, voto):
        """Interpreta voto como tá no XML e responde em adequação a modelagem
        em models.py"""

        DESCULPAS = ['MIS', 'MERC', 'P-NRV', 'REP',
                     'AP', 'LA', 'LAP', 'LC', 'LG', 'LS', 'NA']

        # XML não tá em UTF-8, acho q vai dar probema nessas comparações!
        if voto == 'Não':
            return models.NAO
        elif voto == 'Sim':
            return models.SIM
        elif voto == 'NCom':
            return models.AUSENTE
        elif voto in DESCULPAS:
            return models.AUSENTE
        elif voto == 'Abstenção':
            return models.ABSTENCAO
        elif voto == 'P-OD':  # obstrução
            return models.ABSTENCAO
        else:
            return models.ABSTENCAO

    def _find_partido(self, nome_partido):
        nome_partido = nome_partido.strip()
        partido = models.Partido.from_nome(nome_partido)
        if partido is None:
            logger.warn('Não achou o partido %s' % nome_partido)
            partido = models.Partido.get_sem_partido()
        return partido

    def _find_parlamentar(self, voto_parlamentar_tree):
        nome_senador = voto_parlamentar_tree.find('NomeParlamentar').text
        nome_partido = voto_parlamentar_tree.find('SiglaPartido').text
        localidade = voto_parlamentar_tree.find('SiglaUF').text
        partido = self._find_partido(nome_partido)
        key = (nome_senador, partido.nome, localidade)
        if key in self.parlamentares:
            senador = self.parlamentares[key]
        else:
            codigo = voto_parlamentar_tree.find('CodigoParlamentar').text
            sexo = voto_parlamentar_tree.find('SexoParlamentar').text
            senador = models.Parlamentar()
            senador.id_parlamentar = codigo
            senador.nome = nome_senador
            senador.genero = sexo
            senador.casa_legislativa = self.senado
            senador.partido = partido
            senador.localidade = localidade
            senador.save()
            self.parlamentares[key] = senador
            self.progresso()
        return senador

    def _votos_from_tree(self, votos_tree, votacao):
        """Faz o parse dos votos, salva no BD e devolve lista de votos
           Retorna lista dos votos salvos
        """
        votos = []
        for voto_parlamentar_tree in votos_tree:
            senador = self._find_parlamentar(voto_parlamentar_tree)
            voto = models.Voto()
            voto.parlamentar = senador
            voto.votacao = votacao
            voto.opcao = self._voto_senado_to_model(
                voto_parlamentar_tree.find('Voto').text)
            voto.save()
            votos.append(voto)
        return votos

    def _nome_prop_from_tree(self, votacao_tree):

        sigla = votacao_tree.find('SiglaMateria').text
        numero = votacao_tree.find('NumeroMateria').text
        ano = votacao_tree.find('AnoMateria').text
        return '%s %s/%s' % (sigla, numero, ano)

    def _proposicao_from_tree(self, votacao_tree):

        prop_nome = self._nome_prop_from_tree(votacao_tree)
        if prop_nome in self.proposicoes:
            prop = self.proposicoes[prop_nome]
        else:
            prop = models.Proposicao()
            prop.sigla = votacao_tree.find('SiglaMateria').text
            prop.numero = votacao_tree.find('NumeroMateria').text
            prop.ano = votacao_tree.find('AnoMateria').text
            prop.casa_legislativa = self.senado
            prop.save()
            self.proposicoes[prop_nome] = prop
        return prop

    def _from_xml_to_bd(self, xml_file):
        """Salva no banco de dados do Django e retorna lista das votações"""

        f = open(xml_file, 'r')
        xml = f.read()
        f.close()
        tree = etree.fromstring(xml)

        votacoes = []
        # Pelo q vimos, nesses XMLs não há votações 'inúteis' (homenagens etc)
        # como na cmsp (exceto as secretas)
        votacoes_tree = tree.find('Votacoes')
        if votacoes_tree is not None:
            for votacao_tree in votacoes_tree:
                # se votação não é secreta
                votacao_secreta = votacao_tree.find('Secreta').text
                if votacao_tree.tag == 'Votacao' and votacao_secreta == 'N':

                    codigo = votacao_tree.find('CodigoSessaoVotacao').text
                    votacoes_query = models.Votacao.objects.filter(
                        id_vot=codigo)

                    if votacoes_query:
                        votacao = votacoes_query[0]
                        votacoes.append(votacao)
                    else:
                        proposicao = self._proposicao_from_tree(votacao_tree)
                        self.progresso()
                        votacao = models.Votacao()
                        votacao.id_vot = codigo
                        # só pra criar a chave primária e poder atribuir o
                        # votos
                        votacao.save()
                        votacao.descricao = votacao_tree.find(
                            'DescricaoVotacao').text
                        votacao.data = self._converte_data(
                            votacao_tree.find('DataSessao').text)
                        if votacao_tree.find('Resultado') is not None:
                            votacao.resultado = votacao_tree.find(
                                'Resultado').text
                        votacao.proposicao = proposicao
                        votos_tree = votacao_tree.find('Votos')
                        if votos_tree is not None:
                            votos = self._votos_from_tree(votos_tree, votacao)
                            if not votos:
                                logger.warn(
                                    'Votação desconsiderada (sem votos)')
                                votacao.delete()
                            else:
                                votacao.save()
                                votacoes.append(votacao)
                        else:
                            logger.warn(
                                'Votação desconsiderada (votos_tree nulo)')
                            votacao.delete()
        return votacoes

    def progresso(self):
        """Indica progresso na tela"""
        sys.stdout.write('x')
        sys.stdout.flush()

    def _xml_file_names(self):
        """Retorna uma lista com os caminhos dos arquivos XMLs contidos
        na pasta VOTACOES_FOLDER"""
        files = os.listdir(VOTACOES_FOLDER)
        xmls = filter(lambda name: name.endswith('.xml'), files)
        xmls = map(lambda name: os.path.join(VOTACOES_FOLDER, name), xmls)
        return xmls

    def importar_votacoes(self):
        """# for xml_file in
        ['importadores/dados/senado/votacoes/ListaVotacoes2014.xml',
        'importadores/dados/senado/votacoes/ListaVotacoes2015.xml']:
        # facilita debug"""
        for xml_file in self._xml_file_names():
            logger.info('Importando %s' % xml_file)
            self._from_xml_to_bd(xml_file)


class PosImportacao:

    def processar(self):
        self.consertar_suplicy_sem_partido()

    # Issue #325
    def consertar_suplicy_sem_partido(self):
        try:
            suplicy_sem_partido = models.Parlamentar.objects.get(
                nome='Eduardo Suplicy',
                partido__numero=0,
                casa_legislativa__nome_curto='sen')
            suplicy_do_pt = models.Parlamentar.objects.get(
                nome='Eduardo Suplicy',
                partido__numero=13,
                casa_legislativa__nome_curto='sen')
            votos = models.Voto.objects.filter(parlamentar=suplicy_sem_partido)
            for v in votos:
                v.parlamentar = suplicy_do_pt
                v.save()
            suplicy_sem_partido.delete()
        except ObjectDoesNotExist:
            logger.warn('Eduardo Suplicy sem partido não existe.')


def main():
    logger.info('IMPORTANDO DADOS DO SENADO')
    geradorCasaLeg = CasaLegislativaGerador()
    geradorCasaLeg.gera_senado()
    logger.info('IMPORTANDO CHEFES EXECUTIVOS DO SENADO')
    importer_chefe = ImportadorChefesExecutivos(NOME_CURTO, 'Presidentes', 'Presidente', XML_FILE)
    importer_chefe.importar_chefes()
    logger.info('IMPORTANDO VOTAÇÕES DO SENADO')
    importer = ImportadorVotacoesSenado()
    importer.importar_votacoes()
    logger.info('PROCESSAMENTO PÓS-IMPORTAÇÃO')
    posImportacao = PosImportacao()
    posImportacao.processar()
    logger.info('IMPORTANDO INDICES DO SENADO')
    import importadores.sen_indexacao as indexacao_senado
    indexacao_senado.indexar_proposicoes()
