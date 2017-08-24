# coding=utf8

# Copyright (C) 2015, Vanessa Soares, Thaiane Braga
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
# along with Radar Parlamentar.  If not, see
#               <http://www.gnu.org/licenses/>.# -*- coding: utf-8 -*-


from django.template import RequestContext
from django.shortcuts import render
from django.contrib.staticfiles import finders
from analises.genero import Genero
import os
import datetime
import json
import logging
from .blog import DictionaryBlogGenerator
import feedparser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

logger = logging.getLogger("radar")


def index(request):
    return render(request, 'index.html')


def origem(request):
    return render(request, 'origem.html')


def ogrupo(request):
    return render(request, 'grupo.html')


def premiacoes(request):
    return render(request,'premiacoes.html')


def radar_na_midia(request):
    return render(request,'radar_na_midia.html')


def votoaberto(request):
    return render(request,'votoaberto.html')


def importadores(request):
    return render(request,'importadores.html')


# def grafico_alternativo(request):
#     return render(request,'grafico_alternativo.html', {},
#                               context_instance=RequestContext(request))


def genero(request):
    return render(request,'genero.html')


def genero_termos_nuvem(request):

    genero = Genero()

    casas_legislativas_com_genero = genero.get_casas_legislativas_com_genero()

    try:
        id_casa_legislativa = int(request.GET["casa_legislativa"])
    except:
        id_casa_legislativa = ""

    if not isinstance(id_casa_legislativa, int):

        return render(request,'genero_tagcloud.html',
                      {'casas_legislativas': casas_legislativas_com_genero})

    else:
        temas_frequencia_mulher = genero.agrupa_palavras('F',
                                                         id_casa_legislativa)
        temas_json_mulher = json.dumps(temas_frequencia_mulher)
        temas_frequencia_homem = genero.agrupa_palavras('M',
                                                        id_casa_legislativa)
        temas_json_homem = json.dumps(temas_frequencia_homem)

        return render(request,'genero_tagcloud.html',
                      {'temas_mulher': temas_json_mulher,
                       'temas_homem': temas_json_homem,
                       'casas_legislativas': casas_legislativas_com_genero})


def genero_matriz(request):
    return render(request,'genero_matriz.html')


def genero_treemap(request):
    return render(request,'genero_treemap.html')


def genero_historia_legislaturas(request):
    return render(request,'genero_historia.html')


def genero_perfil_partido(request):
    return render(request,'genero_perfil_partido.html')


def genero_comparativo_partidos(request):
    return render(request,'genero_comparativo_partidos.html')


def genero_futuro(request):
    return render(request,'genero_futuro.html')


# def genero_perfil_legis(request):
#     return render(request,'perfil_legis.html', {},
#                               context_instance=RequestContext(request))


def dados_utilizados(request):
    if finders.find('db-dump/radar.sql.bz2'):
        dump_file_path = finders.find('db-dump/radar.sql.bz2')
        time = os.path.getmtime(dump_file_path)
        dt = datetime.datetime.fromtimestamp(time)
        dt_str = dt.strftime('%d/%m/%Y')
        arquivo = True
        return render(request,'dados_utilizados.html',
                      {'dumpdate': dt_str, 'arquivo_dump': arquivo})
    else:
        arquivo = False
        return render(request,'dados_utilizados.html',
                      {'_arquivo_dump': arquivo})


def generate_blog_news(request):
    number_of_news = 10
    dictionary = DictionaryBlogGenerator.create_dict_blog()
    my_news = dictionary["items"]
    paginator = Paginator(my_news, number_of_news)

    page = request.GET.get('page')
    try:
        my_news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        my_news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        my_news = paginator.page(paginator.num_pages)
    return render(request,'blog.html', {'my_news': my_news})
