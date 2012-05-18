# -*- coding: utf-8 -*-

# Copyright (C) 2012, Leonardo Leite
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

"""Módulo model -- modelagem do domínio, baseado nos XMLs dos web services da câmara

Classes:
Partido -- modela um partido
Proposicao -- modela uma proposição parlamentar
Votacao -- modela uma votação pertencente à uma proposição parlamentar
Voto -- modela o voto de um deputado numa votação
Parlamentar -- modela um deputado, senador ou vereador
VotoPartido -- representa um conjunto de votos de um partido
VotoUF -- representa um conjunto de votos de uma UF (estado ou distrito federal)

Obs: esta documentação faz referências às constantes deste módulo
ex: \in {SIM, NAO} na descrição de um atributo, quer dizer que o atributo
deve receber como valor as constantes SIM ou NAO deste módulo
""" 

from __future__ import unicode_literals
import xml.etree.ElementTree as etree
import io
import re
import sqlite3 as lite

# tipos de votos
SIM = 'Sim'
NAO = 'Não'
ABSTENCAO = 'Abstenção'
OBSTRUCAO = 'Obstrução' # no PCA interpretada como Abstenção
AUSENTE = 'Ausente' # no PCA interpretada como Abstenção

# tipos de parlamentar
DEPUTADO_FEDERAL = 'Deputado federal'
DEPUTADO_ESTADUAL = 'Deputado estadual'
SENADOR = 'Senador'
VEREADOR = 'Vereador'

# gêneros
MASCULINO = 'M'
FEMENINO = 'F'

UFS = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

class Partido:
    """Modela um partido político
    Atributos:
    nome -- ex: 'PT' [string] 
    numero -- ex: '13' [string]
    """

    def __init__(self, nome='', numero=''):
        self.nome = nome
        self.numero = numero

class Proposicao:
    """Modela uma proposição parlamentar
    Atributos:
    id, sigla, numero, ano, ementa, autor, data_apresentacao, indexacao, situacao -- strings
    votacaoes -- lista de objetos do tipo Votacao
    """

    def __init__(self):
        self.id = ''
        self.sigla = ''
        self.numero = ''
        self.ano = ''
        self.ementa = ''
        self.autor = ''
        self.data_apresentacao = ''
        self.indexacao = ''
        self.situacao = ''
        self.votacoes = []
    
    def __unicode__(self):
        return "[%s %s/%s]: %s \nEmenta: %s \nSituação: %s" % (self.sigla, self.numero, self.ano, self.explicacao, self.ementa, self.situacao) 

    def __str__(self):
        return unicode(self).encode('utf-8')

    def nome(self):
        return "%s %s/%s" % (self.sigla, self.numero, self.ano)

class Votacao:
    """Modela uma votação pertencente à uma proposição parlamentar
    Atributos:
    resumo, data, hora -- strings
    votos -- lista de objetos do tipo Voto
    """
    def __init__(self, id_vot=''): 
        self.id = id_vot
        self.resumo = ''
        self.data = ''
        self.resultado = ''
        self.votos = []

    # TODO
    def por_partido(self):
        """Retorna votos agregados por partido
        Retorna:
        Um dicionário cuja chave é o nome do partido (string) e o valor é um VotoPartido
        """
        dic = {}
        for dep in self.deputados:
          part = dep.partido
          if not part in dic:
            dic[part] = VotoPartido(part)
          voto = dic[part]
          voto.add(dep.voto)
        return dic  
  
    # TODO
    def por_uf(self):
        """Retorna votos agregados por UF
        Retorna:
        Um dicionário cuja chave é o nome da UF (string) e o valor é um VotoUF
        """
        dic = {}
        for dep in self.deputados:
          uf = dep.uf
          if not uf in dic:
            dic[uf] = VotoUF(uf)
          voto = dic[uf]
          voto.add(dep.voto)
        return dic  

    def __unicode__(self):
        return "[%s, %s] %s" % (self.data, self.hora, self.resumo)

    def __str__(self):
        return unicode(self).encode('utf-8')

class Parlamentar:
    """Modela um deputado, senador ou vereador
    Atributos:
    nome, uf -- strings que caracterizam o parlamentar (uf é opcional)
    tipo \in {DEPUTADO_ESTADUAL, DEPUTADO_FEDERAL, SENADOR, VEREADOR}
    genero \in {MASCULINO, FEMININO}
    partido -- objeto do tipo Partido
    """

    def __init__(self, partido=None, idPar=''):
        self.id = idPar
        self.nome = ''
        self.genero = ''
        self.tipo = ''
        self.uf = ''
        self.partido = partido

    def __unicode__(self):
        ufstr = ''
        if self.uf:
            ufstr = '-%s' % self.uf
        return "%s (%s%s)" % (self.nome, self.partido, ufstr)

    def __str__(self):
        return unicode(self).encode('utf-8')

class Voto:
    """Modela o voto de um parlamentar
    Atributos:
    parlamentar -- objeto do tipo Parlamentar
    voto \in {SIM, NAO, ABSTENCAO, OBSTRUCAO, AUSENTE}
    """ 

    def __init__(self, parlamentar, voto):
        self.parlamentar = parlamentar
        self.voto = voto

    def __unicode__(self):
        return "%s votou %s" % (self.parlamentar, self.voto)

    def __str__(self):
        return unicode(self).encode('utf-8')

class VotosAgregados:
    """Representa um conjunto de votos
    Atributos:
    sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto
    """

    def add(self, voto):
        """Adiciona um voto ao conjunto de votos
        Argumentos:
        voto -- string \in {SIM, NAO, ABSTENCAO, OBSTRUCAO}
        OBSTRUCAO e AUSENTE contam como um voto ABSTENCAO
        """
        if (voto == SIM):
          self.sim += 1
        if (voto == NAO):
          self.nao += 1
        if (voto == ABSTENCAO):
          self.abstencao += 1
        if (voto == OBSTRUCAO):
          self.abstencao += 1
        if (voto == OBSTRUCAO):
          self.abstencao += 1

    def __init__(self):
        self.sim = 0
        self.nao = 0
        self.abstencao = 0

    def __unicode__(self):
        return '(%s, %s, %s)' % (self.sim, self.nao, self.abstencao)

    def __str__(self):
        return unicode(self).encode('utf-8')

class VotoPartido(VotosAgregados):
    """Representa um conjunto de votos de um partido
    Atributos:
    sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto
    partido -- nome do partido [string]
    """
    def __init__(self, partido):
        VotosAgregados.__init__(self)
        self.partido = partido

class VotoUF(VotosAgregados):
    """Representa um conjunto de votos de uma UF (estado ou distrito federal)
    Atributos:
    sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto
    uf -- string
    """
    def __init__(self, uf):
        VotosAgregados.__init__(self)
        self.uf = uf


