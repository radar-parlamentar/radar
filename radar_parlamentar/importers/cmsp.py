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

Classes:
    ImportadorCMSP -- salva os dados dos arquivos XML da cmsp no banco de dados
"""

from __future__ import unicode_literals
from django.utils.dateparse import parse_datetime
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

INICIO_PERIODO = parse_datetime('2010-01-01 0:0:0')
FIM_PERIODO = parse_datetime('2011-07-01 0:0:0')

# TODO: caso o parlamentar pertenca a partidos distintos, ou, mais generciamente,
#       se sua "legislatura" mudar, caso seu ID, provindo do XML de entrada,
#       continue o mesmo, a primeira legislatura que sobrevalecerah para as demais
#       votacoes tambem. Mas, se o ID corretamente mudar, entao tudo estarah perfeito.
#TODO   Como a LEGISLATURA eh many to many, parece que o parlamentar pode ter varias
#       legislaturas (e ainda por cima no mesmo arquivo entrada). Assim, talvez
#       fosse interessante armazenar a legislatura no VOTO, e não numa lista de legislatura.
#       A nao ser q, a cada voto, o parlamentar esteja relacionada tb a todas as suas legislaturas.

class ImportadorCMSP:

    def __init__(self):
        self.cmsp = self._gera_casa_legislativa()
        print 'at init %s' % self.cmsp
        self.parlamentares = {} # mapeia um ID de parlamentar incluso em alguma votacao a um objeto Parlamentar.
        self.partidos = {} # chave: nome partido; valor: objeto Partido

    def _gera_casa_legislativa(self):
        """Gera objeto do tipo CasaLegislativa representando a CMSP; salva em self.cmsp"""

        cmsp = models.CasaLegislativa()
        cmsp.nome = 'Câmara Municipal de São Paulo'
        cmsp.nome_curto = 'cmsp'
        cmsp.esfera = models.MUNICIPAL
        cmsp.local = 'São Paulo - SP'
        cmsp.save()
        return cmsp

    def _get_legislatura(self, partido):
        """Cria e retorna uma legistura para o partido fornecido"""

        leg = models.Legislatura()
        leg.casa_legislativa = self.cmsp
        leg.inicio = INICIO_PERIODO
        leg.fim = FIM_PERIODO
        leg.partido = partido
        leg.save()

        return leg

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
        """Interpreta voto como tá no XML e responde em adequação a modelagem em models.py
        Em especial, "Não votou" é mapeado para abstenção
        """
        
        if voto == 'Não':
            return models.NAO
        if voto == 'Sim':
            return models.SIM
        if voto == 'Não votou':
            return models.ABSTENCAO # TODO mudar pra AUSENTE (ter certeza que análise trata isso corretamente)

    def _partido(self, nome_partido):
        nome_partido = nome_partido.strip()
        if self.partidos.has_key(nome_partido):
            partido = self.partidos[nome_partido]
        else:
            partido = models.Partido.from_nome(nome_partido)
            if partido == None:
                print 'Não achou o partido %s' % nome_partido
            partido.save()
            print 'Partido %s salvo' % partido
            self.partidos[nome_partido] = partido
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
            partido = self._partido(ver_tree.get('Partido'))
            votante.partido = partido
            legislatura = self._get_legislatura(partido)
            votante.legislaturas.add(legislatura)
            votante.save() 
            print 'Vereador %s salvo' % votante
            self.parlamentares[id_parlamentar] = votante
            #TODO genero, legislatura - da pra preencher +- a legislatura
        return votante

    def _votos_from_tree(self, vot_tree):
        """Extrai lista de votos do XML da votação.
           Preenche tambem um vetor contendo a descricao de cada parlamentar."""
        votos = []
        for ver_tree in vot_tree.getchildren():
            if ver_tree.tag == 'Vereador':
                votante = self._votante(ver_tree)
                voto = models.Voto()
                voto.parlamentar = votante
                voto.opcao = self._voto_cmsp_to_model(ver_tree.get('Voto'))
                if voto.opcao != None:
                    votos.append(voto)
                    voto.save() # só pra criar a chave primária, pra poder relacionar com a votação
        return votos
              

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

                        proposicoes[prop_nome] = prop

                    print 'Proposição %s salva' % prop
                    prop.save()
                    vot = models.Votacao()
                    vot.save() # só pra criar a chave primária e poder atribuir o votos
                    vot.id_vot = vot_tree.get('VotacaoID')
                    vot.casa_legislativa = self.cmsp
                    vot.descricao = resumo
                    vot.data = self._converte_data(vot_tree.get('DataDaSessao'))
                    vot.resultado = vot_tree.get('Resultado')
                    vot.votos = self._votos_from_tree(vot_tree)
                    vot.proposicao = prop
                    print 'Votação %s salva' % vot
                    vot.save()

                    votacoes.append(vot)

        return votacoes

    def importar(self):
        """Salva informações no banco de dados do Django

        Retorna lista das votações
        """

        print '*** 2010 ***'
        vots = self._from_xml_to_bd(XML2010)
        print '*** 2011 ***'
        vots.append(self._from_xml_to_bd(XML2011))
        print '*** 2012 ***'
        vots.append(self._from_xml_to_bd(XML2012))
        return vots

def main():

    print 'IMPORTANDO DADOS DA CÂMARA MUNICIPAL DE SÃO PAULO (CMSP)'
    importer = ImportadorCMSP()
    importer.importar()
        

