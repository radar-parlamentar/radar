# coding=utf8

# Copyright (C) 2013, Leonardo Leite, Eduardo Hideo
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
from models import MUNICIPAL, ESTADUAL, FEDERAL, MES
from models import SEMESTRE, ANO, BIENIO, QUADRIENIO
from models import Votacao, PeriodoCasaLegislativa
import datetime


class MandatoLists:

    def get_mandatos(self, esfera, ini_date, end_date):
        """Retorna datas do início de cada mandato no período compreendido
            entre ini_date e end_date
            Argumentos:
                ini_date, end_date -- tipo date
            Retorno:
                lista do tipo date
            Obs: início de cada mandato é sempre em 1 de janeiro
        """
        if esfera == MUNICIPAL:
            return self._get_mandatos(ini_date, end_date, 2009)
        elif esfera in [ESTADUAL, FEDERAL]:
            return self._get_mandatos(ini_date, end_date, 2011)

    def _get_mandatos(self, ini_date, end_date, ano_inicio_de_algum_mandato):
        ANO_DE_REFERENCIA = ano_inicio_de_algum_mandato - \
            4 * 500  # suficientemente no passado
        defasagem = (abs(ANO_DE_REFERENCIA - ini_date.year)) % 4
        y = ini_date.year - defasagem
        mandatos = []
        while y <= end_date.year:
            date_ini_mandato = datetime.date(y, 1, 1)
            mandatos.append(date_ini_mandato)
            y += 4
        return mandatos


class PeriodosRetriever:

    """Recupera os períodos com um mínimo de votações de uma casa legislativa
        entre data_da_primeira_votacao e data_da_ultima_votacao
        Argumentos:
          casa_legislativa -- um objeto CasaLegislativa.
          periodicidade -- uma constante em PERIODOS (ex. ANO, SEMESTRE).
          data_da_primeira_votacao, data_da_ultima_votacao:
              objetos datetime. Se não especificados,
              utiliza todo o histórico da casa.
          numero_minimo_de_votacoes -- periodos com menos votações
          são excluídos da lista. Default é 1.
        Retorna:
            Uma lista de objetos do tipo PeriodoCasaLegislativa.
        Detalhes:
        1) Períodos anual, biênio e quadriênio sempre começam em 1 de janeiro.
            Período semestral começa em 1 de janeiro ou 1 de julho.
            Período bimestral começa no primeiro dia do mês inicial do período.
        2) O início do primeiro período sempre coincidi com um início
            de um mandato. Assim, é garantido que cada período esteja
            inteiramente dentro de um mandato. Mandatos municipais são grupos
            de 4 anos começando em 2009 + i*4, i \in Z
            Mandatos federais/estaduais são grupos de 4 anos começando
            em 2011 + i*4, i \in Z
            WARNING: Brazil dependent code!
    """

    def __init__(self, casa_legislativa, periodicidade,
                 data_da_primeira_votacao=None, data_da_ultima_votacao=None,
                 numero_minimo_de_votacoes=1):
        self.casa_legislativa = casa_legislativa
        self.periodicidade = periodicidade
        self.data_da_primeira_votacao = data_da_primeira_votacao
        self.data_da_ultima_votacao = data_da_ultima_votacao
        self.numero_minimo_de_votacoes = numero_minimo_de_votacoes

    def get_periodos(self):
        if (self.data_da_primeira_votacao is None):
            # TODO a query abaixo poderia usar um ORDER BY
            votacao_datas = [votacao.data for votacao in Votacao.objects.filter(
                proposicao__casa_legislativa=self.casa_legislativa)]
            if not votacao_datas:
                return []
            self.data_da_primeira_votacao = min(votacao_datas)
            self.data_da_ultima_votacao = max(votacao_datas)
        data_inicial = self._inicio_primeiro_periodo()
        periodos_candidatos = []
        while data_inicial < self.data_da_ultima_votacao:
            data_inicial_prox_periodo = self._data_inicio_prox_periodo(
                data_inicial)
            data_final = data_inicial_prox_periodo - datetime.timedelta(days=1)
            quantidade_votacoes = self.casa_legislativa.num_votacao(
                data_inicial, data_final)
            periodo = PeriodoCasaLegislativa(
                data_inicial, data_final, quantidade_votacoes)
            periodos_candidatos.append(periodo)
            data_inicial = data_inicial_prox_periodo
        periodos_aceitos = self._filtra_periodos_com_minimo_de_votos(
            periodos_candidatos)
        return periodos_aceitos

    def _filtra_periodos_com_minimo_de_votos(self, periodos_candidatos):
        return [p for p in periodos_candidatos
                if p.quantidade_votacoes >= self.numero_minimo_de_votacoes]

    def _inicio_primeiro_periodo(self):
        # TODO extrair e fazer teste de unidade só pra esse método
        # dia
        dia_inicial = 1
        # mês
        if self.periodicidade == MES:
            mes_inicial = self.data_da_primeira_votacao.month
        elif self.periodicidade in [ANO, BIENIO, QUADRIENIO]:
            mes_inicial = 1
        elif self.periodicidade == SEMESTRE:
            primeiro_de_julho = datetime.date(
                self.data_da_primeira_votacao.year, 7, 1)
            if (self.data_da_primeira_votacao < primeiro_de_julho):
                mes_inicial = 1
            else:
                mes_inicial = 7
        # ano
        mandatos_lists = MandatoLists()
        esfera = self.casa_legislativa.esfera
        mandatos = mandatos_lists.get_mandatos(
            esfera, self.data_da_primeira_votacao, self.data_da_ultima_votacao)
        i = 0
        while i < len(mandatos) and mandatos[i] < self.data_da_primeira_votacao:
            ano_inicial = mandatos[i].year
            i += 1
        inicio_primeiro_periodo = datetime.date(
            ano_inicial, mes_inicial, dia_inicial)
        return inicio_primeiro_periodo

    def _data_inicio_prox_periodo(self, data_inicio_periodo):
        # TODO tb extrair e fazer testes
        # dia
        dia_inicial = 1
        # mês
        if self.periodicidade == MES:
            mes_inicial = data_inicio_periodo.month + 1
            if mes_inicial == 13:
                mes_inicial = 1
        elif self.periodicidade in [ANO, BIENIO, QUADRIENIO]:
            mes_inicial = 1
        elif self.periodicidade == SEMESTRE:
            if data_inicio_periodo.month == 1:
                mes_inicial = 7
            elif data_inicio_periodo.month == 7:
                mes_inicial = 1
        # ano
        if self.periodicidade == MES:
            if data_inicio_periodo.month < 12:
                ano_inicial = data_inicio_periodo.year
            else:
                ano_inicial = data_inicio_periodo.year + 1
        elif self.periodicidade == SEMESTRE:
            if data_inicio_periodo.month < 7:
                ano_inicial = data_inicio_periodo.year
            else:
                ano_inicial = data_inicio_periodo.year + 1
        elif self.periodicidade == ANO:
            ano_inicial = data_inicio_periodo.year + 1
        elif self.periodicidade == BIENIO:
            ano_inicial = data_inicio_periodo.year + 2
        elif self.periodicidade == QUADRIENIO:
            ano_inicial = data_inicio_periodo.year + 4
        inicio_prox_periodo = datetime.date(
            ano_inicial, mes_inicial, dia_inicial)
        return inicio_prox_periodo


class StringUtils():

    @staticmethod
    def transforma_texto_em_lista_de_string(texto):
        lista_de_string = []
        if texto is not None and texto != "":
            lista_de_string = texto.split(", ")
        return lista_de_string
