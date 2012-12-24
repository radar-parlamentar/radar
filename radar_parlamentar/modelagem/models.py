# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Eduardo Hideo
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

from __future__ import unicode_literals
from django.db import models
from calendar import monthrange
import re
import logging 
import os
import datetime

logger = logging.getLogger("radar")
MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

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
    (M, 'Masculino'),
    (F, 'Feminino'),
)

MUNICIPAL = 'MUNICIPAL'
ESTADUAL = 'ESTADUAL'
FEDERAL = 'FEDERAL'

ESFERAS = (
    (MUNICIPAL, 'Municipal'),
    (ESTADUAL, 'Estadual'),
    (FEDERAL, 'Federal'),
)

ANO = 'ANO'
SEMESTRE = 'SEMESTRE'
MES = 'MES'

PERIODOS = (
    (ANO, 'ano'),
    (SEMESTRE, 'semestre'),
    (MES, 'mes')
)

SEM_PARTIDO = 'Sem partido'

class Partido(models.Model):
    """Partido político.

    Atributos:
        nome -- string; ex: 'PT' 
        numero -- int; ex: '13'

    Métodos da classe:
        from_nome(nome): retorna objeto do tipo Partido
        from_numero(numero): retorna objeto do tipo Partido
        get_sem_partido(): retorna um partido chamado 'SEM PARTIDO'
        exists(): retorna True se já existe um partido com mesmo nome e número na base de dados, ou False caso contrário
    """

    LISTA_PARTIDOS = os.path.join(MODULE_DIR, 'recursos/partidos.txt')

    nome = models.CharField(max_length=10)
    numero = models.IntegerField()
    
    @classmethod
    def from_nome(cls, nome):
        """Recebe um nome e retornar um objeto do tipo Partido, ou None se nome for inválido"""
        p = Partido.objects.filter(nome=nome) # procura primeiro no banco de dados
        if p:
            return p[0]
        else: # se não estiver no BD, procura no arquivo que contém lista de partidos
            return cls._from_regex(1, nome.strip())

    @classmethod
    def from_numero(cls, numero):
        """Recebe um número (int) e retornar um objeto do tipo Partido, ou None se nome for inválido"""
        p = Partido.objects.filter(numero=numero) # procura primeiro no banco de dados
        if p:
            return p[0]
        else: # se não estiver no BD, procura no arquivo que contém lista de partidos
            return cls._from_regex(2, str(numero))

    @classmethod
    def get_sem_partido(cls):
        """Retorna um partido chamado 'SEM PARTIDO'"""
        lista = Partido.objects.filter(nome = SEM_PARTIDO)
        if not lista:
            partido = Partido()
            partido.nome = SEM_PARTIDO
            partido.numero = 0
            partido.save()
        else:
            partido = lista[0]
        return partido

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
    
class PeriodoVotacao():
    """Representa um período de tempo em uma casa legislativa
    Atributos:
        ini -- datetime
        fim -- datetime
        label -- string do tipo '2010', '2010 - 1o semestre', ou '2010 - Janeiro'
        casa_legislativa -- objeto do tipo CasaLegislativa
        num_votacoes -- quantidade (int) de votações no período
    """
    
    def __init__(self):
        self.ini = None
        self.fim = None
        self.label = ''
        self.casa_legislativa = None
        self.num_votacoes = 0

class CasaLegislativa(models.Model):
    """Instituição tipo Senado, Câmara etc

    Atributos:
        nome -- string; ex 'Câmara Municipal de São Paulo'
        nome_curto -- string; será usado pra gerar links. ex 'cmsp' para 'Câmara Municipal de São Paulo' 
        esfera -- string (municipal, estadual, federal)
        local -- string; ex 'São Paulo' para a CMSP
        atualizacao -- data em que a base de dados foi atualizada pea última vez com votações desta casa
    """

    nome = models.CharField(max_length=100)
    nome_curto = models.CharField(max_length=50, unique=True)
    esfera = models.CharField(max_length=10, choices=ESFERAS)
    local = models.CharField(max_length=100)
    atualizacao = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.nome

    def partidos(self):
        """Retorna os partidos existentes nesta casa legislativa"""
        return Partido.objects.filter(legislatura__casa_legislativa=self).distinct()

    def periodos(self, delta, minimo=0.0):
        """Retorna os períodos em que houve votações nesta casa legislativa.
         
        Argumentos:
            delta: aceita as constantes em models.PERIODOS (ANO, SEMESTRE, MES)
            minimo: valor entre 0 e 1 para filtrar (remover) períodos não significativos;
                    se período não tiver pelo menos (minimo*100)% da média dos votos por período,
                    período não é retornado. 
                    valor default é 0.
                    
        Retorna:
            Uma lista de objetos do tipo PeriodoCasaLegislativa. 
        """
        votacao_datas = [votacao.data for votacao in Votacao.objects.filter(proposicao__casa_legislativa=self)]
        delta_mes = CasaLegislativa._delta_para_numero(delta)
        ini = CasaLegislativa._intervalo_inicio(min(votacao_datas),delta)
        fim = CasaLegislativa._intervalo_fim(max(votacao_datas),delta)
        intervalos = CasaLegislativa._intervalo_periodo(ini,fim, delta_mes)
        CasaLegislativa._periodos_set_string(intervalos,delta)
        #filtro
        if minimo != 0.0:
            media = self._media_votos_por_periodo(intervalos)
            corte = media*minimo
            intervalos = self._filtro_media_periodo(intervalos,corte)
        return intervalos
    

    @staticmethod
    def _intervalo_to_string(intervalo,delta):
        data_string = ""
        meses = ['','Jan', 'Fev', 'Mar', 'Abr', 'Maio', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        data_string += str(intervalo.ini.year)
        if delta == MES:
            data_string +=" "+str(meses[intervalo.ini.month])
        return data_string

    @staticmethod
    def _periodos_set_string(periodos,delta):
        numero_semestre = 1
        for periodo in periodos:
            data_string = CasaLegislativa._intervalo_to_string(periodo,delta)
            if delta == SEMESTRE:
                data_string += " "+str(numero_semestre)+"o Semestre"
                numero_semestre +=1
            periodo.string = data_string

    @staticmethod
    def _intervalo_inicio(data_inicial,delta):
	dia_inicial = 1
	ano_inicial = data_inicial.year
	if delta == MES:
	    mes_inicial = data_inicial.month
	if delta in [SEMESTRE,ANO]:
	    mes_inicial = 1
	return datetime.date(ano_inicial,mes_inicial,dia_inicial) 
     
    @staticmethod
    def _intervalo_fim(data_fim,delta):
	ano_fim = data_fim.year
	if delta == MES:
	    mes_fim = data_fim.month
	if delta == SEMESTRE:
	    if data_fim.month <= 6:
		mes_fim = 6
	    else:
		mes_fim = 12
	if delta == ANO:
	    mes_fim = 12
	dia_fim = monthrange(ano_fim,mes_fim)[1]
	return datetime.date(ano_fim,mes_fim,dia_fim)

    def _votacoes(self,data_inicial=None,data_final=None): 
        votacoes = Votacao.objects.filter(proposicao__casa_legislativa=self)
        from django.utils.dateparse import parse_datetime
        if data_inicial != None:
            ini = parse_datetime('%s 0:0:0' % data_inicial)
            votacoes =  votacoes.filter(data__gte=ini)
        if data_final != None:
            fim = parse_datetime('%s 0:0:0' % data_final)
            votacoes = votacoes.filter(data__lte=fim)
        return votacoes
    
    def num_votacao(self,data_inicial=None,data_final=None): 
        return self._votacoes(data_inicial,data_final).count()

    @staticmethod
    def _delta_para_numero(delta=SEMESTRE):
        delta_numero = {ANO:11,MES:0,SEMESTRE:5}
        valor = delta_numero[delta]
        return valor
 
    @staticmethod
    def _intervalo_periodo(ini,fim,delta_mes):
        intervalos = []
        data_inicial = ini
        dias_que_faltam = 1
        while dias_que_faltam > 0:
            mes = data_inicial.month
            ano = data_inicial.year
            mes = mes + delta_mes
            while mes > 12:
                mes = mes - 12
                ano = ano + 1
            data_final = data_inicial.replace(month=mes,year=ano)
            # ir ate ultimo dia do mes:
            dia_final = monthrange(data_final.year,data_final.month)[1]
            data_final = data_final.replace(day=dia_final)
            intervalos.append(PeriodoCasaLegislativa(data_inicial,data_final))
            data_inicial = data_final + datetime.timedelta(days=1)
            delta_que_falta = fim - data_final
            dias_que_faltam = delta_que_falta.days
        return intervalos
    
    def _media_votos_por_periodo(self,periodo):
        num_periodo = len(periodo)
        votos = self._votos()
        return len(votos)/num_periodo

    def _votos(self,data_inicio=None,data_fim=None):
        votacoes = self._votacoes(data_inicio,data_fim)
        votos = []
        for votacao in votacoes:
            votos+=votacao.votos()
        return votos

    def _filtro_media_periodo(self,periodos,media):
        periodo_filtrado = []
        for periodo in periodos:
            votos_periodo = len(self._votos(periodo.ini,periodo.fim))
            if votos_periodo >= media:
                periodo_filtrado.append(periodo)
        return periodo_filtrado

class PeriodoCasaLegislativa(object):
    
    def __init__(self,data_inicio,data_fim):
        self.ini = data_inicio
        self.fim = data_fim
        self.string = ""

    def __unicode__(self):
        return self.string

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
        return self.nome 


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
        return "%s - %s@%s [%s, %s]" % (self.parlamentar, self.partido, self.casa_legislativa.nome_curto, self.inicio, self.fim)


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


class Votacao(models.Model):
    """Votação em planário.
    
    Atributos:
        id_vot - string identificadora de acordo a fonte de dados
        descricao, resultado -- strings
        data -- data da votação (tipo date)
        proposicao -- objeto do tipo Proposicao

    Métodos:
        votos() 
        por_partido()
    """

    id_vot = models.CharField(max_length=100, blank=True) # obs: não é chave primária!
    descricao = models.TextField(blank=True)
    data = models.DateField(blank=True, null=True)
    resultado = models.TextField(blank=True)
    proposicao = models.ForeignKey(Proposicao, null=True)
    
    def votos(self):
        """Retorna os votos da votação (depende do banco de dados)"""
        return self.voto_set.all()

    def por_partido(self):
        """Retorna votos agregados por partido.

        Retorno: um dicionário cuja chave é o nome do partido (string) e o valor é um VotoPartido
        """
        dic = {}
        for voto in self.votos():
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

class Voto(models.Model):
    """Um voto dado por um parlamentar em uma votação.

    Atributos:
        legislatura -- objeto do tipo Legislatura
        opcao -- qual foi o voto do parlamentar (sim, não, abstenção, obstrução, não votou)
    """

    votacao = models.ForeignKey(Votacao)
    legislatura = models.ForeignKey(Legislatura)
    opcao = models.CharField(max_length=10, choices=OPCOES)

    def __unicode__(self):
        return "%s votou %s" % (self.parlamentar, self.opcao)
    
class VotosAgregados:
    """Um conjunto de votos.

    Atributos:
        sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto

    Método:
        add
        total
    """

    sim = 0
    nao = 0
    abstencao = 0

    def add(self, voto):
        """Adiciona um voto ao conjunto de votos.

        Argumentos:
            voto -- string \in {SIM, NAO, ABSTENCAO, AUSENTE, OBSTRUCAO}
            OBSTRUCAO conta como um voto ABSTENCAO
            AUSENTE não conta como um voto
        """
        if (voto == SIM):
            self.sim += 1
        if (voto == NAO):
            self.nao += 1
        if (voto == ABSTENCAO):
            self.abstencao += 1
        if (voto == OBSTRUCAO):
            self.abstencao += 1
        #if (voto == AUSENTE):
        #    self.abstencao += 1

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


