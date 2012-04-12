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
Proposicao -- modela uma proposição parlamentar
Votacao -- modela uma votação pertencente à uma proposição parlamentar
Deputado -- modela o voto de um deputado numa votação
VotoPartido -- representa um conjunto de votos de um partido
VotoUF -- representa um conjunto de votos de uma UF (estado ou distrito federal)
""" 

from __future__ import unicode_literals
import xml.etree.ElementTree as etree
import io

SIM = 'Sim'
NAO = 'Não'
ABSTENCAO = 'Abstenção'
OBSTRUCAO = 'Obstrução' # por hora será interpretado como 'Não'

class Proposicao:
    """Modela uma proposição parlamentar
    Atributos:
    id, sigla, numero, ano, ementa, explicacao, situacao -- strings
    votacaoes -- lista de objetos do tipo Votacao
    """

    def __init__(self):
        self.id = ''
        self.sigla = ''
        self.numero = ''
        self.ano = ''
        self.ementa = ''
        self.explicacao = ''
        self.situacao = ''
        self.votacoes = []
    
    @staticmethod
    def fromxml(xml):
        """Transforma um texto XML em uma proposição
        Argumentos:
        xml -- string contendo o XML retornado do web service que retorna votações de uma proposição

        Retorna:
        Um objeto do tipo Proposicao
        """  
        tree = etree.fromstring(xml)
        prop = Proposicao()
        prop.sigla = tree.find('Sigla').text
        prop.numero = tree.find('Numero').text
        prop.ano = tree.find('Ano').text
        for child in tree.find('Votacoes'):
          vot = Votacao.fromtree(child)
          prop.votacoes.append(vot)
        return prop

    @staticmethod
    def fromxmlid(xml):
        """Transforma um texto XML do ObterProposicaoPorID em um string do tipo "sigla numero/ano"
        Argumentos:
        xml -- string contendo o XML retornado do web service que retorna proposição por id

        Retorna:
        string do tipo "sigla numero/ano", por exemplo fromxmlid(513512) retorna "MPV 540/2011"
        """  
        tree = etree.fromstring(xml)
        nome = tree.find('nomeProposicao').text
        return nome


    def __unicode__(self):
        return "[%s %s/%s]: %s \nEmenta: %s \nSituação: %s" % (self.sigla, self.numero, self.ano, self.explicacao, self.ementa, self.situacao) 

    def __str__(self):
        return unicode(self).encode('utf-8')

class Votacao:
    """Modela uma votação pertencente à uma proposição parlamentar
    Atributos:
    resumo, data, hora -- strings
    deputados -- lista de objetos do tipo Deputado
    """
    def __init__(self): 
        self.resumo = ''
        self.data = ''
        self.hora = ''
        self.deputados = []

    @staticmethod
    def fromtree(tree):
        """Transforma um XML em uma votação
        Argumentos:
        tree -- objeto do tipo xml.etree.ElementTree representando o XML que descreve uma votação

        Retorna:
        Um objeto do tipo Votacao
        """
        vot = Votacao() 
        vot.resumo = tree.attrib['Resumo']
        vot.data = tree.attrib['Data']
        vot.hora = tree.attrib['Hora']
        for child in tree:
          dep = Deputado.fromtree(child)
          vot.deputados.append(dep)
        return vot

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

class Deputado:
    """Modela o voto de um deputado numa votação
    Atributos:
    nome, partido, uf -- strings que caracterizam o deputado
    voto -- voto dado pelo deputado \in {SIM, NAO, ABSTENCAO, OBSTRUCAO}
    """

    def __init__(self):
        self.nome = ''
        self.partido = ''
        self.uf = ''
        self.voto = ''

    @staticmethod
    def fromtree(tree):
        """Transforma um XML no voto de um deputado
        Argumentos:
        tree -- objeto do tipo xml.etree.ElementTree representando o XML que descreve o voto de um deputado

        Retorna:
        Um objeto do tipo Deputado
        """
        dep = Deputado()
        dep.nome = tree.attrib['Nome']
        dep.partido = tree.attrib['Partido']
        dep.uf = tree.attrib['UF']
        dep.voto = tree.attrib['Voto']
        return dep

    def __unicode__(self):
        return "%s (%s-%s) votou %s" % (self.nome, self.partido, self.uf, self.voto)

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
        OBSTRUCAO conta como um voto NAO
        """
        if (voto == SIM):
          self.sim += 1
        if (voto == NAO):
          self.nao += 1
        if (voto == OBSTRUCAO):
          self.nao += 1
        if (voto == ABSTENCAO):
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
    partido -- string
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


