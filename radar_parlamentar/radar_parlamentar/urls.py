# Create your views here.
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$',
    #     'radar_parlamentar.views.home', name='home'),
    # url(r'^radar_parlamentar/', include(
    # 'radar_parlamentar.foo.urls')),

    # Index
    url(r'^$', 'radar_parlamentar.views.index'),
    url(r'^index/$', redirect_to, {'url': '/'}),
    url(r'^origem/$', 'radar_parlamentar.views.origem'),
    url(r'^ogrupo/$', 'radar_parlamentar.views.ogrupo'),
    url(r'^premiacoes/$',
        'radar_parlamentar.views.premiacoes'),
    url(r'^radarnamidia/$',
        'radar_parlamentar.views.radar_na_midia'),
    url(r'^sim-voto-aberto/$',
        'radar_parlamentar.views.votoaberto'),
    url(r'^importadores/$',
        'radar_parlamentar.views.importadores'),

    url(r'^dados/$',
        'radar_parlamentar.views.dados_utilizados'),
    url(r'^dados/(?P<dado_solicitado>\w*)/$',
        'exportadores.views.download_dados'),

    # Páginas do Projeto Gênero do Hackathon da Câmara dos
    # Deputados em 2013
    url(r'^genero/$', 'radar_parlamentar.views.genero'),
    url(r'^genero/tematica/partido/$',
        'radar_parlamentar.views.genero_matriz'),
    url(r'^genero/perfil/partido/$',
        'radar_parlamentar.views.genero_perfil_partido'),
    url(r'^genero/perfil/partido/comparacao/$',
        'radar_parlamentar.views.genero_comparativo_partidos'),
    url(r'^genero/perfil/legislaturas/$',
        'radar_parlamentar.views.genero_historia_legislaturas'),
    url(r'^genero/tematica/treemap/$',
        'radar_parlamentar.views.genero_treemap'),
    url(r'^genero/tematica/legislador/$',
        'radar_parlamentar.views.genero_futuro'),
    url(r'^genero/tematica/nuvem/$',
        'radar_parlamentar.views.genero_termos_nuvem'),

    # Serivço que retorna conteúdo para plotar o mapa
    url(r'^analises/analise/(?P<nome_curto_casa_legislativa>\w*)/$',
        'analises.views.analise'),
    url(r'^analises/json_analise/(?P<nome_curto_casa_legislativa>\w*)/(?P<periodicidade>\w*)/$',
        'analises.views.json_analise'),
    url(r'^analises/json_analise/(?P<nome_curto_casa_legislativa>\w*)/(?P<periodicidade>\w*)/(?P<palavras_chave>.*)/$',
        'analises.views.json_analise'),
    url(r'^analises/lista_de_votacoes_filtradas/(?P<nome_curto_casa_legislativa>\w*)/$', 
        'analises.views.lista_de_votacoes_filtradas'),
    url(r'^analises/lista_de_votacoes_filtradas/(?P<nome_curto_casa_legislativa>\w*)/(?P<periodicidade>\w*)/(?P<palavras_chave>.*)/$', 
        'analises.views.lista_de_votacoes_filtradas'),
    url(r'^analises/lista_de_votacoes_filtradas/(?P<nome_curto_casa_legislativa>\w*)/$', 'analises.views.lista_de_votacoes_filtradas'),
    url(r'^analises/lista_de_votacoes_filtradas/(?P<nome_curto_casa_legislativa>\w*)/(?P<periodicidade>\w*)/(?P<palavras_chave>.*)/$', 'analises.views.lista_de_votacoes_filtradas')

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
