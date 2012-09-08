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
from analise import JsonAnaliseGenerator

def analises(request):
    return render_to_response('analise.html')

def cmsp(request):

    """ Retorna a lista de partidos para montar a legenda do gráfico"""
    partidos = models.Partido.objects.order_by('numero').all()
    return render_to_response('cmsp.html', {'partidos':partidos})

def json_cmsp(request):

    cmsp = models.CasaLegislativa.objects.get(nome_curto='cmsp')
    gen = JsonAnaliseGenerator()
    json = gen.get_json(cmsp)
    return HttpResponse(json, mimetype='application/json')

def cdep(request):
        return render_to_response('cdep.html')


def senf(request):
        return render_to_response('senf.html')
