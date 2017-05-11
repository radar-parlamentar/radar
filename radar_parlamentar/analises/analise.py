# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Saulo Trento, Diego Rabatone,
# Guilherme Januário
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


from math import hypot, atan2, pi
from .models import AnalisePeriodo, AnaliseTemporal
from modelagem import models
from modelagem import utils
from analises import filtro
import logging
import numpy
from . import pca
import copy
# import time # timetrack

logger = logging.getLogger("radar")


class AnalisadorTemporal:

    """O AnalisadorTemporal cria objetos do tipo AnaliseTemporal, o qual
    contém uma lista de objetos AnalisePeriodo.

    Uma análise de um período é uma análise de componentes principais dos
    votos de um dado período, por exemplo do ano de 2010. Para fazer um gráfico
    animado, é preciso fazer análises de dois ou mais períodos consecutivos,
    por exemplo 2010, 2011 e 2012, e rotacionar adequadamente os resultados
    para que os partidos globalmente caminhem o mínimo possível de um lado para
    o outro (vide algoritmo de rotação).

    A classe AnalisadorTemporal tem métodos para criar os objetos
    AnalisadorPeriodo e fazer as análises.

    Atributos:
        data_inicio e data_fim -- strings no formato 'aaaa-mm-dd'.
        analises_periodo -- lista de objetos da classe AnalisePeriodo
        palavras_chave -- lista de strings para serem utilizadas na filtragem
        de votações
        votacoes -- lista de objetos do tipo Votacao para serem usados
        na análise se não for especificado, procura votações na base de dados
        de acordo data_inicio, data_fim e palavras_chave.
    """

    def __init__(self, casa_legislativa, periodicidade,
                 palavras_chave=[], votacoes=[]):
        self.casa_legislativa = casa_legislativa
        recuperador_votacoes = utils.PeriodosRetriever(
            self.casa_legislativa, periodicidade)
        self.periodos = recuperador_votacoes.get_periodos()
        self.ini = self.periodos[0].ini
        self.fim = self.periodos[len(self.periodos) - 1].fim
        self.periodicidade = periodicidade
        self.analises_periodo = []
        self.palavras_chave = palavras_chave
        self.votacoes = []
        self.total_votacoes = 0
        self.json = ""
        self.chefes_executivos = []

    def get_analise_temporal(self):
        """Retorna instância de AnaliseTemporal"""
        if not self.analises_periodo:
            self._faz_analises()
        analise_temporal = AnaliseTemporal()
        analise_temporal.casa_legislativa = self.casa_legislativa
        analise_temporal.periodicidade = self.periodicidade
        analise_temporal.analises_periodo = self.analises_periodo
        analise_temporal.votacoes = self.votacoes
        analise_temporal.chefes_executivos = self.chefes_executivos
        analise_temporal.total_votacoes = self.total_votacoes
        analise_temporal.palavras_chaves = self.palavras_chave
        return analise_temporal

    def _faz_analises(self):
        """Método da classe AnalisadorTemporal que cria os objetos
        AnalisadorPeriodo e faz as análises."""

        for periodo in self.periodos:
            logger.info("Analisando periodo %s a %s." %
                        (str(periodo.ini), str(periodo.fim)))
            analisadorPeriodo = AnalisadorPeriodo(self.casa_legislativa,
                                                  periodo, self.votacoes,
                                                  self.palavras_chave)
            if analisadorPeriodo.votacoes:
                logger.info("O periodo possui %d votações." %
                            len(analisadorPeriodo.votacoes))
                analisePeriodo = analisadorPeriodo.analisa()
                self.analises_periodo.append(analisePeriodo)
                self.total_votacoes += len(analisadorPeriodo.votacoes)
            else:
                logger.info("O periodo não possui nenhuma votação.")

        # Rotaciona/espelha cada análise baseado em sua análise anterior
        logger.info("Rotacionando...")
        # a partir da segunda analise
        for i in range(1, len(self.analises_periodo)):
            rotacionador = Rotacionador(
                self.analises_periodo[i], self.analises_periodo[i - 1])
            analiseRotacionada = rotacionador.espelha_ou_roda()
            self.analises_periodo[i] = analiseRotacionada
        logger.info("Rotacionado")

    def votacoes_filtradas(self):
        votacoes_filtradas = []
        for periodo in self.periodos:
            analisadorPeriodo = AnalisadorPeriodo(self.casa_legislativa,
                                                  periodo, self.votacoes,
                                                  self.palavras_chave)
            votacoes_filtradas.extend(analisadorPeriodo._inicializa_votacoes())
        return votacoes_filtradas


class AnalisadorPeriodo:

    def __init__(self, casa_legislativa, periodo,
                 votacoes=[], palavras_chave=[]):
        """Argumentos:
            casa_legislativa -- objeto do tipo CasaLegislativa;
            somente votações desta casa serão analisados.
            periodo -- objeto do tipo PeriodoCasaLegislativa;
                       sem periodo, a análise é feita sobre todas as votações.
            votacoes -- lista de objetos do tipo Votacao para serem usados na
            análise se não for especificado, procura votações na base de dados
                        de acordo data_inicio, data_fim e palavras_chave.
            palavras_chave -- lista de strings para serem usadas na filtragem
            das votações
        """
        self.casa_legislativa = casa_legislativa
        self.periodo = periodo
        self.ini = periodo.ini if periodo is not None else None
        self.fim = periodo.fim if periodo is not None else None
        self.partidos = self.casa_legislativa.partidos()
        self.parlamentares = self.casa_legislativa.parlamentares()
        self.votacoes = votacoes
        self.palavras_chave = palavras_chave
        if not self.votacoes:
            self._inicializa_votacoes()

        self.num_votacoes = len(self.votacoes)
        self.analise_ja_feita = False  # quando a analise for feita, vale True.
        # em graus, eventual rotação feita por self.espelha_ou_roda()
        self.theta = 0

        # calculados por self._inicializa_vetores():
        self.vetores_votacao = []
        self.vetores_presencas = []
        self.tamanhos_partidos = {}
        self.coordenadas_partidos = {}

        # array de partido.nome's, um por parlamentar
        self.partido_do_parlamentar = []

        # parlamentar.id => {True,False},
        # sendo True se estava presente no periodo.
        self.presencas_parlamentares = {}

        # partido.nome => lista de parlamentares do partido
        # (independente de periodo).
        self.parlamentares_por_partido = {}

        self.pca_parlamentares = None
        self.coordenadas_parlamentares = {}

        #lista de chefes_executivos
        self.chefes_executivos = self._inicializa_chefes_executivo()

    def _inicializa_votacoes(self):
        """Pega votações deste período no banco de dados filtrando por palavras
        chave e seta a lista self.votacoes"""
        filtro_votacao = filtro.FiltroVotacao(
            self.casa_legislativa, self.periodo, self.palavras_chave)
        self.votacoes = filtro_votacao.filtra_votacoes()
        return self.votacoes

    def _inicializa_chefes_executivo(self):
        """Pega chefes executivo deste período no banco de dados filtrando pela casa 
        legislativa e seta a lista self.chefes_executivo"""
        filtro_chefe = filtro.FiltroChefesExecutivo(
            self.casa_legislativa, self.periodo)
        chefes_executivos = filtro_chefe.filtra_chefes_executivo()
        return chefes_executivos

    def analisa(self):
        """Retorna instância de AnalisePeriodo"""
        self._calcula_parlamentares_2d()
        self._analisa_partidos()
        analisePeriodo = AnalisePeriodo()
        analisePeriodo.casa_legislativa = self.casa_legislativa
        analisePeriodo.periodo = self.periodo
        analisePeriodo.partidos = self.partidos
        analisePeriodo.votacoes = self.votacoes
        analisePeriodo.num_votacoes = self.num_votacoes
        analisePeriodo.pca = self.pca
        analisePeriodo.tamanhos_partidos = self.tamanhos_partidos
        analisePeriodo.coordenadas_parlamentares = self.coordenadas_parlamentares
        analisePeriodo.coordenadas_partidos = self.coordenadas_partidos
        analisePeriodo.parlamentares_por_partido = self.parlamentares_por_partido
        analisePeriodo.chefes_executivos = self.chefes_executivos
        return analisePeriodo

    def _inicializa_vetores(self):
        construtorMatrizes = ConstrutorDeMatrizesDeDados(
            self.votacoes, self.partidos, self.parlamentares)
        construtorMatrizes.gera_matrizes()
        self.vetores_votacao = construtorMatrizes.matriz_votacoes
        self.vetores_presencas = construtorMatrizes.matriz_presencas
        self.partido_do_parlamentar = construtorMatrizes.partido_do_parlamentar

    def _calcula_parlamentares_2d(self):
        """Retorna mapa com as coordenadas de parlamentares no plano 2D formado
        pelas duas primeiras componentes principais.

        A chave do mapa é o id do parlamentar (int) e o valor é uma lista
        de duas posições [x,y].
        """
        if not self.analise_ja_feita:
            self.coordenadas_parlamentares = self._pca_parlamentares()
            if self.num_votacoes > 1:
                for partido in list(self.coordenadas_parlamentares.keys()):
                    self.coordenadas_parlamentares[partido] = (
                        self.coordenadas_parlamentares[partido])[0:2]
            # se só tem 1 votação, só tem 1 C.P. Jogar tudo zero na segunda CP.
            elif self.num_votacoes == 1:
                for partido in list(self.coordenadas_parlamentares.keys()):
                    self.coordenadas_parlamentares[partido] = numpy.array(
                        [(self.coordenadas_parlamentares[partido])[0], 0.])
            # Zero votações no período. Os partidos são todos iguais. Tudo
            # zero.
            else:
                for parlamentar in list(self.coordenadas_parlamentares.keys()):
                    self.coordenadas_parlamentares[
                        parlamentar] = numpy.array([0., 0.])
        return self.coordenadas_parlamentares

    def _pca_parlamentares(self):
        """Roda a análise de componentes principais por parlamentares.

        Retorna um dicionário no qual as chaves são os ids dos parlamentares
        e o valor de cada chave é um vetor com as n dimensões da análise pca
        """
        if not self.pca_parlamentares:
            if not self.vetores_votacao:
                self._inicializa_vetores()
            ids_parlamentares_presentes = self._listar_indices_de_parlamentares_presentes()
            matriz = self.vetores_votacao
            # exclui parlamentares ausentes em todas as votações do período
            matriz = matriz[ids_parlamentares_presentes, :]
            matriz = matriz - matriz.mean(axis=0)  # centraliza dados
            self.pca = pca.PCA(matriz, fraction=1)  # faz o pca
            self._preenche_pca_de_parlamentares_nulos(ids_parlamentares_presentes)
            logger.info("PCA terminada com sucesso. ini=%s, fim=%s" %
                        (str(self.ini), str(self.fim)))
        # Criar dicionario a ser retornado:
        dicionario = {}
        for parlamentar, vetor in zip(self.parlamentares, self.pca.U):
            dicionario[parlamentar.id] = vetor
        return dicionario

    def _listar_indices_de_parlamentares_presentes(self):
        return self.vetores_presencas.sum(axis=1).nonzero()[0].tolist()

    def _preenche_pca_de_parlamentares_nulos(self, ipnn):
        """Recupera parlamentares ausentes no período, atribuindo NaN em todas
        as dimensões no espaço das componentes principais"""
        U2 = self.pca.U.copy()  # Salvar resultado da pca em U2
        matriz_de_nans = numpy.zeros(
            (len(self.parlamentares), self.num_votacoes)) * numpy.nan
        self.pca.U = matriz_de_nans
        ip = -1
        ipnn2 = -1
        for p in self.parlamentares:
            ip += 1
            if ip in ipnn:  # Se este parlamentar for não nulo
                ipnn2 += 1
                cpmaximo = U2.shape[1]
                # colocar nesta linha os valores que eu salvei antes em U2
                self.pca.U[ip, 0:cpmaximo] = U2[ipnn2, :]
                # aproveitar para preencher presencas_parlamentares
                # (parlamentar.id => True / False)
                self.presencas_parlamentares[p.id] = True
            else:
                self.pca.U[ip, :] = numpy.zeros(
                    (1, self.num_votacoes)) * numpy.NaN
                self.presencas_parlamentares[p.id] = False

    def _analisa_partidos(self):
        coordenadas_parlamentares = self.pca.U[:, 0:2]
        if coordenadas_parlamentares.shape[1] == 1:
            coordenadas_parlamentares = numpy.append(
                coordenadas_parlamentares, numpy.zeros(
                    [len(coordenadas_parlamentares), 1]), 1)
        analisador_partidos = AnalisadorPartidos(
            coordenadas_parlamentares, self.parlamentares, self.partidos,
            self.vetores_presencas, self.partido_do_parlamentar)
        analisador_partidos.analisa_partidos()
        self.coordenadas_partidos = analisador_partidos.coordenadas_partidos
        self.tamanhos_partidos = analisador_partidos.tamanhos_partidos
        self.parlamentares_por_partido = \
            analisador_partidos.parlamentares_por_partido


class ConstrutorDeMatrizesDeDados:

    def __init__(self, votacoes, partidos, parlamentares):
        self.votacoes = votacoes
        self.partidos = partidos
        self.parlamentares = parlamentares
        self.matriz_votacoes = numpy.zeros(
            (len(self.parlamentares), len(self.votacoes)))
        self.matriz_presencas = numpy.zeros(
            (len(self.parlamentares), len(self.votacoes)))
        # array de partido.nome's, um por parlamentar
        self.partido_do_parlamentar = []
        # chave eh nome do partido, e valor eh VotoPartido
        self._dic_partido_votos = {}
        self._dic_parlamentares_votos = {}  # parlamentar.id => voto.opcao

    def gera_matrizes(self):
        """Cria duas matrizes:
            matriz_votacoes -- de votações (por parlamentares),
            matriz_presencas -- presenças de parlamentares

        Os valores possíveis na matriz de votações são:
        -1 (não), 0 (abtencão/falta) e 1 (sim).
        Os valores possíveis na matriz de presenças são:
        0 (falta) e 1 (presente).
        As linhas indexam parlamentares. As colunas indexam as votações.
        A ordenação das linhas segue a ordem de self.partidos ou
        self.parlamentares, e a ordenação das colunas segue a ordem
        de self.votacoes.

        Retorna matriz_votacoes
        """
        iv = -1  # índice votação
        for votacao in self.votacoes:
            iv += 1
            self._construtor_dicionario_parlamentares_votos(votacao)
            self._preenche_matrizes(votacao, iv)
        return self.matriz_votacoes

    def _construtor_dicionario_parlamentares_votos(self, votacao):
        # com o "select_related" fazemos uma query eager
        votos = votacao.voto_set.select_related(
            'opcao', 'parlamentar__id').all()
        for voto in votos:
            self._dic_parlamentares_votos[voto.parlamentar.id] = voto.opcao

    def _preenche_matrizes(self, votacao, iv):
        ip = -1  # indice parlamentares
        for parlamentar in self.parlamentares:
            ip += 1
            self.partido_do_parlamentar.append(parlamentar.partido.nome)
            if parlamentar.id in self._dic_parlamentares_votos:
                opcao = self._dic_parlamentares_votos[parlamentar.id]
                self.matriz_votacoes[ip][iv] = self._converter_opcao_para_valor(opcao)
                if (opcao == models.AUSENTE):
                    self.matriz_presencas[ip][iv] = 0.
                else:
                    self.matriz_presencas[ip][iv] = 1.
            else:
                self.matriz_votacoes[ip][iv] = 0.
                self.matriz_presencas[ip][iv] = 0.

    def _converter_opcao_para_valor(self, opcao):
        if opcao == 'SIM':
            return 1.
        if opcao == 'NAO':
            return -1.
        return 0.


class AnalisadorPartidos:

    """Analisa um partido em um período"""

    def __init__(self, coordenadas_parlamentares, parlamentares, partidos,
                 matriz_presencas, partido_do_parlamentar):
        self.coordenadas_parlamentares = coordenadas_parlamentares
        self.parlamentares = parlamentares
        self.partidos = partidos
        self.matriz_presencas = matriz_presencas
        self.partido_do_parlamentar = partido_do_parlamentar
        self.coordenadas_partidos = {}
        self.tamanhos_partidos = {}
        self.parlamentares_por_partido = {}

    def analisa_partidos(self):
        """Gera as seguintes saídas:
            self.coordenadas_partido # partido => [x,y]
            self.tamanhos_partidos # partido => int
            self.parlamentares_por_partido # partido => parlamentares
        """
        for ip in range(0, len(self.partidos)):
            indices_deste_partido = []
            for il in range(0, len(self.parlamentares)):
                if self.partido_do_parlamentar[il] == self.partidos[ip].nome:
                    indices_deste_partido.append(il)
            coordenadas_medias = self._media_sem_nans(
                self.coordenadas_parlamentares[indices_deste_partido, :])
            tamanho_partido = len(self.matriz_presencas[
                                  indices_deste_partido, :].sum(
                                  axis=1).nonzero()[0])
            self.tamanhos_partidos[self.partidos[ip]] = tamanho_partido
            self.parlamentares_por_partido[self.partidos[ip].nome] = [
                self.parlamentares[x] for x in indices_deste_partido]
            self.coordenadas_partidos[self.partidos[ip]] = coordenadas_medias

    def _media_sem_nans(self, array_numpy):
        """ Retorna média por colunas de uma array numpy,
        desconsiderando os nans."""
        mdat = numpy.ma.masked_array(array_numpy, numpy.isnan(array_numpy))
        mm = numpy.mean(mdat, axis=0)
        return mm.filled(numpy.nan)

class Rotacionador:

    def __init__(self, analisePeriodo, analisePeriodoReferencia):
        self.analisePeriodo = analisePeriodo
        self.analisePeriodoReferencia = analisePeriodoReferencia

    def _espelhar_coordenadas(self, lista_coordenadas):
        for indice, coords in list(lista_coordenadas.items()):
            lista_coordenadas[indice] = numpy.dot(
                coords, numpy.array([[-1., 0.], [0., 1.]]))

    def _rotacionar_coordenadas(self, theta, lista_coordenadas):
        for indice, coords in list(lista_coordenadas.items()):
            lista_coordenadas[indice] = numpy.dot(
            coords, self._gerar_matriz_rotacao(theta))

    def _energia(self, dados_fixos, dados_meus, por_partido,
                 graus=0, espelho=0):
        """Calcula energia envolvida no movimento entre dois instantes
        (fixo e meu), onde o meu é rodado (entre 0 e 360 graus),
        e primeiro eixo multiplicado por -1 se espelho=1.
        Ver pdf intitulado "Solução Analítica para o Problema de
        Rotação dos Eixos de Representação dos Partidos no Radar
        Parlamentar" (algoritmo_rotacao.pdf)."""
        e = 0
        dados_meus = dados_meus.copy()
        if espelho == 1:
            self._espelhar_coordenadas(dados_meus)
        if graus != 0:
            for partido, coords in list(dados_meus.items()):
                dados_meus[partido] = numpy.dot(coords, self._gerar_matriz_rotacao(graus))

        if por_partido:
            for p in dados_meus:
                e += self._retornar_zero_se_nan(
                    numpy.dot(dados_fixos[p] - dados_meus[p],
                              dados_fixos[p] - dados_meus[p]) *
                    self.analisePeriodo.tamanhos_partidos[p])
        else:
            for l in dados_meus:
                e += self._retornar_zero_se_nan(
                    numpy.dot(dados_fixos[l] - dados_meus[
                        l], dados_fixos[l] - dados_meus[l]))
        return e

    def _polar(self, x, y, deg=0):		# radian if deg=0; degree if deg=1
        """
        Convert from rectangular (x,y) to polar (r,w)
        r = sqrt(x^2 + y^2)
        w = arctan(y/x) = [-\pi,\pi] = [-180,180]
        """
        if deg:
            return hypot(x, y), 180.0 * atan2(y, x) / pi
        else:
            return hypot(x, y), atan2(y, x)

    def _gerar_matriz_rotacao(self, graus):
        """ Retorna matriz de rotação 2x2 que roda os eixos em graus (0 a 360)
        no sentido anti-horário (como se os pontos girassem no sentido
        horário em torno de eixos fixos)."""
        graus = float(graus)
        rad = numpy.pi * graus / 180.
        c = numpy.cos(rad)
        s = numpy.sin(rad)
        return numpy.array([[c, -s], [s, c]])

    def _retornar_zero_se_nan(self, x):
        """Retorna zero sempre que x não for um número (NaN = Not a Number)
        Caso x seja um número, retorna x."""
        if numpy.isnan(x):
            return 0
        else:
            return x

    def espelha_ou_roda(self, por_partido=False, so_espelha=True):
        """Retorna nova AnalisePeriodo com coordenadas rotacionadas
        se por_partido == True:
        a operacao minimiza o quanto os partidos caminharam
        se por_partido == False:
        minimiza o quanto os parlamentares em si caminham
        se so_espelha == True:
        nao se faz rotacao, apenas espelha as componentes se necessario.
        """
        if por_partido:
            dados_meus = self.analisePeriodo.coordenadas_partidos
            dados_fixos = self.analisePeriodoReferencia.coordenadas_partidos
        else:
            dados_meus = self.analisePeriodo.coordenadas_parlamentares
            dados_fixos = \
                self.analisePeriodoReferencia.coordenadas_parlamentares
        epsilon = 0.001

        if not so_espelha:
            logger.info("Calculando ângulo teta 1 e ângulo teta 2...")
            numerador = 0
            denominador = 0
            for indice, coords in list(dados_meus.items()):
                meu_polar = self._polar(coords[0], coords[1], 0)
                alheio_polar = self._polar(
                    dados_fixos[indice][0], dados_fixos[indice][1], 0)
                tamanho = self.analisePeriodo.tamanhos_partidos[
                    indice] if por_partido else 1
                numerador += self._retornar_zero_se_nan(
                    tamanho * meu_polar[0] * alheio_polar[0] * numpy.sin(
                        alheio_polar[1]))
                denominador += self._retornar_zero_se_nan(
                    tamanho * meu_polar[0] * alheio_polar[0] * numpy.cos(
                        alheio_polar[1]))
            if denominador < epsilon and denominador > -epsilon:
                angulo_teta1 = 90
                angulo_teta2 = 270
            else:
                angulo_teta1 = numpy.arctan(numerador / denominador) * 180 / 3.141592
                angulo_teta2 = angulo_teta1 + 180
            logger.info("angulo_teta 1 = " + str(angulo_teta1) + "; angulo_teta2 = " + str(angulo_teta2))
        else:
            angulo_teta1 = 0
            angulo_teta2 = 180

        ex = numpy.array([self._energia(dados_fixos, dados_meus, por_partido,
                          graus=angulo_teta1, espelho=0),
                          self._energia(dados_fixos, dados_meus, por_partido,
                          graus=angulo_teta2, espelho=0),
                          self._energia(dados_fixos, dados_meus, por_partido,
                          graus=angulo_teta1, espelho=1),
                          self._energia(dados_fixos, dados_meus, por_partido,
                          graus=angulo_teta2, espelho=1)])
        logger.info(ex)

        dados_partidos = self.analisePeriodo.coordenadas_partidos
        dados_parlamentares = self.analisePeriodo.coordenadas_parlamentares
        ganhou = ex.argmin()
        campeao = [0, 0]
        if ganhou >= 2:  # espelhar
            campeao[0] = 1
            self._espelhar_coordenadas(dados_partidos)
            self._espelhar_coordenadas(dados_parlamentares)
        if ganhou == 0 or ganhou == 2:  # girar de angulo_te1
            campeao[1] = angulo_teta1
        else:
            campeao[1] = angulo_teta2
        self._rotacionar_coordenadas(campeao[1], dados_partidos)
        self._rotacionar_coordenadas(campeao[1], dados_parlamentares)

        self.theta = campeao[1]
        logger.info("campeao = [espelha,theta] = " + str(campeao))

        analiseRotacionada = copy.copy(self.analisePeriodo)
        analiseRotacionada.coordenadas_partidos = dados_partidos
        analiseRotacionada.coordenadas_parlamentares = dados_parlamentares

        return analiseRotacionada
