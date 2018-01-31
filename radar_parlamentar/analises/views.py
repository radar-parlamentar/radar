# Copyright (C) 2012, Leonardo Leite
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


from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from modelagem import models
from modelagem import utils
from .grafico import JsonAnaliseGenerator
from .analise import AnalisadorTemporal
import datetime
import logging

logger = logging.getLogger("radar")


def analises(request):
    return render(request,'analises.html')


def analise(request, nome_curto_casa_legislativa):
    ''' Retorna a lista de partidos para montar a legenda do gráfico'''
    partidos = models.Partido.objects.order_by('numero').all()
    casa_legislativa = get_object_or_404(
        models.CasaLegislativa, nome_curto=nome_curto_casa_legislativa)
    periodicidade = request.GET.get('periodicidade', models.BIENIO)
    palavras_chave = request.GET.get('palavras_chave', '')
    nome_parlamentar = request.GET.get('nome_parlamentar', '')

    num_votacao = casa_legislativa.num_votacao()

    return render(request,'analise.html',
                  {'casa_legislativa': casa_legislativa,
                   'partidos': partidos,
                   'num_votacao': num_votacao,
                   'periodicidade': periodicidade,
                   'palavras_chave': palavras_chave,
                   'nome_parlamentar': nome_parlamentar})


@cache_page(60*60*24*2)
def json_analise(request, nome_curto_casa_legislativa,
                 periodicidade, palavras_chave=""):
    """Retorna o JSON com as coordenadas do gráfico PCA"""
    casa_legislativa = get_object_or_404(
        models.CasaLegislativa, nome_curto=nome_curto_casa_legislativa)
    lista_de_palavras_chave = \
        utils.StringUtils.transforma_texto_em_lista_de_string(palavras_chave)
    analisador = AnalisadorTemporal(
        casa_legislativa, periodicidade, lista_de_palavras_chave)
    analise_temporal = analisador.get_analise_temporal()
    gen = JsonAnaliseGenerator(analise_temporal)
    json = gen.get_json()
    return HttpResponse(json, content_type='application/json')


def lista_de_votacoes_filtradas(request,
                                nome_curto_casa_legislativa,
                                periodicidade=models.BIENIO,
                                palavras_chave=""):
    '''Exibe a lista de votações filtradas'''
    casa_legislativa = \
        get_object_or_404(models.CasaLegislativa,
                          nome_curto=nome_curto_casa_legislativa)
    lista_de_palavras_chave = \
        utils.StringUtils.transforma_texto_em_lista_de_string(palavras_chave)
    analisador = \
        AnalisadorTemporal(casa_legislativa, periodicidade,
                           lista_de_palavras_chave)
    votacoes = analisador.votacoes_filtradas()

    return render(request,'lista_de_votacoes_filtradas.html',
                  {'casa_legislativa': casa_legislativa,
                   'lista_de_palavras_chave': lista_de_palavras_chave,
                   'votacoes': votacoes,
                   'periodicidade': periodicidade})

def redirect_json_analise(request, nome_curto_casa_legislativa, periodicidade):
    url = (
            "/radar/json/{}/{}/"
            .format(nome_curto_casa_legislativa, periodicidade)
        )
    return HttpResponseRedirect(url)

def redirect_analise(request, nome_curto_casa_legislativa):
    url = (
            "/radar/{}"
            .format(nome_curto_casa_legislativa)
        )
    return HttpResponseRedirect(url)

def redirect_json_analise_p_chave(request, nome_curto_casa_legislativa,
                                  periodicidade, palavras_chave):
    url = (
            "/radar/json/{}/{}/{}"
            .format(nome_curto_casa_legislativa, periodicidade, palavras_chave)
        )
    return HttpResponseRedirect(url)

def redirect_votacoes_filtradas(request, nome_curto_casa_legislativa):
    url = (
            "/votacoes/{}"
            .format(nome_curto_casa_legislativa)
        )
    return HttpResponseRedirect(url)

def redirect_lista_votacoes_p_chave(request, nome_curto_casa_legislativa,
                                    periodicidade, palavras_chave):
    url = (
            "/votacoes/{}/{}/{}"
            .format(nome_curto_casa_legislativa, periodicidade, palavras_chave)
        )
    return HttpResponseRedirect(url)

def redirect_plenaria(request, nome_curto_casa_legislativa,
                      identificador_proposicao):
    url = (
            "/plenaria/{}/{}"
            .format(nome_curto_casa_legislativa, identificador_proposicao)
        )
    return HttpResponseRedirect(url)

def redirect_json_plenaria(request, nome_curto_casa_legislativa,
                      identificador_proposicao):
    url = (
            "/plenaria/json/{}/{}"
            .format(nome_curto_casa_legislativa, identificador_proposicao)
        )
    return HttpResponseRedirect(url)

def redirect_importadores(request):
    return HttpResponseRedirect("/dados/importadores")
