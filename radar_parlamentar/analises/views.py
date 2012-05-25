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
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from modelagem import models
from analise import Analise



def cmsp(request):
    """ Retorna a lista de partidos para montar a legenda do gráfico"""
    partidos = models.Partido.objects.order_by('numero').all()
    return render_to_response('cmsp.html', {'partidos':partidos})

def json_cmsp(request):
    """Retorna JSON tipo {periodo:{nomePartido:{numPartido:1, tamanhoPartido:1, x:1, y:1}}"""

    periodos = ['20102', '20111', '20112', '20121']

    a2010 = Analise(None, '2011-01-01')
    a2011a = Analise('2011-01-02', '2011-07-01')
    a2011b = Analise('2011-07-02', '2012-01-01')
    a2012 = Analise('2011-01-02', None)

    analises = [a2011a, a2011b, a2012]
    a2010.partidos_2d()
    coadunados = [a2010.coordenadas]
    for a in analises:
        a.partidos_2d()
        coadunados.append(a.coordenadas)

    i = 0
    json = '{'
    for dic_pca in coadunados:
        json += '%s:%s ' % (periodos[i], json_ano(dic_pca, a2011a))
        i += 1
    json = json.rstrip(', ')
    json += '}'

    return HttpResponse(json, mimetype='application/json')


def json_ano(dic_pca, analise):

    analise._inicializa_tamanhos_partidos()
    nums = {}
    for p in models.Partido.objects.all():
        nums[p.nome] = p.numero

    json = '{'
    for part, coords in dic_pca.items():
        num = nums[part]
        tamanho = analise.tamanhos_partidos[part]
        x = round(coords[0], 2)
        y = round(coords[1], 2)
        json += '"%s":{"numPartido":%s, "tamanhoPartido":%s, "x":%s, "y":%s}, ' % (part, num, tamanho, x, y)
    json = json.rstrip(', ')
    json += '}, '
    return json


def cdep(request):
        return render_to_response('emconstrucao.html')


def senf(request):
        return render_to_response('emconstrucao.html')
