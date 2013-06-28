#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Guilherme Januário, Diego Rabatone
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

"""módulo cmsp (Câmara Municipal de São Paulo)

Classes:
    ImportadorCMSP
"""

from __future__ import unicode_literals
from django.utils.dateparse import parse_datetime
from modelagem import models
import re
import sys
import os
import xml.etree.ElementTree as etree

# data em que os arquivos XMLs foram atualizados
ULTIMA_ATUALIZACAO = parse_datetime('2012-12-31 0:0:0')

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

# arquivos com os dados fornecidos pela cmsp
XML2010 = os.path.join(MODULE_DIR, 'dados/cmsp/cmsp2010.xml')
XML2011 = os.path.join(MODULE_DIR,'dados/cmsp/cmsp2011.xml')
XML2012 = os.path.join(MODULE_DIR,'dados/cmsp/cmsp2012.xml')
XML2013 = os.path.join(MODULE_DIR,'dados/cmsp/cmsp2013.xml')

# tipos de proposições encontradas nos XMLs da cmsp (2010, 2011, 2012, 2013)
# esta lista ajuda a identificar as votações que são de proposições
# Exemplos de votações que não são de proposições: Adiamento do Prolong. do Expediente; Adiamento dos Demais itens da Pauta.
TIPOS_PROPOSICOES = ['PL', 'PLO', 'PDL']

# regex que captura um nome de proposição (ex: PL 12/2010)
PROP_REGEX = '([a-zA-Z]{1,3}) ([0-9]{1,4}) ?/([0-9]{4})'

INICIO_PERIODO = parse_datetime('2010-01-01 0:0:0')
FIM_PERIODO = parse_datetime('2012-12-31 0:0:0')

# TODO: caso o parlamentar pertenca a partidos distintos, ou, mais generciamente,
#       se sua "legislatura" mudar, caso seu ID, provindo do XML de entrada,
#       continue o mesmo, a primeira legislatura que sobrevalecerah para as demais
#       votacoes tambem. Mas, se o ID corretamente mudar, entao tudo estarah perfeito.
#TODO   Como a LEGISLATURA eh many to many, parece que o parlamentar pode ter varias
#       legislaturas (e ainda por cima no mesmo arquivo entrada). Assim, talvez
#       fosse interessante armazenar a legislatura no VOTO, e não numa lista de legislatura.
#       A nao ser q, a cada voto, o parlamentar esteja relacionada tb a todas as suas legislaturas.

class GeradorCasaLegislativa(object):
    def gerar_cmsp(self):
        self.cmsp = models.CasaLegislativa()
        self.cmsp.nome = 'Câmara Municipal de São Paulo'
        self.cmsp.nome_curto = 'cmsp'
        self.cmsp.esfera = models.MUNICIPAL
        self.cmsp.local = 'São Paulo - SP'
        self.cmsp.atualizacao = ULTIMA_ATUALIZACAO
        self.salvar()
        return self.cmsp
    
    def salvar(self):
        if (models.CasaLegislativa.objects.filter(nome_curto='cmsp').count() == 0):
            self.cmsp.save()


class ImportadorCMSP:
    """Salva os dados dos arquivos XML da cmsp no banco de dados"""

    def __init__(self, cmsp, verbose=False):
        """verbose (booleano) -- ativa/desativa prints na tela"""
        self.verbose = verbose
        self.cmsp = cmsp
        self.parlamentares = {} # mapeia um ID de parlamentar incluso em alguma votacao a um objeto Parlamentar.

    def _converte_data(self, data_str):
        """Converte string "d/m/a para objeto datetime; retona None se data_str é inválido"""
        DATA_REGEX = '(\d\d?)/(\d\d?)/(\d{4})'
        res = re.match(DATA_REGEX, data_str)
        if res:
            new_str = '%s-%s-%s 0:0:0' % (res.group(3), res.group(2), res.group(1))
            return parse_datetime(new_str)
        else:
            return None

    def _prop_nome(self, texto):
        """Procura "tipo num/ano" no texto"""
        res = re.search(PROP_REGEX, texto)
        if res and res.group(1).upper() in TIPOS_PROPOSICOES:
                return res.group(0).upper()
        else:
            return None

    def tipo_num_anoDePropNome(self, prop_nome):
        """Extrai ano de "tipo num/ano" """
        res = re.search(PROP_REGEX, prop_nome)
        if res:
            return res.group(1),res.group(2),res.group(3)
        else:
            return None, None, None


    def _voto_cmsp_to_model(self, voto):
        """Interpreta voto como tá no XML e responde em adequação a modelagem em models.py"""

        if voto == 'Não':
            return models.NAO
        elif voto == 'Sim':
            return models.SIM
        elif voto == 'Não votou':
            return models.AUSENTE
        elif voto == 'Abstenção':
            return models.ABSTENCAO
        else:
            print 'tipo de voto (%s) não mapeado!' % voto
            return models.ABSTENCAO

    def _partido(self, nome_partido):
        nome_partido = nome_partido.strip()
        partido = models.Partido.from_nome(nome_partido)
        if partido == None:
            print 'Não achou o partido %s' % nome_partido
            partido = models.Partido.get_sem_partido()
        return partido

    def _votante(self, ver_tree):
        id_parlamentar = ver_tree.get('IDParlamentar')
        if self.parlamentares.has_key(id_parlamentar):
            votante = self.parlamentares[id_parlamentar]
        else:
            votante = models.Parlamentar()
            votante.save()
            votante.id_parlamentar = id_parlamentar
            votante.nome =  ver_tree.get('NomeParlamentar')
            votante.save()
            if self.verbose:
                print 'Vereador %s salvo' % votante
            self.parlamentares[id_parlamentar] = votante
            #TODO genero
        return votante

    def _legislatura(self, ver_tree):
        """Cria e retorna uma legistura para o partido fornecido"""

        partido = self._partido(ver_tree.get('Partido'))
        votante = self._votante(ver_tree)

        legs = models.Legislatura.objects.filter(parlamentar=votante,partido=partido,casa_legislativa=self.cmsp)
        # TODO acima filtrar tb por inicio e fim
        if legs:
            leg = legs[0]
        else:
            leg = models.Legislatura()
            leg.parlamentar = votante
            leg.partido = partido
            leg.casa_legislativa = self.cmsp
            leg.inicio = INICIO_PERIODO # TODO este período deve ser mais refinado para suportar caras que trocaram de partido
            leg.fim = FIM_PERIODO
            leg.save()

        return leg

    def _votos_from_tree(self, vot_tree, votacao):
        """Extrai lista de votos do XML da votação e as salva no banco de dados.

        Argumentos:
           vot_tree -- etree dos votos
           votacao -- objeto do tipo Votacao
        """
        for ver_tree in vot_tree.getchildren():
            if ver_tree.tag == 'Vereador':
                leg = self._legislatura(ver_tree)
                voto = models.Voto()
                voto.legislatura = leg
                voto.votacao = votacao
                voto.opcao = self._voto_cmsp_to_model(ver_tree.get('Voto'))
                if voto.opcao != None:
                    voto.save()

    def _from_xml_to_bd(self, xml_file):
        """Salva no banco de dados do Django e retorna lista das votações"""

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
                prop_nome = self._prop_nome(resumo) # vai retornar prop_nome se votação for de proposição
                # se a votacao for associavel a uma proposicao, entao..
                if (prop_nome):
                    # a proposicao aa qual a votacao sob analise se refere jah estava no dicionario (eba!)
                    if proposicoes.has_key(prop_nome):
                        prop = proposicoes[prop_nome]
                    # a prop. nao estava ainda, entao devemo-la tanto  criar qnt cadastrar no dicionario.
                    else:
                        prop = models.Proposicao()
                        prop.sigla, prop.numero, prop.ano = self.tipo_num_anoDePropNome(prop_nome)
                        prop.casa_legislativa = self.cmsp
                        proposicoes[prop_nome] = prop

                    if self.verbose:
                        print 'Proposição %s salva' % prop
                    prop.save()
                    vot = models.Votacao()
                    vot.save() # só pra criar a chave primária e poder atribuir o votos
                    vot.id_vot = vot_tree.get('VotacaoID')
                    vot.descricao = resumo
                    vot.data = self._converte_data(vot_tree.get('DataDaSessao'))
                    vot.resultado = vot_tree.get('Resultado')
                    self._votos_from_tree(vot_tree, vot)
                    vot.proposicao = prop
                    if self.verbose:
                        print 'Votação %s salva' % vot
                    else:
                        self.progresso()
                    vot.save()

                    votacoes.append(vot)

        return votacoes

    def progresso(self):
        """Indica progresso na tela"""
        sys.stdout.write('x')
        sys.stdout.flush()

    def importar_de(self,xml):
        """Salva informações no banco de dados do Django

        Retorna lista das votações
        """

        if self.verbose:
            print "importando de: " + str(xml)
        vots = self._from_xml_to_bd(xml)

        #if self.verbose:
        #    print '*** 2013 ***'
        #vots.append(self._from_xml_to_bd(XML2013))

        return vots

def main():
    print 'IMPORTANDO DADOS DA CÂMARA MUNICIPAL DE SÃO PAULO (CMSP)'
    gerador_casa = GeradorCasaLegislativa()
    cmsp = gerador_casa.gerar_cmsp()
    importer = ImportadorCMSP(cmsp)
    importer.importar_de(XML2010)
    importer.importar_de(XML2011)
    importer.importar_de(XML2012)
    print 'Importação dos dados da Câmara Municipal de São Paulo (CMSP) terminada'

