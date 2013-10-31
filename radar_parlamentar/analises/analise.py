# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Saulo Trento, Diego Rabatone, Guilherme Januário
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

"""Módulo analise"""

from __future__ import unicode_literals
from math import hypot, atan2, pi
from models import AnalisePeriodo, AnaliseTemporal
from modelagem import models
import grafico
import logging
import numpy
import pca
import json
import copy
#import time # timetrack

logger = logging.getLogger("radar")

class AnalisadorTemporal:
    """Um objeto da classe AnalisadorTemporal é um envelope para um conjunto de
    objetos do tipo AnalisadorPeriodo.

    Uma análise de um período é uma análise de componentes principais dos
    votos de um dado período, por exemplo do ano de 2010. Para fazer um gráfico
    animado, é preciso fazer análises de dois ou mais períodos consecutivos, 
    por exemplo 2010, 2011 e 2012, e rotacionar adequadamente os resultados 
    para que os partidos globalmente caminhem o mínimo possível de um lado para
    o outro (vide algoritmo de rotação).

    A classe AnalisadorTemporal tem métodos para criar os objetos AnalisadorPeriodo e
    fazer as análises.

    Atributos:
        data_inicio e data_fim -- strings no formato 'aaaa-mm-dd'.
        analises_periodo -- lista de objetos da classe AnalisePeriodo
    """
    def __init__(self, casa_legislativa, periodicidade=models.BIENIO, votacoes=[]):
        self.casa_legislativa = casa_legislativa
        self.periodos = self.casa_legislativa.periodos(periodicidade)
        self.ini = self.periodos[0].ini
        self.fim = self.periodos[len(self.periodos)-1].fim
        self.periodicidade = periodicidade
        self.area_total = 1
        self.analises_periodo = [] 
        self.votacoes = []
        self.json = ""

    def get_json(self):
        self._faz_analises()
        self._cria_json(constante_escala_tamanho = 50)
        return self.json

    def get_analise_temporal(self):
        """Retorna instância de AnaliseTemporal"""
        if not self.analises_periodo:
            self._faz_analises()
        analise_temporal = AnaliseTemporal()
        analise_temporal.casa_legislativa = self.casa_legislativa
        analise_temporal.periodicidade = self.periodicidade
        analise_temporal.area_total = self.area_total
        analise_temporal.analises_periodo = self.analises_periodo
        analise_temporal.votacoes = self.votacoes
        return analise_temporal
            
    def _faz_analises(self):
        """Método da classe AnalisadorTemporal que cria os objetos AnalisadorPeriodo e faz as análises."""
        for periodo in self.periodos:
            logger.info("Analisando periodo %s a %s." % (str(periodo.ini),str(periodo.fim)) )
            analisadorPeriodo = AnalisadorPeriodo(self.casa_legislativa, periodo, self.votacoes)
            if analisadorPeriodo.votacoes:
                logger.info("O periodo possui %d votações." % len(analisadorPeriodo.votacoes))
                analisePeriodo = analisadorPeriodo.analisa()
                self.analises_periodo.append(analisePeriodo)
            else:
                logger.info("O periodo não possui nenhuma votação.")

        # Rotaciona/espelha cada análise baseado em sua análise anterior
        for i in range(1,len(self.analises_periodo)): # a partir da segunda analise
            rotacionador = Rotacionador(self.analises_periodo[i], self.analises_periodo[i-1])
            analiseRotacionada = rotacionador.espelha_ou_roda()
            self.analises_periodo[i] = analiseRotacionada 
        
        # determina área máxima:
        maior_soma_dos_tamanhos_dos_partidos = max([ analise.soma_dos_tamanhos_dos_partidos for analise in self.analises_periodo ])
        logger.info("maior soma dos tamanhos dos partidos = %f",maior_soma_dos_tamanhos_dos_partidos)
        self.area_total = maior_soma_dos_tamanhos_dos_partidos


class AnalisadorPeriodo:

    def __init__(self, casa_legislativa, periodo=None, votacoes=[]):
        """Argumentos:
            casa_legislativa -- objeto do tipo CasaLegislativa; somente votações desta casa serão analisados.
            periodo -- objeto do tipo PeriodoCasaLegislativa; 
                       sem periodo, a análise é feita sobre todas as votações.
            votacoes -- lista de objetos do tipo Votacao para serem usados na análise
                        se não for especificado, procura votações na base de dados de acordo data_inicio e data_fim.
        """
        self.casa_legislativa = casa_legislativa
        self.periodo = periodo
        self.ini = periodo.ini if periodo != None else None
        self.fim = periodo.fim if periodo != None else None
        self.partidos = self.casa_legislativa.partidos()
        self.legislaturas = self.casa_legislativa.legislaturas()
        self.votacoes = votacoes
        if not self.votacoes: 
            self._inicializa_votacoes()
        
        self.num_votacoes = len(self.votacoes)
        self.analise_ja_feita = False # quando a analise for feita, vale True.
        self.theta = 0 # em graus, eventual rotação feita por self.espelha_ou_roda()
        
        # calculados por self._inicializa_vetores():
        self.vetores_votacao_por_partido = []
        self.vetores_presenca_por_partido = []
        self.vetores_votacao = []
        self.tamanhos_partidos = {}
        self.presencas_partidos = {}
        self.soma_dos_tamanhos_dos_partidos = 0
        
        self.pca_partido = None # É calculado por self._pca_partido()
        self.coordenadas = {} # É o produto final da análise realizada por esta classe

    def _inicializa_votacoes(self):
        """Pega votações do banco de dados e seta a lista self.votacoes"""
        if self.ini == None and self.fim == None:
            self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=self.casa_legislativa) 
        if self.ini == None and self.fim != None:
            self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=self.casa_legislativa).filter(data__lte=self.fim)
        if self.ini != None and self.fim == None:
            self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=self.casa_legislativa).filter(data__gte=self.ini)
        if self.ini != None and self.fim != None:
            self.votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=self.casa_legislativa).filter(data__gte=self.ini, data__lte=self.fim)

    def _inicializa_vetores(self):
        matrizesBuilder = MatrizesDeDadosBuilder(self.votacoes, self.partidos, self.legislaturas)
        matrizesBuilder.gera_matrizes()
        self.vetores_votacao = matrizesBuilder.matriz_votacoes
        self.vetores_votacao_por_partido = matrizesBuilder.matriz_votacoes_por_partido
        self.vetores_presenca_por_partido = matrizesBuilder.matriz_presencas_por_partido
        tamanhosBuilder = TamanhoPartidoBuilder(self.partidos, self.casa_legislativa)
        self.tamanhos_partidos = tamanhosBuilder.gera_dic_tamanho_partidos()
        # Presencas dos partidos está quebrado:
        self.presencas_partidos = {}
        self.soma_dos_tamanhos_dos_partidos = tamanhosBuilder.soma_dos_tamanhos_dos_partidos 

    def _pca_partido(self):
        """Roda a análise de componentes principais por partido.

        Guarda o resultado em self.pca
        Retorna um dicionário no qual as chaves são as siglas dos partidos
        e o valor de cada chave é um vetor com as n dimensões da análise pca
        """
        if not self.pca_partido:
            if self.vetores_votacao_por_partido == None or len(self.vetores_votacao_por_partido) == 0:
                self._inicializa_vetores()
            ipnn = self._lista_de_indices_de_partidos_naos_nulos()
            matriz = self.vetores_votacao_por_partido
            matriz = matriz[ipnn,:] # exclui partidos de tamanho zero
            matriz = matriz - matriz.mean(axis=0) # centraliza dados
            self.pca_partido = pca.PCA(matriz,fraction=1) # faz o pca
            self._preenche_pca_de_partidos_nulos(ipnn)
            logger.info("PCA terminada com sucesso. ini=%s, fim=%s" % (str(self.ini),str(self.fim)))
        # Criar dicionario a ser retornado:
        dicionario = {}
        for partido, vetor in zip(self.partidos, self.pca_partido.U):
            dicionario[partido.nome] = vetor
        return dicionario
    
    def _lista_de_indices_de_partidos_naos_nulos(self):
        ipnn = [] 
        ip = -1
        for p in self.partidos:
            ip += 1
            if self.tamanhos_partidos[p.nome] != 0:
                ipnn.append(ip)
        return ipnn
    
    def _preenche_pca_de_partidos_nulos(self, ipnn):
        """Recupera partidos de tamanho nulo, atribuindo zero em todas as dimensões no espaço das componentes principais"""
        U2 = self.pca_partido.U.copy() # Salvar resultado da pca em U2
        self.pca_partido.U = numpy.zeros((len(self.partidos), self.num_votacoes))
        ip = -1
        ipnn2 = -1
        for p in self.partidos:
            ip += 1
            if ip in ipnn: # Se este partido for um partido não nulo
                ipnn2 += 1
                cpmaximo = U2.shape[1]
                # colocar nesta linha os valores que eu salvei antes em U2
                self.pca_partido.U[ip,0:cpmaximo] = U2[ipnn2,:]
            else:
                self.pca_partido.U[ip,:] = numpy.zeros((1,self.num_votacoes))
        

    def _calcula_partidos_2d(self):
        """Retorna mapa com as coordenadas dos partidos no plano 2D formado
        pelas duas primeiras componentes principais. Para isso é preciso
        fazer uma análise de componentes principais (pca); se esta já tiver
        sido feita, o método apenas retorna o resultado já previamente salvo
        na variável self.coordenadas. Caso contrário a análise é feita.

        A chave do mapa é o nome do partido (string) e o valor é uma lista 
        de duas posições [x,y].
        """
        if not self.analise_ja_feita: # A análise pca ainda tem que ser feita.
            self.coordenadas = self._pca_partido() # Fazer análise pca.
            if self.num_votacoes > 1:
                for partido in self.coordenadas.keys():
                    self.coordenadas[partido] = (self.coordenadas[partido])[0:2]
            elif self.num_votacoes == 1: # se só tem 1 votação, só tem 1 C.P. Jogar tudo zero na segunda CP.
                for partido in self.coordenadas.keys():
                    self.coordenadas[partido] = [(self.coordenadas[partido])[0], 0.]
            else: # Zero votações no período. Os partidos são todos iguais. Tudo zero.
                for partido in self.coordenadas.keys():
                    self.coordenadas[partido] = [ 0. , 0. ]
        return self.coordenadas
    
    def analisa(self):
        """Retorna AnalisePeriodo"""
        self._calcula_partidos_2d()
        analisePeriodo = AnalisePeriodo()
        analisePeriodo.casa_legislativa = self.casa_legislativa
        analisePeriodo.periodo = self.periodo
        analisePeriodo.partidos = self.partidos
        analisePeriodo.votacoes = self.votacoes
        analisePeriodo.num_votacoes = self.num_votacoes
        analisePeriodo.tamanhos_partidos = self.tamanhos_partidos
        analisePeriodo.presencas_partidos = self.presencas_partidos        
        analisePeriodo.soma_dos_tamanhos_dos_partidos = self.soma_dos_tamanhos_dos_partidos
        analisePeriodo.pca_partido = self.pca_partido
        analisePeriodo.coordenadas = self.coordenadas
        return analisePeriodo


# TODO testar matriz_votacoes
class MatrizesDeDadosBuilder:
    
    def __init__(self, votacoes, partidos, legislaturas):
        self.votacoes = votacoes
        self.partidos = partidos
        self.legislaturas = legislaturas
        self.matriz_votacoes =  numpy.zeros((len(self.legislaturas), len(self.votacoes)))
        self.matriz_presencas = numpy.zeros((len(self.legislaturas), len(self.votacoes)))
        self.matriz_votacoes_por_partido =  numpy.zeros((len(self.partidos), len(self.votacoes)))
        self.matriz_presencas_por_partido = numpy.zeros((len(self.partidos), len(self.votacoes)))
        self.partido_do_parlamentar = numpy.zeros((len(self.legislaturas), 1)) # lista de partidos, um por legislatura
        self._dic_partido_votos = {} # chave eh nome do partido, e valor eh VotoPartido
        self._dic_legislaturas_votos = {} # legislatura.id => voto.opcao

    def gera_matrizes(self):
        """Cria quatro matrizes: 
            matriz_votacoes -- de votações (por legislaturas), 
            matriz_presencas -- presenças de legislaturas
            matriz_votacoes_por_partido -- de votações agregadas por partido,
            matriz_presencas_por_partido -- presenças dos partidos.

        As matrizes de votações têm valores entre -1 e 1. Quando por deputado, os valores
        possíveis são -1, 0 e 1, e quando agregado por partido a faixa é contínua.
    
        As linhas indexam os partidos em matriz_votacoes_por_partido e matriz_presencas
        e indexam os legislaturas em matriz_votacoes. As colunas indexam as votações.
        A ordenação das linhas segue a ordem de self.partidos ou self.legislaturas,
        e a ordenação das colunas segue a ordem de self.votacoes.
        """
        iv = -1 # índice votação
        for votacao in self.votacoes:
            iv += 1
            self._agrega_votos(votacao)
            self._preenche_matriz_por_legislatura(votacao, iv)
            self._preenche_matrizes_por_partido(votacao, iv)
        return self.matriz_votacoes  
    
    def _agrega_votos(self, votacao):
        self._dic_partido_votos = {}
        for partido in self.partidos:
            self._dic_partido_votos[partido.nome] = models.VotoPartido(partido.nome)
        # com o "select_related" fazemos uma query eager
        votos = votacao.voto_set.select_related('legislatura__partido', 'opcao', 'legislatura__id').all() 
        
        for voto in votos:
            nome_partido = voto.legislatura.partido.nome
            voto_partido = self._dic_partido_votos[nome_partido]
            opcao = voto.opcao
            voto_partido.add(opcao) 
            self._dic_legislaturas_votos[voto.legislatura.id] = opcao
            
    def _preenche_matriz_por_legislatura(self, votacao, iv):
        il = -1 # indice legislatura
        for legislatura in self.legislaturas:
            il += 1
            if self._dic_legislaturas_votos.has_key(legislatura.id):
                opcao = self._dic_legislaturas_votos[legislatura.id]
                self.matriz_votacoes[il][iv] = self._opcao_to_double(opcao)
                if (opcao == models.AUSENTE):
                    self.matriz_presencas[il][iv] = 0.
                else:
                    self.matriz_presencas[il][iv] = 1.
            else:
                self.matriz_votacoes[il][iv] = 0.
                self.matriz_presencas[il][iv] = 0.

    def _preenche_matrizes_por_partido(self, votacao, iv):
        ip = -1 # índice partido 
        for partido in self.partidos:
            ip += 1
            if self._dic_partido_votos.has_key(partido.nome):
                voto_partido = self._dic_partido_votos[partido.nome] 
                self.matriz_votacoes_por_partido[ip][iv] = voto_partido.voto_medio() 
                self.matriz_presencas_por_partido[ip][iv] = voto_partido.total()
            else:
                self.matriz_votacoes_por_partido[ip][iv] = 0.
                self.matriz_presencas_por_partido[ip][iv] = 0.

    def _opcao_to_double(self, opcao):
        if opcao == 'SIM':
            return 1.
        if opcao == 'NAO':
            return -1.
        return 0.

class TamanhoPartidoBuilder:
    
    def __init__(self, partidos, casa_legislativa):
        self.partidos = partidos
        self.casa_legislativa = casa_legislativa
        self.tamanhos = {} # nome partido => tamanho
        self.soma_dos_tamanhos_dos_partidos = 0
        
    def gera_dic_tamanho_partidos(self):
        for partido in self.partidos:
            tamanho = models.Legislatura.objects.filter(casa_legislativa=self.casa_legislativa, partido=partido).count() 
            self.tamanhos[partido.nome] = tamanho
        self._calcula_soma_dos_tamanhos()
        return self.tamanhos
    
    def _calcula_soma_dos_tamanhos(self):
        """Calcula um valor proporcional à soma das áreas dos partidos, para usar 
        no fator de escala de exibição do gráfico de bolhas
        """
        self.soma_dos_tamanhos_dos_partidos = sum(self.tamanhos.values())

    
    
class Rotacionador:
    
    def __init__(self, analisePeriodo, analisePeriodoReferencia):
        self.analisePeriodo = analisePeriodo
        self.analisePeriodoReferencia = analisePeriodoReferencia
    
    def _energia(self,dados_fixos,dados_meus,graus=0,espelho=0):
        """Calcula energia envolvida no movimento entre dois instantes (fixo e meu), onde o meu é rodado (entre 0 e 360 graus), e primeiro eixo multiplicado por -1 se espelho=1. Ver pdf intitulado "Solução Analítica para o Problema de Rotação dos Eixos de Representação dos Partidos no Radar Parlamentar" (algoritmo_rotacao.pdf)."""
        e = 0
        dados_meus = dados_meus.copy()
        if espelho == 1:
            for partido, coords in dados_meus.items():
                dados_meus[partido] = numpy.dot( coords,numpy.array( [[-1.,0.],[0.,1.]] ) )
        if graus != 0:
            for partido, coords in dados_meus.items():
                dados_meus[partido] = numpy.dot( coords,self._matrot(graus) )

        for p in self.analisePeriodo.partidos:
            e += numpy.dot( dados_fixos[p.nome] - dados_meus[p.nome],  dados_fixos[p.nome] - dados_meus[p.nome] ) * self.analisePeriodo.tamanhos_partidos[p.nome]
        return e

    def _polar(self,x, y, deg=0):		# radian if deg=0; degree if deg=1
        """
        Convert from rectangular (x,y) to polar (r,w)
        r = sqrt(x^2 + y^2)
        w = arctan(y/x) = [-\pi,\pi] = [-180,180]
        """
        if deg:
            return hypot(x, y), 180.0 * atan2(y, x) / pi
        else:
            return hypot(x, y), atan2(y, x)
    
    def _matrot(self,graus):
        """ Retorna matriz de rotação 2x2 que roda os eixos em graus (0 a 360) no sentido anti-horário (como se os pontos girassem no sentido horário em torno de eixos fixos)."""
        graus = float(graus)
        rad = numpy.pi * graus/180.
        c = numpy.cos(rad)
        s = numpy.sin(rad)
        return numpy.array([[c,-s],[s,c]])

    def espelha_ou_roda(self):
        """Retorna nova AnalisePeriodo com coordenadas rotacionadas"""
        epsilon = 0.001
        dados_meus = self.analisePeriodo.coordenadas
        dados_fixos = self.analisePeriodoReferencia.coordenadas

        numerador = 0;
        denominador = 0;
        for partido, coords in dados_meus.items():
            meu_polar = self._polar(coords[0],coords[1],0)
            alheio_polar = self._polar(dados_fixos[partido][0],dados_fixos[partido][1],0)
            numerador += self.analisePeriodo.tamanhos_partidos[partido] * meu_polar[0] * alheio_polar[0] * numpy.sin(alheio_polar[1])
            denominador += self.analisePeriodo.tamanhos_partidos[partido] * meu_polar[0] * alheio_polar[0] * numpy.cos(alheio_polar[1])
        if denominador < epsilon and denominador > -epsilon:
            teta1 = 90
            teta2 = 270
        else:
            teta1 = numpy.arctan(numerador/denominador) * 180 / 3.141592
            teta2 = teta1 + 180

        ex = numpy.array([self._energia(dados_fixos,dados_meus,graus=teta1,espelho=0),self._energia(dados_fixos,dados_meus,graus=teta2,espelho=0),self._energia(dados_fixos,dados_meus,graus=teta1,espelho=1), self._energia(dados_fixos,dados_meus,graus=teta2,espelho=1) ])
        print ex
        
        ganhou = ex.argmin()
        campeao = [0,0]
        if ganhou >= 2: # espelhar
            campeao[0] = 1
            for partido, coords in dados_meus.items():
                dados_meus[partido] = numpy.dot( coords, numpy.array([[-1.,0.],[0.,1.]]) )
        if ganhou == 0 or ganhou == 2: # girar de teta1
            campeao[1] = teta1
        else:
            campeao[1] = teta2
        for partido, coords in dados_meus.items():
            dados_meus[partido] = numpy.dot( coords, self._matrot(campeao[1]) )

        self.coordenadas = dados_meus; # altera coordenadas originais da instância.
        self.theta = campeao[1]
        
        analiseRotacionada = copy.copy(self.analisePeriodo)
        analiseRotacionada.coordenadas = dados_meus
        return analiseRotacionada








