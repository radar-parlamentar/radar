# Create your views here.
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

url_plenaria = 'analises/plenaria/'
url_json_plenaria = 'analises/json_plenaria/'
url_analise = 'analises/analise/'
url_json_analise = 'analises/json_analise/'
url_lista = 'analises/lista_de_votacoes_filtradas/'
casa_legislativa = '((?P<nome_curto_casa_legislativa>\w+)/)'
periodicidade = '(?P<periodicidade>\w*)/'
palavras_chave = '(?P<palavras_chave>.*)/'
id_proposicao = '((?P<id_proposicao>\d+)/?)'

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$',
    #     'radar_parlamentar.views.home', name='home'),
    # url(r'^radar_parlamentar/', include(
    # 'radar_parlamentar.foo.urls')),

    # Index
    url(r'^$', 'radar_parlamentar.views.index', name="index"),
    url(r'^index/$', redirect_to, {'url': '/'}),
    url(r'^origem/$', 'radar_parlamentar.views.origem', name="origem"),
    url(r'^ogrupo/$', 'radar_parlamentar.views.ogrupo', name="ogrupo"),
    url(r'^premiacoes/$',
        'radar_parlamentar.views.premiacoes', name="premiacoes"),
    url(r'^radarnamidia/$',
        'radar_parlamentar.views.radar_na_midia', name="radar_na_midia"),
    url(r'^sim-voto-aberto/$',
        'radar_parlamentar.views.votoaberto', name="votoaberto"),
    url(r'^importadores/$',
        'radar_parlamentar.views.importadores', name="importadores"),

    url(r'^importar/(?P<nome_curto_casa_legislativa>\w*)/$',
        'importadores.views.importar'),

    url(r'^dados/$',
        'radar_parlamentar.views.dados_utilizados'),

    url(r'^blog/$',
        'radar_parlamentar.views.generate_blog_news', name="blog"),

    # Páginas do Projeto Gênero do Hackathon da Câmara dos
    # Deputados em 2013
    url(r'^genero/$', 'radar_parlamentar.views.genero', name="genero"),
    url(r'^genero/tematica/partido/$',
        'radar_parlamentar.views.genero_matriz', name="genero_matriz"),
    url(r'^genero/perfil/partido/$',
        'radar_parlamentar.views.genero_perfil_partido', name="genero_perfil_partido"),
    url(r'^genero/perfil/partido/comparacao/$',
        'radar_parlamentar.views.genero_comparativo_partidos', name="genero_comparativo_partidos"),
    url(r'^genero/perfil/legislaturas/$',
        'radar_parlamentar.views.genero_historia_legislaturas', name="genero_historia_legislaturas"),
    url(r'^genero/tematica/treemap/$',
        'radar_parlamentar.views.genero_treemap', name="genero_treemap"),
    url(r'^genero/tematica/legislador/$',
        'radar_parlamentar.views.genero_futuro', name="genero_futuro"),
    url(r'^genero/tematica/nuvem/$',
        'radar_parlamentar.views.genero_termos_nuvem', name="genero_termos_nuvem"),
    url(r'^genero/tematica/nuvem/?Pcasa_legislativa=$',
        'radar_parlamentar.views.genero_termos_nuvem'),

    # Serviço que retorna conteúdo para plotar o mapa
    url(r'^' + url_analise + casa_legislativa + '$',
        'analises.views.analise'),
    url(r'^' + url_json_analise + casa_legislativa + periodicidade + '$',
        'analises.views.json_analise'),
    url(r'^' + url_json_analise + casa_legislativa + periodicidade + palavras_chave + '$',
        'analises.views.json_analise'),
    url(r'^' + url_lista + casa_legislativa + '$',
        'analises.views.lista_de_votacoes_filtradas'),
    url(r'^' + url_lista + casa_legislativa + periodicidade + palavras_chave + '$',
        'analises.views.lista_de_votacoes_filtradas'),
    url(r'^' + url_lista + casa_legislativa + '$',
        'analises.views.lista_de_votacoes_filtradas'),
    url(r'^' + url_lista + casa_legislativa + periodicidade + palavras_chave + '$',
        'analises.views.lista_de_votacoes_filtradas'),

    # Páginas do Projeto Análise Votações Hackathon 2016
    url(r'^' + url_plenaria + casa_legislativa + '?' + \
        id_proposicao + '?' + '$',
        'plenaria.views.plenaria'),
    url(r'^' + url_json_plenaria + casa_legislativa + id_proposicao + '$',
        'plenaria.views.json_proposicao'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
