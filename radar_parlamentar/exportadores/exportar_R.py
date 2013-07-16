#!/usr/bin/python
# coding=utf8

# Copyright (C) 2013, Leonardo Leite 
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
import codecs
from modelagem import models
from django.utils.dateparse import parse_datetime

# Resultado da exportação deveria ser lido pelo R com
# dados <- read.table("votes.Rdata", header=TRUE)
# mas ainda não funciona...

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

COALITION_PARTIES = ['PT', 'PCdoB', 'PSB', 'PP', 'PMDB', 'PTB']
# PR, PDT não são coalition?

ROLLCALL = 'rollcall' 
ID = 'id'
NAME = 'name'
PARTY = 'party'
COALITION = 'coalition'
VOTE = 'vote'

LABELS = [ROLLCALL, ID, NAME, PARTY, COALITION, VOTE]

DATA_FILE = 'votes.Rdata'

class RollCallVote:
    
    def __init__(self):
        self.rollcall = 0
        self.id = 0
        self.name = ''
        self.party = ''
        self.coalition = 0
        self.vote = ''
        
    def __unicode__(self):
        return '%s    %s    "%s"    %s    %s    %s' % (self.rollcall, self.id, self.name, self.party, self.coalition, self.vote)        


class ExportadorR:
    
    def __init__(self, nome_curto_casa_legislativa, data_ini, data_fim):
        self.nome_curto = nome_curto_casa_legislativa
        self.ini = data_ini
        self.fim = data_fim
        self.votacoes = None
        self.votes = []

    def exportar(self):
        self.retrieve_votacoes()
        self.transform_data()
        self.write_file()
            
    def retrieve_votacoes(self):
        casa = models.CasaLegislativa.objects.get(nome_curto=self.nome_curto)
        if self.ini == None and self.fim == None:
            self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=casa).order_by('data') 
        if self.ini == None and self.fim != None:
            self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=casa).filter(data__lte=self.fim).order_by('data')
        if self.ini != None and self.fim == None:
            self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=casa).filter(data__gte=self.ini).order_by('data')
        if self.ini != None and self.fim != None:
            self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=casa).filter(data__gte=self.ini, data__lte=self.fim).order_by('data')
    
    def transform_data(self):
        for votacao in self.votacoes:
            votos = votacao.votos()
            for voto in votos:
                legislatura = voto.legislatura
                parlamentar = legislatura.parlamentar
                partido = legislatura.partido
                v = RollCallVote()
                v.rollcall = votacao.id_vot
                v.id = voto.id
                v.name = parlamentar.nome
                v.party = partido.nome
                v.coalition =  self.coalition(partido.nome)
                try:
                    v.vote = self.voto(voto.opcao)
                    self.votes.append(v)
                except:
                    print 'Ignorando voto ', voto.opcao
                
    def coalition(self, nome_partido):
        return '1' if nome_partido in COALITION_PARTIES else '0'
                
    def voto(self, opcao):
        if opcao == models.SIM:
            return 'Y'
        elif opcao == models.NAO:
            return 'N'
        elif opcao == models.ABSTENCAO:
            return 'A'
        elif opcao == models.OBSTRUCAO:
            return 'O'
        else: 
            raise ValueError()
    
    def write_file(self):
        filepath = os.path.join(MODULE_DIR, 'dados', DATA_FILE)
        with codecs.open(filepath, 'wb', 'utf-8') as data_file:
            for label in LABELS:
                data_file.write('%s    ' % label)
            data_file.write('\n')
            for vote in self.votes:
                data_file.write('%s    ' % vote.__unicode__())
                data_file.write('\n')
                
def main():
    data_ini = parse_datetime('2010-06-01 0:0:0')
    data_fim = parse_datetime('2010-06-30 0:0:0')
    exportador = ExportadorR('sen', data_ini, data_fim)
    exportador.exportar()
    
    
    
    
    
    