# Create your views here.
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'radar_parlamentar.views.home', name='home'),
    # url(r'^radar_parlamentar/', include('radar_parlamentar.foo.urls')),

    # Index
    url(r'^$', redirect_to, {'url' : '/index/'}),
    url(r'^index/$', 'radar_parlamentar.views.index'),
    url(r'^origem/$', 'radar_parlamentar.views.origem'),
    url(r'^ogrupo/$', 'radar_parlamentar.views.ogrupo'),
    url(r'^sim-voto-aberto/$', 'radar_parlamentar.views.votoaberto'),
    url(r'^importadores/$', 'radar_parlamentar.views.importadores'),
    url(r'^grafico_alternativo/$', 'radar_parlamentar.views.grafico_alternativo'),

    #Serivço que retorna conteúdo para plotar o mapa
    url(r'^analises/$', 'analises.views.analises'),
    url(r'^analises/analise/(?P<nome_curto_casa_legislativa>\w*)/$', 'analises.views.analise'),
    url(r'^analises/analise/(?P<nome_curto_casa_legislativa>\w*)/json_pca/$', 'analises.views.json_pca'),
    url(r'^analises/json_analise/(?P<nome_curto_casa_legislativa>\w*)/$', 'analises.views.json_analise'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
