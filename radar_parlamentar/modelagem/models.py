
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Eduardo Hideo, Saulo Trento,
#                     Diego Rabatone
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


from django.db import models
from django.utils.dateparse import parse_datetime
import re
import logging
import os

logger = logging.getLogger("radar")
MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

SIM = 'SIM'
NAO = 'NAO'
ABSTENCAO = 'ABSTENCAO'
OBSTRUCAO = 'OBSTRUCAO'
AUSENTE = 'AUSENTE'

OPCOES = (
    (SIM, "Sim"),
    (NAO, "Não"),
    (ABSTENCAO, "Abstenção"),
    (OBSTRUCAO, "Obstrução"),
    (AUSENTE, "Ausente"),
)

M = "M"
F = "F"

GENEROS = (
    (M, "Masculino"),
    (F, "Feminino"),
)

MUNICIPAL = 'MUNICIPAL'
ESTADUAL = 'ESTADUAL'
FEDERAL = 'FEDERAL'

ESFERAS = (
    (MUNICIPAL, 'Municipal'),
    (ESTADUAL, 'Estadual'),
    (FEDERAL, 'Federal'),
)

QUADRIENIO = "QUADRIENIO"
BIENIO = 'BIENIO'
ANO = 'ANO'
SEMESTRE = 'SEMESTRE'
MES = 'MES'

PERIODOS = (
    (QUADRIENIO, 'QUADRIENIO'),
    (BIENIO, 'BIENIO'),
    (ANO, 'ano'),
    (SEMESTRE, 'semestre'),
    (MES, 'mes')
)

SEM_PARTIDO = 'Sem partido'
COR_PRETA = '#000000'


class Indexadores(models.Model):
    """Termos utilizados na indexação de proposições

    Atributos:
        termo -- string; ex: "mulher" ou "partido político"+
        principal -- bool; identifica se o termo é o principal
                    de uma linha de sinônimos, o termo a ser usado.
    """
    termo = models.CharField(max_length=120)
    principal = models.BooleanField()

    def __unicode__(self):
        return '%s-%s-%s' % (self.nome, self.numero, self.cor)


class Partido(models.Model):
    """Partido político.

    Atributos:
        nome -- string; ex: 'PT'
        numero -- int; ex: '13'
        cor -- string; ex: #FFFFFF

    Métodos da classe:
        from_nome(nome): retorna objeto do tipo Partido
        from_numero(numero): retorna objeto do tipo Partido
        get_sem_partido(): retorna um partido chamado 'SEM PARTIDO'
    """

    LISTA_PARTIDOS = os.path.join(MODULE_DIR, 'recursos/partidos.txt')

    nome = models.CharField(max_length=12)
    numero = models.IntegerField()
    cor = models.CharField(max_length=7)

    @classmethod
    def from_nome(cls, nome):
        """Recebe um nome e retornar um objeto do tipo Partido,
            ou None se nome for inválido
        """
        if nome is None:
            return None

        # procura primeiro no banco de dados
        nome = cls._normaliza_nome_partido(nome)
        p = Partido.objects.filter(nome__iexact=nome)
        if p:
            return p[0]
        else:
            # se não estiver no BD, procura hardcoded
            return cls._from_regex(1, nome.strip())

    @classmethod
    def _normaliza_nome_partido(cls, nome_partido):
        trocar = {'DEMOCRATAS': 'DEM', 'SOLIDARIED': 'SD', 'SDD': 'SD'}
        nome_partido = nome_partido.upper().replace(' ', '')
        nome_partido = trocar.get(nome_partido, nome_partido)
        return nome_partido

    @classmethod
    def from_numero(cls, numero):
        """Recebe um número (int) e retornar um objeto do tipo Partido,
            ou None se nome for inválido
        """

        if numero is None:
            return None

        # procura primeiro no banco de dados
        p = Partido.objects.filter(numero=numero)
        if p:
            return p[0]
        else:
            # se não estiver no BD, procura no arquivo hardcoded
            return cls._from_regex(2, str(numero))

    @classmethod
    def get_sem_partido(cls):
        """Retorna um partido chamado 'SEM PARTIDO'"""
        lista = Partido.objects.filter(nome=SEM_PARTIDO)
        if not lista:
            partido = Partido()
            partido.nome = SEM_PARTIDO
            partido.numero = 0
            partido.cor = COR_PRETA
            partido.save()
        else:
            partido = lista[0]
        return partido

    @classmethod
    def _from_regex(cls, idx, key):
        PARTIDO_REGEX = '([a-zA-Z]*); *([0-9]{2}); *(#+[0-f]{6})'
        f = open(cls.LISTA_PARTIDOS)
        for line in f:
            res = re.search(PARTIDO_REGEX, line)
            if res and res.group(idx).upper() == key:
                partido = Partido()
                partido.nome = res.group(1)
                partido.numero = int(res.group(2))
                partido.cor = res.group(3)
                partido.save()
                return partido
        return None

    def __unicode__(self):
        return '%s-%s' % (self.nome, self.numero)


class CasaLegislativa(models.Model):
    """Instituição tipo Senado, Câmara etc

    Atributos:
        nome -- string; ex 'Câmara Municipal de São Paulo'
        nome_curto -- string; será usado pra gerar links.
                        ex 'cmsp' para 'Câmara Municipal de São Paulo'
        esfera -- string (municipal, estadual, federal)
        local -- string; ex 'São Paulo' para a CMSP
    """

    nome = models.CharField(max_length=100)
    nome_curto = models.CharField(max_length=50, unique=True)
    esfera = models.CharField(max_length=10, choices=ESFERAS)
    local = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome

    def partidos(self):
        """Retorna os partidos existentes nesta casa legislativa"""
        return Partido.objects.filter(
            parlamentar__casa_legislativa=self).distinct()

    def parlamentares(self):
        """Retorna os parlamentares existentes nesta casa legislativa"""
        return Parlamentar.objects.filter(casa_legislativa=self).distinct()

    def num_votacao(self, data_inicial=None, data_final=None):
        """retorna a quantidade de votacao numa casa legislativa"""
        return Votacao.por_casa_legislativa(
            self, data_inicial, data_final).count()

    def num_votos(self, data_inicio=None, data_fim=None):
        """retorna a quantidade de votos numa casa legislativa"""
        votacoes = Votacao.por_casa_legislativa(self, data_inicio, data_fim)
        votos = []
        for votacao in votacoes:
            votos += votacao.votos()
        return len(votos)

    @staticmethod
    def deleta_casa(nome_casa_curto):
        """Método que deleta determinado registro de casa legislativa
            em cascata
            Argumentos:
                nome_casa - Nome da casa a ser deletada"""
        try:
            try:
                CasaLegislativa.objects.get(
                    nome_curto=nome_casa_curto).delete()

            except CasaLegislativa.DoesNotExist:
                logger.info(
                    'Casa legislativa ' + nome_casa_curto + ' não existe')
        except:
            logger.info('Possivelmente a operacao extrapolou o limite de '
                        'operacoes do SQLite, tente utilizar o MySQL')


class ChefeExecutivo(models.Model):
    """Atributos:
        nome -- string; ex Lula
        genero -- string: ex Masculino
        partido -- tipo Partido
        mandato_ano_inicio -- objetos datetime
        mandato_ano_fim -- objetos datetime
    """

    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=10, choices=GENEROS, blank=True)
    partido = models.ForeignKey(Partido)
    mandato_ano_inicio = models.IntegerField()
    mandato_ano_fim = models.IntegerField()
    casas_legislativas = models.ManyToManyField(CasaLegislativa)
    titulo = None
    
    def __unicode__(self):
        self.titulo = self.get_titulo_chefe()
        return self.titulo + ": " + self.nome + " - " + self.partido.nome

    @staticmethod
    def por_casa_legislativa_e_periodo(casa_legislativa,
                             data_inicial=None,
                             data_final=None):
        
        chefes_executivo = ChefeExecutivo.objects.filter(
            casas_legislativas__nome_curto=casa_legislativa.nome_curto)
        
        chefes = []
        if data_inicial is not None and data_final is not None:
            ano_inicio = int(data_inicial.year)
            ano_fim = int(data_final.year)
            if(ano_inicio == ano_fim):
                chefes = ChefeExecutivo.get_chefe_anual(ano_inicio, chefes_executivo)
            else:
                chefes = ChefeExecutivo.get_chefe_periodo(ano_inicio, ano_fim, chefes_executivo)
        else:
            chefes = chefes_executivo

        return chefes
    
    @staticmethod
    def get_chefe_anual(ano, chefes_executivo):
        chefes = []
        for chefe in chefes_executivo:
            ano_valido = chefe.mandato_ano_inicio <= ano and chefe.mandato_ano_fim >= ano
            if(ano_valido):
                chefes.append(chefe)

        return chefes

    @staticmethod
    def get_chefe_periodo(ano_inicio, ano_fim, chefes_executivo):
        chefes = []
        for chefe in chefes_executivo:
            ano_inicio_valido =  ano_inicio >= chefe.mandato_ano_inicio and ano_inicio <= chefe.mandato_ano_fim   
            ano_fim_valido =  ano_fim >= chefe.mandato_ano_inicio and ano_fim <= chefe.mandato_ano_fim
            mandato_ano_inicio_valido = chefe.mandato_ano_inicio >= ano_inicio and chefe.mandato_ano_inicio <= ano_fim
            mandato_ano_fim_valido = chefe.mandato_ano_fim >= ano_inicio and chefe.mandato_ano_fim <= ano_fim
            if(ano_inicio_valido or ano_fim_valido or mandato_ano_inicio_valido or mandato_ano_fim_valido):
                chefes.append(chefe)

        return chefes

    def get_titulo_chefe(self):
        titulo = ""
        casas_legislativas = self.casas_legislativas.all()
        for casa in casas_legislativas:
            esfera = casa.esfera  
            genero_masculino = self.genero == M
            if(esfera == FEDERAL):
                if(genero_masculino):
                    titulo = "Presidente"
                else:
                    titulo = "Presidenta"
            elif(esfera == MUNICIPAL):
                if(genero_masculino):
                    titulo = "Prefeito"
                else:
                    titulo = "Prefeita"
        return titulo                


class PeriodoCasaLegislativa(object):
    """Atributos:
        ini, fim -- objetos datetime
        string -- Descrição do período
        quantidade_votacoes -- inteiro
    """

    def __init__(self, data_inicio, data_fim, quantidade_votacoes=0):
        # TODO self.casa_legislativa = ...
        self.ini = data_inicio
        self.fim = data_fim
        self.quantidade_votacoes = quantidade_votacoes
        self.string = ""
        self.string = str(self)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        if not self.string:
            self._build_string()
        return self.string

    def _build_string(self):
        data_string = ''
#       data_string = str(self.ini.year) # sempre começa com o ano
        delta = self.fim - self.ini
        if delta.days < 35:  # período é de um mês
            meses = ['',
                     'Jan',
                     'Fev',
                     'Mar',
                     'Abr',
                     'Maio',
                     'Jun',
                     'Jul',
                     'Ago',
                     'Set',
                     'Out',
                     'Nov',
                     'Dez']
            data_string += str(self.ini.year)
            data_string += " " + str(meses[self.ini.month])
        elif delta.days < 200:  # periodo é de um semestre
            data_string += str(self.ini.year)
            if self.ini.month < 6:
                data_string += " 1o Semestre"
            else:
                data_string += " 2o Semestre"
        elif delta.days < 370:  # periodo é de um ano
            data_string += str(self.ini.year)
        elif delta.days < 750:  # periodo é um biênio
            data_string += str(self.ini.year) + " e "
            data_string += str(self.fim.year)
        elif delta.days < 1500:  # periodo é um quadriênio
            data_string += str(self.ini.year) + " a "
            data_string += str(self.fim.year)
        self.string = data_string


class Parlamentar(models.Model):
    """Um parlamentar em uma determinada situação.
    Se o cidadão troca de partido, de casa legislativa ou de localidade,
    passa a ser um novo Parlamentar.

    Atributos:
        id_parlamentar --
                    string identificadora de acordo a fonte de dados
                    (i.e., pode se repetir entre diferentes casa legislativas)
        nome, genero -- strings
        casa_legislativa -- tipo CasaLegislativa
        partido -- tipo Partido
        localidade -- string, ex: RJ (usado apenas para parlamentares federais)
    """
    id_parlamentar = models.CharField(max_length=100, blank=True)
    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=10, choices=GENEROS, blank=True)
    casa_legislativa = models.ForeignKey(CasaLegislativa, null=True)
    partido = models.ForeignKey(Partido)
    localidade = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.nome, self.partido.nome)


class Proposicao(models.Model):
    """Proposição parlamentar (proposta de lei).

    Atributos:
        id_prop - string identificadora de acordo a fonte de dados
        sigla, numero, ano -- strings que formam o nome legal da proposição
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
    # obs: id_prop não é chave primária!
    id_prop = models.CharField(max_length=100, blank=True)
    sigla = models.CharField(max_length=10)
    numero = models.CharField(max_length=10)
    ano = models.CharField(max_length=4)
    ementa = models.TextField(blank=True)
    descricao = models.TextField(blank=True)
    indexacao = models.TextField(blank=True)
    data_apresentacao = models.DateField(null=True)
    situacao = models.TextField(blank=True)
    casa_legislativa = models.ForeignKey(CasaLegislativa, null=True)
    autor_principal = models.TextField(blank=True)
    # TODO
    # autor_principal = models.ForeignKey(
    #    Parlamentar,
    #    null=True,
    #    related_name='Autor principal')
    autores = models.ManyToManyField(
        Parlamentar,
        null=True,
        related_name='demais_autores')

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
        resultado -- string
        proposicao -- objeto do tipo Proposicao

    Métodos:
        votos()
        por_partido()
    """
    # obs: id_vot não é chave primária!
    id_vot = models.CharField(max_length=100, blank=True)
    descricao = models.TextField(blank=True)
    data = models.DateField(blank=True, null=True)
    resultado = models.TextField(blank=True)
    proposicao = models.ForeignKey(Proposicao, null=True)

    def votos(self):
        """Retorna os votos da votação (depende do banco de dados)"""
        return self.voto_set.all()

    def por_partido(self):
        """Retorna votos agregados por partido.

        Retorno: um dicionário cuja chave é o nome do partido (string)
        e o valor é um VotoPartido
        """
        dic = {}
        for voto in self.votos():
            part = voto.parlamentar.partido.nome
            if part not in dic:
                dic[part] = VotoPartido(part)
            voto_partido = dic[part]
            voto_partido.add(voto.opcao)
        return dic

    @staticmethod
    def por_casa_legislativa(casa_legislativa,
                             data_inicial=None,
                             data_final=None):
        votacoes = Votacao.objects.filter(
            proposicao__casa_legislativa=casa_legislativa)
        from django.utils.dateparse import parse_datetime
        if data_inicial is not None:
            ini = parse_datetime('%s 0:0:0' % data_inicial)
            votacoes = votacoes.filter(data__gte=ini)
        if data_final is not None:
            fim = parse_datetime('%s 0:0:0' % data_final)
            votacoes = votacoes.filter(data__lte=fim)
        return votacoes

    # TODO def por_uf(self):

    def __unicode__(self):
        if self.data:
            return "[%s] %s" % (self.data, self.descricao)
        else:
            return self.descricao


class Voto(models.Model):
    """Um voto dado por um parlamentar em uma votação.

    Atributos:
        parlamentar -- objeto do tipo Parlamentar
        opcao -- qual foi o voto do parlamentar
                (sim, não, abstenção, obstrução, não votou)
    """

    votacao = models.ForeignKey(Votacao)
    parlamentar = models.ForeignKey(Parlamentar)
    opcao = models.CharField(max_length=10, choices=OPCOES)

    def __unicode__(self):
        return "%s votou %s" % (self.parlamentar, self.opcao)


class VotosAgregados:
    """Um conjunto de votos.

    Atributos:
        sim, nao, abstencao --
            inteiros que representam a quantidade de votos no conjunto

    Método:
        add
        total
        voto_medio
    """

    def __init__(self):
        self.sim = 0
        self.nao = 0
        self.abstencao = 0

    def add(self, voto):
        """Adiciona um voto ao conjunto de votos.

        Argumentos:
            voto -- string \in {SIM, NAO, ABSTENCAO, AUSENTE, OBSTRUCAO}
            OBSTRUCAO conta como um voto ABSTENCAO
            AUSENTE não conta como um voto
        """
        if voto == SIM:
            self.sim += 1
        if voto == NAO:
            self.nao += 1
        if voto == ABSTENCAO:
            self.abstencao += 1
        if voto == OBSTRUCAO:
            self.abstencao += 1
        # if (voto == AUSENTE):
        #    self.abstencao += 1

    def total(self):
        return self.sim + self.nao + self.abstencao

    def voto_medio(self):
        """Valor real que representa a 'opnião média' dos
            votos agregados; 1 representa sim e -1 representa não."""
        total = self.total()
        if total > 0:
            return 1.0 * (self.sim - self.nao) / self.total()
        else:
            return 0

    def __unicode__(self):
        return '(%s, %s, %s)' % (self.sim, self.nao, self.abstencao)

    def __str__(self):
        return str(self).encode('utf-8')


class VotoPartido(VotosAgregados):
    """Um conjunto de votos de um partido.

    Atributos:
        partido -- objeto do tipo Partido
        sim, nao, abstencao --
            inteiros que representam a quantidade de votos no conjunto
    """
    def __init__(self, partido):
        VotosAgregados.__init__(self)
        self.partido = partido
