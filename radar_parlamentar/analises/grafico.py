# !/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Saulo Trento, Diego Rabatone
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
# TemasTest
# You should have received a copy of the GNU General Public License
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.

"""Módulo gráfico
Responsável por cuidar das coisas relacionadas à apresentação do PCA para
o usuário final, dado que os cálculos do PCA já foram realizados
"""

from __future__ import unicode_literals
import json
import logging
from math import sqrt, isnan
from django import db  # para debugar numero de queries, usando
                        # db.reset_queries() e print len(db.connection.queries)
import time

logger = logging.getLogger("radar")


class JsonAnaliseGenerator:

    def __init__(self, analise_temporal):
        self.CONSTANTE_ESCALA_TAMANHO = 120
        self.analise_temporal = analise_temporal
        self.escala_periodo = None
        self.json = None
        self.max_parlamentar_radius_calculator = MaxRadiusCalculator()
        self.max_partido_radius_calculator = MaxRadiusCalculator()
        self.parlamentaresScaler = GraphScaler()
        self.partidosScaler = GraphScaler()
        self._init_raio_calculator()

    def _init_raio_calculator(self):
        tamanhos_dos_partidos_por_periodo = {}
        for ap in self.analise_temporal.analises_periodo:
            label_periodo = str(ap.periodo)
            tamanhos_dos_partidos_por_periodo[
                label_periodo] = ap.tamanhos_partidos
        self.raio_partido_calculator = RaioPartidoCalculator(
            tamanhos_dos_partidos_por_periodo)

    def get_json(self):
        if not self.json:
            logger.info('Gerando json...')
            self._cria_json()
            logger.info('json gerado')
        return self.json

    def _cria_json(self):
        dict_analise = {}
        dict_analise['geral'] = self._dict_geral()
        dict_analise['periodos'] = self._list_periodos()
        dict_analise['partidos'] = self._list_partidos_instrumented()
        dict_analise[
            'max_raio'] = self.max_parlamentar_radius_calculator.max_r()
        dict_analise[
            'max_raio_partidos'] = self.max_partido_radius_calculator.max_r()
        self.json = json.dumps(dict_analise)

    def _dict_geral(self):
        dict_geral = {}
        dict_geral['escala_tamanho'] = None
        dict_geral['filtro_votacoes'] = None
        dict_geral['CasaLegislativa'] = self._dict_casa_legislativa()
        dict_geral['total_votacoes'] = self.analise_temporal.total_votacoes
        dict_geral['palavras_chaves'] = self.analise_temporal.palavras_chaves
        return dict_geral

    def _dict_casa_legislativa(self):
        casa_legislativa = self.analise_temporal.casa_legislativa
        dict_casa = {}
        dict_casa['nome'] = casa_legislativa.nome
        dict_casa['nome_curto'] = casa_legislativa.nome_curto
        dict_casa['esfera'] = casa_legislativa.esfera
        dict_casa['local'] = casa_legislativa.local
        dict_casa['atualizacao'] = unicode(casa_legislativa.atualizacao)
        return dict_casa

    def _list_periodos(self):
        list_aps = []
        for ap in self.analise_temporal.analises_periodo:
            dict_ap = {}
            eigen0 = ap.pca.eigen[0] if len(
                ap.pca.eigen) > 0 is not None else 0
            eigen1 = ap.pca.eigen[1] if len(
                ap.pca.eigen) > 1 is not None else 0
            var_explicada = round(
                (eigen0 + eigen1) / ap.pca.eigen.sum() * 100, 1)
            dict_ap['nvotacoes'] = ap.num_votacoes
            dict_ap['nome'] = ap.periodo.string
            dict_ap['var_explicada'] = var_explicada
            dict_ap['cp1'] = self._dict_cp1(ap)
            dict_ap['cp2'] = self._dict_cp2(ap)
            dict_ap['votacoes'] = self._list_votacoes_do_periodo(ap)
            list_aps.append(dict_ap)
        return list_aps

    def _dict_cp1(self, ap):
        return self._dict_cp(ap, 0)

    def _dict_cp2(self, ap):
        return self._dict_cp(ap, 1)

    def _dict_cp(self, ap, idx):
        """ap -- AnalisePeriodo; idx == 0 para cp1 and idx == 1 para cp2"""
        dict_cp = {}
        try:
            theta = round(ap.theta, 0) % 180 + 90 * idx
        except AttributeError, error:
            logger.error("AttributeError: %s" % error)
            theta = 0
        try:
            var_explicada = round(
                ap.pca.eigen[idx] / ap.pca.eigen.sum() * 100, 1)
            if ap.pca.Vt is not None:
                composicao = [round(el, 2)
                              for el in 100 * ap.pca.Vt[idx, :] ** 2]
                dict_cp['composicao'] = composicao
        except IndexError:
            var_explicada = 0
            dict_cp['composicao'] = 0
        dict_cp['theta'] = theta
        dict_cp['var_explicada'] = var_explicada
        # TODO estas contas complexas já deveriam ter sido feitas pela análise
        # o JsonGenerator não deveria entender dessas cosias.
        return dict_cp

    def _list_votacoes_do_periodo(self, ap):
        list_votacoes = []
        for votacao in ap.votacoes:
            dict_votacao = {}
            dict_votacao['id'] = unicode(votacao).replace('"', "'")
            list_votacoes.append(dict_votacao)
        return list_votacoes

    def _list_partidos_instrumented(self):
        db.reset_queries()
        print 'comecando lista de partidos'
        ttotal1 = time.time()
        list_partidos = self._list_partidos()
        print 'queries para fazer lista de partidos = '
        print str(len(db.connection.queries))
        print 'tempo na lista de partidos = '
        print str(time.time() - ttotal1) + ' s.'
        return list_partidos

    def _list_partidos(self):
        list_partidos = []
        partidos = self.analise_temporal.casa_legislativa.partidos(
        ).select_related('nome', 'numero', 'cor')
        #  self.analise_temporal.analises_periodo[0].partidos:
        for partido in partidos:
            list_partidos.append(self._dict_partido(partido))
        return list_partidos

    def _dict_partido(self, partido):
        dict_partido = {
            "nome": partido.nome, "numero": partido.numero, "cor": partido.cor}
        dict_partido["t"] = []
        dict_partido["r"] = []
        dict_partido["x"] = []
        dict_partido["y"] = []
        for ap in self.analise_temporal.analises_periodo:
            label_periodo = str(ap.periodo)
            cache_coords_key = label_periodo
            coordenadas = self.partidosScaler.scale(
                ap.coordenadas_partidos, cache_coords_key)
            try:
                x = round(coordenadas[partido][0], 2)
                y = round(coordenadas[partido][1], 2)
                self.max_partido_radius_calculator.add_point(x, y)
                if not isnan(x):
                    dict_partido["x"].append(round(x, 2))
                    dict_partido["y"].append(round(y, 2))
                else:
                    dict_partido["x"].append(0.)
                    dict_partido["y"].append(0.)
            except KeyError, error:
                logger.error("KeyError: %s" % error)
                dict_partido["x"].append(0.)
                dict_partido["y"].append(0.)
            tamanho = ap.tamanhos_partidos[partido]
            dict_partido["t"].append(tamanho)
            raio = self.raio_partido_calculator.get_raio(
                partido, label_periodo)
            dict_partido["r"].append(raio)
        dict_partido["parlamentares"] = []
        #legislaturas = self.analise_temporal.analises_periodo[0].legislaturas_por_partido[partido.nome]
        legislaturas = self.analise_temporal.casa_legislativa.legislaturas().filter(
            partido=partido).select_related('id', 'localidade', 'partido__nome', 'parlamentar__nome')
        for leg in legislaturas:
            dict_partido["parlamentares"].append(self._dict_parlamentar(leg))
        return dict_partido

    def _dict_parlamentar(self, legislatura):
        leg_id = legislatura.id
        nome = legislatura.parlamentar.nome
        localidade = legislatura.localidade
        dict_parlamentar = {
            "nome": nome, "id": leg_id, "localidade": localidade}
        dict_parlamentar["x"] = []
        dict_parlamentar["y"] = []
        for ap in self.analise_temporal.analises_periodo:
            cache_coords_key = str(ap.periodo)
            coordenadas = self.parlamentaresScaler.scale(
                ap.coordenadas_legislaturas, cache_coords_key)
            if coordenadas.has_key(leg_id):
                x = coordenadas[leg_id][0]
                y = coordenadas[leg_id][1]
                self.max_parlamentar_radius_calculator.add_point(x, y)
                if not isnan(x):
                    x = round(x, 2)
                    y = round(y, 2)
                else:
                    x = None
                    y = None
                dict_parlamentar["x"].append(x)
                dict_parlamentar["y"].append(y)
            else:
                dict_parlamentar["x"].append(None)
                dict_parlamentar["y"].append(None)
        return dict_parlamentar


class MaxRadiusCalculator:

    def __init__(self):
        self.max_r2 = 0

    def add_point(self, x, y):
        if self._valid(x) and self._valid(y):
            r2 = x ** 2 + y ** 2
            self.max_r2 = max(self.max_r2, r2)

    def _valid(self, value):
        return value is not None and not isnan(value)

    def max_r(self):
        return round(sqrt(self.max_r2), 1)


class GraphScaler:

    def __init__(self):
        self.cache = {}

    def scale(self, coords, cache_key):
        """Changes X,Y scale from [-1,1] to [-100,100]
        coords -- key => [x, y]
        """
        if cache_key in self.cache.keys():
            return self.cache[cache_key]
        scaled = self._scale(coords)
        self.cache[cache_key] = scaled
        return scaled

    def _scale(self, coords):
        scaled = {}
        for key, coord in coords.items():
            x = coord[0]
            try:
                y = coord[1]
            except IndexError:
                y = 0
            if x < -1 or x > 1 or y < -1 or y > 1:
                raise ValueError("Value should be in [-1,1]")
            scaled[key] = [x * 100, y * 100]
        return scaled


class RaioPartidoCalculator():

    """Define o raio da circunferência do partido no gráfico"""

    def __init__(self, tamanhos_dos_partidos_por_periodo):
        """Argumento:
        tamanhos_dos_partidos_por_periodo:
            string_periodo => (partido => int)
        onde string_periodo é uma string que representa univocamente um período
        gerada com str(periodo), onde periodo é do tipo PeriodoCasaLegislativa
        """
        self.CONSTANTE_ESCALA_TAMANHO = 120
        self.tamanhos_dos_partidos_por_periodo = tamanhos_dos_partidos_por_periodo
        self._init_area_total()
        self.escala = self.CONSTANTE_ESCALA_TAMANHO ** 2. / \
            max(1, self.area_total)

    def _init_area_total(self):
        maior_soma = 0
        for tamanhos_partidos in self.tamanhos_dos_partidos_por_periodo.values():
            soma_dos_tamanhos_dos_partidos = sum(tamanhos_partidos.values())
            if soma_dos_tamanhos_dos_partidos > maior_soma:
                maior_soma = soma_dos_tamanhos_dos_partidos
        self.area_total = maior_soma

    def get_raio(self, partido, periodo_str):
        tamanhos_partidos = self.tamanhos_dos_partidos_por_periodo[periodo_str]
        tamanho = tamanhos_partidos[partido]
        raio = sqrt(tamanho * self.escala)
        return round(raio, 1)
