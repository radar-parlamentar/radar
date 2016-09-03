# coding=utf8

# Copyright (C) 2016, Saulo Trento
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


"""Módulo ordenacao.
Este módulo foi criado na hackaton sprinklr set/2016 para resolver a issue 331.
O mapa de parlamentares precisa de uma ordem dos parlamentares, 
agrupados por partido, para que os partidos fiquem coesosno mapa."""


from __future__ import unicode_literals
from modelagem.models import Parlamentar, Proposicao, Votacao, \
    PeriodoCasaLegislativa, Voto
from modelagem import utils
from modelagem.models import ANO, BIENIO, QUADRIENIO
from analises.analise import AnalisadorPeriodo
from datetime import datetime
from operator import itemgetter
#import logging

#logger = logging.getLogger("radar")

def ordem_dos_parlamentares(proposicao):
    """Recebe um objeto Proposicao, e retorna uma lista de 2-tuplas onde o primeiro
    elemento é uma votação e o segundo é uma lista de objetos Parlamentar.
    A lista conterá os parlamentares que possuem Voto na Votacao.
    A lista estará ordenada conforme o seguinte critério:
      1o. Por partido, sendo que a ordem dos partidos deverá vir da primeira
          componente principal de uma PCA feita sobre as votações da legislatura
          da votação mais recente da proposição.
      2o. Partidos iguais na PCA, ordenar pelo maior partido primeiro, na soma
          de todas as votações.
      3o. Ordem alfabética de partidos.
      4o. Parlamentar que votou mais primeiro.
      5o. Ordem alfabética de parlamentar.
    """
    retorno = []
    votacs = Votacao.objects.filter(proposicao=proposicao).order_by('data')
    casa = proposicao.casa_legislativa
    datas_votacoes = [votac.data for votac in votacs]
    pr = utils.PeriodosRetriever(casa_legislativa = casa,
                                 periodicidade = QUADRIENIO,
                                 data_da_primeira_votacao = min(datas_votacoes),
                                 data_da_ultima_votacao = max(datas_votacoes),
                                 numero_minimo_de_votacoes = 1 )
    periodo = pr.get_periodos()[-1] # usar o ultimo periodo, mais recente.
    # primeiro criterio sao partidos:
    lista_ordenada_partidos = ordenar_partidos(casa, periodo)
    # segundo criterio foi quem votou mais, ou seja, nao se absteve/faltou:
    dicionario_votantes = ordenar_votantes(proposicao) # parlamtr -> (partido,int (qtas votou))

    for votacao in votacs:
        retorno.append((votacao,ordem_dos_parl_por_votacao(votacao,
                                                           dicionario_votantes,
                                                           lista_ordenada_partidos)))
    return retorno

def ordem_dos_parl_por_votacao(votacao, dicionario_votantes, lista_ordenada_partidos):
    """recebe uma votacao e lista ja ordenada de partidos,
    e retorna a lista dos parlamentares desta votacao,
    ordenada conforme os criterios descritos no metodo ordem_dos_parlamentares.
    votacao -- objeto Votacao
    dicionario_votantes -- parlamentar -> (partido, int quantos votou)
    lista_ordenada_partidos -- lista de objetos Partido, ja bem ordenada.
    """
    retorno = []
    votos = votacao.voto_set.select_related('parlamentar','parlamentar__partido')
    parlamentares = [v.parlamentar for v in votos]
    ordenado = sorted([(lista_ordenada_partidos.index(p.partido),dicionario_votantes[p][1],p.nome,p) for p in parlamentares], key=itemgetter(2))
    ordenado = sorted(ordenado, key=itemgetter(1), reverse=True)
    ordenado = sorted(ordenado, key=itemgetter(0))
    return [x[3] for x in ordenado]

def ordenar_partidos(casa, periodo):
    """Retorna uma lista ordenada dos partidos da casa/periodo, conforme PCA."""
    analisador = AnalisadorPeriodo(casa_legislativa = casa,
                                   periodo = periodo)
    analise_periodo = analisador.analisa()
    coords = analise_periodo.coordenadas_partidos
    coords_list = []
    for k in coords.iteritems():
        coords_list.append(k)
    partidos = sorted([(x[0],x[1][0]) for x in coords_list], key=itemgetter(1,0))
    return [p[0] for p in partidos]
    
def ordenar_votantes(proposicao):
    """Retorna um dicionario Parlamentar -> (partido,int)
    onde o inteiro é o número de vezes que o parlamentar votou SIM ou NAO,
    mas nao se absteve ou faltou, nas votacoes da proposicao, e partido é o
    seu partido."""
    votos_prop = Voto.objects.filter(votacao__proposicao = proposicao).select_related("parlamentar", "parlamentar__partido")
    parlams = set()
    for v in votos_prop:
        parlams.add(v.parlamentar)
    retorno = {}
    for prl in parlams:
        retorno[prl] = (prl.partido,len([vv for vv in votos_prop if vv.parlamentar == prl]))
    return retorno

    
