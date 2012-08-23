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
import re

SIM = 'SIM'
NAO = 'NAO'
ABSTENCAO = 'ABSTENCAO'
OBSTRUCAO = 'OBSTRUCAO'
AUSENTE = 'AUSENTE'

OPCOES = (
    (SIM, 'Sim'),
    (NAO, 'Não'),
    (ABSTENCAO, 'Abstenção'),
    (OBSTRUCAO, 'Obstrução'),
    (AUSENTE, 'Ausente'),
)

M = 'M'
F = 'F'

GENEROS = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)

MUNICIPAL = 'MUNICIPAL'
ESTADUAL = 'ESTADUAL'
FEDERAL = 'FEDERAL'

ESFERAS = (
    ('MUNICIPAL', 'Municipal'),
    ('ESTADUAL', 'Estadual'),
    ('FEDERAL', 'Federal'),
)


class Partido(models.Model):
    """Partido político.

    Atributos:
        nome -- string; ex: 'PT' 
        numero -- string; ex: '13'

    Métodos da classe:
        partido_from_nome(nome): retorna objeto do tipo Partido
        partido_from_numero(numero): retorna objeto do tipo Partido
    """

    LISTA_PARTIDOS = 'modelagem/recursos/partidos.txt'

    nome = models.CharField(max_length=10)
    numero = models.IntegerField()

    @classmethod
    def from_nome(cls, nome):
        """Recebe um nome e retornar um objeto do tipo Partido, ou None se nome for inválido"""
        return cls._from_regex(1, nome.strip())

    @classmethod
    def from_numero(cls, numero):
        """Recebe um número (string) e retornar um objeto do tipo Partido, ou None se nome for inválido"""
        return cls._from_regex(2, numero.strip())

    @classmethod
    def _from_regex(cls, idx, key):
        PARTIDO_REGEX = '([a-zA-Z]*) *([0-9]*)'
        f = open(cls.LISTA_PARTIDOS)
        for line in f:
            res = re.search(PARTIDO_REGEX, line)
            if res and res.group(idx) == key:
                partido = Partido()
                partido.nome = res.group(1)
                partido.numero = int(res.group(2))
                return partido
        return None

    def __unicode__(self):
        return '%s-%s' % (self.nome, self.numero)


class HistoricoTamanho(models.Model):

    tamanho = models.IntegerField()
    inicio = models.DateField(blank=True)
    fim = models.DateField(blank=True)


class Composicao(models.Model):
    """Participação de um partido na casa"""

    partido = models.ForeignKey(Partido)
    historico = models.ManyToManyField(HistoricoTamanho)


class CasaLegislativa(models.Model):
    """Instituição tipo Senado, Câmara etc

    Atributos:
        nome -- string; ex 'Câmara Municipal de São Paulo'
        nome_curto -- string; será usado pra gerar links. ex 'cmsp' para 'Câmara Municipal de São Paulo' 
        esfera -- string (municipal, estadual, federal)
        local -- string; ex 'São Paulo' para a CMSP
        tamanhos -- lista de objetos do tipo HistoricoTamanho representando quantas cadeiras possui a casa
        composicao -- lista de objetos do tipo Composicao
    """

    nome = models.CharField(max_length=100)
    nome_curto = models.CharField(max_length=50, unique=True)
    esfera = models.CharField(max_length=10, choices=ESFERAS)
    local = models.CharField(max_length=100)
    tamanhos = models.ManyToManyField(HistoricoTamanho, null=True)
    composicoes = models.ManyToManyField(Composicao, null=True)

    def __unicode__(self):
        return self.nome

class Parlamentar(models.Model):
    """Um parlamentar.

    Atributos:
        id_parlamentar - string identificadora de acordo a fonte de dados
        nome, genero -- strings
    """

    id_parlamentar = models.CharField(max_length=100, blank=True) # obs: não é chave primária! 
    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=10, choices=GENEROS, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.nome, self.partido()) 


class Legislatura(models.Model):
    """Um período de tempo contínuo em que um político atua como parlamentar.
    É diferente de mandato. Um mandato dura 4 anos. Se o titular sai
    e o suplente assume, temos aí uma troca de legislatura.

    Atributos:
        parlamentar -- parlamentar exercendo a legislatura; objeto do tipo Parlamentar
        casa_legislativa -- objeto do tipo CasaLegislativa
        inicio, fim -- datas indicando o período
        partido -- objeto do tipo Partido
        localidade -- string; ex 'SP', 'RJ' se for no senado ou câmara dos deputados
    """

    parlamentar = models.ForeignKey(Parlamentar)
    casa_legislativa = models.ForeignKey(CasaLegislativa, null=True)
    inicio = models.DateField(null=True)
    fim = models.DateField(null=True)
    partido = models.ForeignKey(Partido)
    localidade = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return "%s@%s [%s, %s]" % (self.partido, self.casa_legislativa.nome_curto, self.inicio, self.fim)


class Proposicao(models.Model):
    """Proposição parlamentar (proposta de lei).
    
    Atributos:
        id_prop - string identificadora de acordo a fonte de dados
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

    id_prop = models.CharField(max_length=100, blank=True) # obs: não é chave primária!
    sigla = models.CharField(max_length=10)
    numero = models.CharField(max_length=10)
    ano = models.CharField(max_length=4)
    ementa = models.TextField(blank=True)
    descricao = models.TextField(blank=True)
    indexacao = models.TextField(blank=True)
    data_apresentacao = models.DateField(null=True)
    situacao = models.TextField(blank=True)
    casa_legislativa = models.ForeignKey(CasaLegislativa, null=True)
    autores = models.ManyToManyField(Parlamentar, null=True)

    def nome(self):
        return "%s %s/%s" % (self.sigla, self.numero, self.ano)

    def __unicode__(self):
        return "[%s] %s" % (self.nome(), self.ementa) 


class Voto(models.Model):
    """Um voto dado por um parlamentar em uma votação.

    Atributos:
        legislatura -- objeto do tipo Legislatura
        opcao -- qual foi o voto do parlamentar (sim, não, abstenção, obstrução, não votou)
    """

    legislatura = models.ForeignKey(Legislatura)
    opcao = models.CharField(max_length=10, choices=OPCOES)

    def __unicode__(self):
        return "%s votou %s" % (self.parlamentar, self.opcao)


class Votacao(models.Model):
    """Votação em planário.
    
    Atributos:
        id_vot - string identificadora de acordo a fonte de dados
        descricao, data, resultado -- strings
        casa_legislativa -- objeto do tipo CasaLegislativa
        proposicao -- objeto do tipo Proposicao
        votos -- lista de objetos do tipo Voto

    Métodos:
        por_partido()
    """

    id_vot = models.CharField(max_length=100, blank=True) # obs: não é chave primária!
    descricao = models.TextField(blank=True)
    data = models.DateField(blank=True, null=True)
    resultado = models.TextField(blank=True)
    casa_legislativa = models.ForeignKey(CasaLegislativa, null=True)
    proposicao = models.ForeignKey(Proposicao, null=True)
    votos = models.ManyToManyField(Voto, null=True) # votações simbólicas não tem votos
    # TODO Devia ser OneToMany, e não ManyToMany!

    def por_partido(self):
        """Retorna votos agregados por partido.

        Retorno: um dicionário cuja chave é o nome do partido (string) e o valor é um VotoPartido
        """
        dic = {}
        for voto in self.votos.all():
            # TODO poderia ser mais complexo: checar se a data da votação bate com o período da legislatura mais recente
            part = voto.legislatura.partido.nome
            if not dic.has_key(part):
                dic[part] = VotoPartido(part)
            voto_partido = dic[part]
            voto_partido.add(voto.opcao)
        return dic

    # TODO def por_uf(self):

    def __unicode__(self):
        if self.data:
            return "[%s] %s" % (self.data, self.descricao) 
        else:
            return self.descricao


class VotosAgregados:
    """Um conjunto de votos.

    Atributos:
        sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto
    """

    sim = 0
    nao = 0
    abstencao = 0

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

    def total(self):
        return self.sim + self.nao + self.abstencao

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
        self.partido = partido

# TODO class VotoUF(VotosAgregados):


