# coding=utf8

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

from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError

class Partido:
    """Partido político.

    Atributos:
        nome -- string; ex: 'PT' 
        numero -- string; ex: '13'
    """

    def __init__(self):
        self.nome = ''
        self.numero = ''

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return unicode(self).encode('utf-8')


class Proposicao:
    """Proposição parlamentar (proposta de lei).
    
    Atributos:
        id -- string identificadora da proposição
        sigla, numero, ano -- string que juntas formam o nome legal da proposição
        ementa-- descrição sucinta e oficial
        descricao -- descrição mais detalhada
        indexacao -- palavras chaves
        autores -- lista de objetos do tipo Parlamentar
        data_apresentacao -- quando foi proposta
        situacao -- como está agora
        casa_legislativa -- objeto do tipo CasaLegislativa

    Métodos:
        nome: retorna "sigla numero/ano"
    """

    def __init__(self):
        self.id = ''
        self.sigla = ''
        self.numero = ''
        self.ano = ''
        self.ementa = ''
        self.descricao = ''
        self.indexacao = ''
        self.data_apresentacao = ''
        self.situacao = ''
        self.casa_legislativa = None
        self.autores = []

    def nome(self):
        return "%s %s/%s" % (self.sigla, self.numero, self.ano)

    def __unicode__(self):
        return "[%s] %s" % (self.nome, self.ementa) 

    def __str__(self):
        return unicode(self).encode('utf-8')


class Votacao:
    """Votação em planário.
    
    Atributos:
        id, descricao, data, resultado -- strings
        casa_legislativa -- objeto do tipo CasaLegislativa
        proposicao -- objeto do tipo Proposicao
        votos -- lista de objetos do tipo Voto

    Métodos:
        por_partido()
    """

    def __init__(self):
        self.id = ''
        self.descricao = ''
        self.data = ''
        self.resultado = ''
        self.casa_legislativa = None
        self.proposicao = None
        self.votos = []

    def por_partido(self):
        """Retorna votos agregados por partido.

        Retorno: um dicionário cuja chave é o nome do partido (string) e o valor é um VotoPartido
        """
        dic = {}
        for voto in self.votos:
            # TODO poderia ser mais complexo: checar se a data da votação bate com o período da legislatura mais recente
            part = voto.parlamentar.partido_atual() 
            if not part in dic:
                dic[part] = VotoPartido(part.nome)
            voto_partido = dic[part.nome]
            voto_partido.add(voto.opcao)
        return dic

    # TODO def por_uf(self):

    def __unicode__(self):
        if self.data:
            return "[%s] %s" % (self.data, self.descricao) 
        else:
            return self.descricao

    def __str__(self):
        return unicode(self).encode('utf-8')    


class Voto:
    """Um voto dado por um parlamentar em uma votação.

    Atributos:
        parlamentar -- objeto do tipo Parlamentar
        opcao -- qual foi o voto do parlamentar (sim, não, abstenção, obstrução, não votou)
    """

    def __init__(self):
        self.parlamentar = None
        self.opcao = ''

    def __unicode__(self):
        return "%s votou %s" % (self.parlamentar, self.opcao)

    def __str__(self):
        return unicode(self).encode('utf-8')

class Parlamentar:
    """Um parlamentar.

    Atributos:
        id, nome, genero -- strings
        legislatura -- lista de objetos do tipo Legislatura

    Métodos:
        partido_atual()
        legislatura_atual()
    """

    def __init__(self):
        self.id = ''
        self.nome = ''
        self.genero = ''
        self.legislaturas = []

    def partido_atual(self):
        """Retorna partido atual do parlamentar.

        Retorno: objeto do tipo Partido
        """
        return self.legislatura_atual().partido

    def legislatura_atual(self):
        """Retorna legislatura atual do parlamentar.

        Retorno: objeto do tipo Legislatura
        """
        return self.legislaturas[-1] 

    def __unicode__(self):
        leg = self.legislatura_atual()
        if (leg.localidade):
            return "%s (%s-%s)" % (self.nome, leg.partido, leg.localidade)
        else:
            return "%s (%s)" % (self.nome, leg.partido)

    def __str__(self):
        return unicode(self).encode('utf-8')


class Legislatura:
    """O mandato exercido por um parlamentar.

    Atributos:
        id -- string identificadora da legislatura
        localidade -- string; ex 'SP', 'RJ' se for no senado ou câmara dos deputados
        casa_legislativa -- objeto do tipo CasaLegislativa
        partido -- objeto do tipo Partido
        periodo -- objeto do tipo Periodo
    """

    def __init__(self):
        self.id = ''
        self.localidade  = ''
        self.casa_legislativa = None
        self.Partido = None
        self.periodo = None

    def __unicode__(self):
        return "%s" % self.periodo

    def __str__(self):
        return unicode(self).encode('utf-8')

class Periodo:
    """Intervalo de datas com um inicio e um fim"""

    def__init__(self):
        self.inicio = ''
        self.fim = ''

    def __unicode__(self):
        return "[%s,%s]" % (self.inicio, self.fim)

    def __str__(self):
        return unicode(self).encode('utf-8')

class CasaLegislativa:
    """Instituição tipo Senado, Câmara etc

    Atributos:
        id -- string identificadora da casa
        nome -- string; ex 'Câmara Municipal de São Paulo'
        esfera -- string (municipal, estadual, federal)
        local -- string; ex 'São Paulo' para a CMSP
        tamanhos -- lista de objetos do tipo HistoricoTamanho representando quantas cadeiras possui a casa
        composicao -- lista de objetos do tipo Composicao
    """

    def __init__(self):
        self.id = ''
        self.nome = ''
        self.esfera = ''
        self.local = ''
        self.tamanhos = []
        self.composicoes = []

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return unicode(self).encode('utf-8')


class Composicao:
    """Participação de um partido na casa"""

    def __init__(self):
        partido = None
        historico = []


class HistoricoTamanho:

    def __init__(self):
        tamanho = 0
        periodo = None


class VotosAgregados:
    """Um conjunto de votos.

    Atributos:
        sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto
    """

    def add(self, voto):
        """Adiciona um voto ao conjunto de votos.

        Argumentos:
            voto -- string \in {SIM, NAO, ABSTENCAO, AUSENTE, OBSTRUCAO}
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
        if (voto == AUSENTE):
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
    """Um conjunto de votos de um partido.

    Atributos:
        partido -- objeto do tipo Partido
        sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto
    """
    def __init__(self, partido):
        VotosAgregados.__init__(self)
        self.partido = partido

# TODO class VotoUF(VotosAgregados):


