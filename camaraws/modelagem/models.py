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

OPCOES = (
    ('SIM', 'Sim'),
    ('NAO', 'Não'),
    ('ABSTENCAO', 'Abstenção'),
    ('OBSTRUCAO', 'Obstrução'),
    ('AUSENTE', 'Ausente'),
)

GENEROS = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)

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
    """

    nome = models.CharField(max_length=10)
    numero = models.IntegerField()

    def __unicode__(self):
        return self.nome


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
        esfera -- string (municipal, estadual, federal)
        local -- string; ex 'São Paulo' para a CMSP
        tamanhos -- lista de objetos do tipo HistoricoTamanho representando quantas cadeiras possui a casa
        composicao -- lista de objetos do tipo Composicao
    """

    nome = models.CharField(max_length=100)
    esfera = models.CharField(max_length=10, choices=ESFERAS)
    local = models.CharField(max_length=100)
    tamanhos = models.ManyToManyField(HistoricoTamanho, null=True)
    composicoes = models.ManyToManyField(Composicao, null=True)

    def __unicode__(self):
        return self.nome


class Legislatura(models.Model):
    """O mandato exercido por um parlamentar.

    Atributos:
        localidade -- string; ex 'SP', 'RJ' se for no senado ou câmara dos deputados
        casa_legislativa -- objeto do tipo CasaLegislativa
        partido -- objeto do tipo Partido
        inicio, fim -- datas indicando o período
    """

    localidade = models.CharField(max_length=100, blank=True)
    casa_legislativa = models.ForeignKey(CasaLegislativa, null=True)
    partido = models.ForeignKey(Partido)
    inicio = models.DateField(null=True)
    fim = models.DateField(null=True)

    def __unicode__(self):
        return "%s" % self.periodo


class Parlamentar(models.Model):
    """Um parlamentar.

    Atributos:
        id_parlamentar - string identificadora de acordo a fonte de dados
        nome, genero -- strings
        legislatura -- lista de objetos do tipo Legislatura
        partido -- pode-se guardar o partido atual aqui também (objeto do tipo Partido)

    Métodos:
        partido_atual()
        legislatura_atual()
    """

    id_parlamentar = models.CharField(max_length=100, blank=True) # obs: não é chave primária! 
    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=10, choices=GENEROS, blank=True)
    legislaturas = models.ManyToManyField(Legislatura, null=True)
    partido = models.ForeignKey(Partido, null=True) # para facilitar o uso, pelo menos por hora

    def partido_atual(self):
        """Retorna partido atual do parlamentar.

        Retorno: objeto do tipo Partido
        """
        return self.legislatura_atual().partido

    def legislatura_atual(self):
        """Retorna legislatura atual do parlamentar.

        Retorno: objeto do tipo Legislatura
        """
        if self.legislaturas:
            return self.legislaturas[-1] # TODO: se lista é vazia, o if tá caindo nessa linha!
        else:
            return None

    def __unicode__(self):
        return "%s (%s)" % (self.nome, self.partido) # TODO: pegar partido da legislatura mais nova, se houver


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
        parlamentar -- objeto do tipo Parlamentar
        opcao -- qual foi o voto do parlamentar (sim, não, abstenção, obstrução, não votou)
    """

    parlamentar = models.ForeignKey(Parlamentar)
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


