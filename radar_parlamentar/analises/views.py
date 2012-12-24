# coding=utf8

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

from __future__ import unicode_literals
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from modelagem import models
from analise import JsonAnaliseGenerator
import logging

logger = logging.getLogger("radar")

def analises(request):
    return render_to_response('analises.html')

def analise(request, nome_curto_casa_legislativa):
    """ Retorna a lista de partidos para montar a legenda do gráfico"""
    
    partidos = models.Partido.objects.order_by('numero').all()
    casa_legislativa = get_object_or_404(models.CasaLegislativa,nome_curto=nome_curto_casa_legislativa)
    num_votacao = casa_legislativa.num_votacao()
    return render_to_response('analise.html', {'casa_legislativa':casa_legislativa, 'partidos':partidos,'num_votacao':num_votacao})


def json_pca(request, nome_curto_casa_legislativa):
    """Retorna o JSON com as coordenadas do gráfico PCA"""
    
    casa_legislativa = get_object_or_404(models.CasaLegislativa,nome_curto=nome_curto_casa_legislativa)
    gen = JsonAnaliseGenerator()
    json = gen.get_json(casa_legislativa)
    return HttpResponse(json, mimetype='application/json')

def senf(request):
        return render_to_response('senf.html')
