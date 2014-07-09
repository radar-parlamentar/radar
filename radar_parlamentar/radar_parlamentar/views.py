# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html', {},
                              context_instance=RequestContext(request))


def origem(request):
    return render_to_response('origem.html', {},
                              context_instance=RequestContext(request))


def ogrupo(request):
    return render_to_response('grupo.html', {},
                              context_instance=RequestContext(request))


def premiacoes(request):
    return render_to_response('premiacoes.html', {},
                              context_instance=RequestContext(request))


def radar_na_midia(request):
    return render_to_response('radar_na_midia.html', {},
                              context_instance=RequestContext(request))


def votoaberto(request):
    return render_to_response('votoaberto.html', {},
                              context_instance=RequestContext(request))


def importadores(request):
    return render_to_response('importadores.html', {},
                              context_instance=RequestContext(request))


def grafico_alternativo(request):
    return render_to_response('grafico_alternativo.html', {},
                              context_instance=RequestContext(request))


def genero(request):
    return render_to_response('genero.html', {},
                              context_instance=RequestContext(request))


def genero_termos_nuvem(request):
    return render_to_response('genero_tagcloud.html', {},
                              context_instance=RequestContext(request))


def genero_matriz(request):
    return render_to_response('genero_matriz.html', {},
                              context_instance=RequestContext(request))


def genero_treemap(request):
    return render_to_response('genero_treemap.html', {},
                              context_instance=RequestContext(request))


def genero_historia_legislaturas(request):
    return render_to_response('genero_historia.html', {},
                              context_instance=RequestContext(request))


def genero_perfil_partido(request):
    return render_to_response('genero_perfil_partido.html', {},
                              context_instance=RequestContext(request))


def genero_comparativo_partidos(request):
    return render_to_response('genero_comparativo_partidos.html', {},
                              context_instance=RequestContext(request))


def genero_futuro(request):
    return render_to_response('genero_futuro.html', {},
                              context_instance=RequestContext(request))


def genero_perfil_legis(request):
    return render_to_response('perfil_legis.html', {},
                              context_instance=RequestContext(request))


def dados_utilizados(request):
    return render_to_response('dados_utilizados.html', {},
                              context_instance=RequestContext(request))
