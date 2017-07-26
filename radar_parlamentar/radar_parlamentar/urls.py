# Create your views here.
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.conf.urls import *
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

casa_legislativa = '((?P<nome_curto_casa_legislativa>\w+)/)'
periodicidade = '(?P<periodicidade>\w*)/'
palavras_chave = '(?P<palavras_chave>.*)/'
identificador_proposicao = '((?P<identificador_proposicao>\w+-\d+-\d{4})/)'

url_radar = 'radar/'
url_genero = 'genero/'
url_plenaria = 'plenaria/'

url_json = 'json/'
url_json_radar = url_json + url_radar
url_json_plenaria = url_json + url_plenaria

url_lista = 'dados/votacoes/'

# urls legadas
raiz_analise_legada = 'analises/'
url_lista_legada = 'lista_de_votacoes_filtradas/'
url_json_analise_legada = 'json_analise/'
url_json_plenaria_legada = 'json_plenaria/'

urlpatterns = patterns(
    '',

    # Examples:
    # url(r'^$',
    #     'radar_parlamentar.views.home', name='home'),
    # url(r'^radar_parlamentar/', include(
    # 'radar_parlamentar.foo.urls')),

    # Index
    url(r'^$', 'radar_parlamentar.views.index', name="index"),
    url(r'^index/$', redirect, {'url': '/'}),
    url(r'^origem/$', 'radar_parlamentar.views.origem', name="origem"),
    url(r'^ogrupo/$', 'radar_parlamentar.views.ogrupo', name="ogrupo"),
    url(r'^premiacoes/$',
        'radar_parlamentar.views.premiacoes', name="premiacoes"),
    url(r'^radarnamidia/$',
        'radar_parlamentar.views.radar_na_midia', name="radar_na_midia"),
    url(r'^sim-voto-aberto/$',
        'radar_parlamentar.views.votoaberto', name="votoaberto"),
    url(r'^dados/importadores/$',
        'radar_parlamentar.views.importadores', name="importadores"),

    url(r'^importar/(?P<nome_curto_casa_legislativa>\w*)/$',
        'importadores.views.importar'),

    url(r'^dados/downloads/$',
        'radar_parlamentar.views.dados_utilizados'),

    url(r'^blog/$',
        'radar_parlamentar.views.generate_blog_news', name="blog"),

    # Páginas do Projeto Gênero do Hackathon da Câmara dos
    # Deputados em 2013
    url(r'^genero/$', 'radar_parlamentar.views.genero', name="genero"),
    url(r'^genero/tematica/partido/$',
        'radar_parlamentar.views.genero_matriz', name="genero_matriz"),
    url(r'^genero/perfil/partido/$',
        'radar_parlamentar.views.genero_perfil_partido',
        name="genero_perfil_partido"),
    url(r'^genero/perfil/partido/comparacao/$',
        'radar_parlamentar.views.genero_comparativo_partidos',
        name="genero_comparativo_partidos"),
    url(r'^genero/perfil/legislaturas/$',
        'radar_parlamentar.views.genero_historia_legislaturas',
        name="genero_historia_legislaturas"),
    url(r'^genero/tematica/treemap/$',
        'radar_parlamentar.views.genero_treemap', name="genero_treemap"),
    url(r'^genero/tematica/legislador/$',
        'radar_parlamentar.views.genero_futuro', name="genero_futuro"),
    url(r'^genero/tematica/nuvem/$',
        'radar_parlamentar.views.genero_termos_nuvem',
        name="genero_termos_nuvem"),
    url(r'^genero/tematica/nuvem/?Pcasa_legislativa=$',
        'radar_parlamentar.views.genero_termos_nuvem'),

    # Serviço que retorna conteúdo para plotar o mapa
    url(r'^' + url_radar + casa_legislativa + '$',
        'analises.views.analise'),
    url(r'^' + url_json_radar + casa_legislativa + periodicidade + '$',
        'analises.views.json_analise'),
    url(r'^' + url_json_radar + casa_legislativa + periodicidade +
        palavras_chave + '$',
        'analises.views.json_analise'),
    url(r'^' + url_lista + casa_legislativa + '$',
        'analises.views.lista_de_votacoes_filtradas'),
    url(r'^' + url_lista + casa_legislativa + periodicidade +
        palavras_chave + '$',
        'analises.views.lista_de_votacoes_filtradas'),

    # Páginas da Plenária - Hackathon Eleições 2016
    url(r'^' + url_plenaria + '$',
        'plenaria.views.plenaria'),
    url(r'^' + url_plenaria + casa_legislativa + '$',
        'plenaria.views.plenaria'),
    url(r'^' + url_plenaria + casa_legislativa + identificador_proposicao +
        '$',
        'plenaria.views.plenaria'),
    url(r'^' + url_json_plenaria + casa_legislativa +
        identificador_proposicao + '$',
        'plenaria.views.json_proposicao'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    ###########################################################################
    # URLS legadas
    #
    # Aqui temos definidas algumas urls com redirects para manter
    # compatibilidade com links já divulgados publicamente com urls que não
    # serão mais utilizadas.
    #
    # Serviço que retorna conteúdo para plotar o mapa

    url(r'^analises/analise/' + casa_legislativa + '$',
        "analises.views.redirect_analise",
        name="redirect_analise"),

    url(r'^analises/json_analise/' + casa_legislativa + periodicidade + '$',
        "analises.views.redirect_json_analise", name="redirect_json_analise"),


    url(r'^analises/json_analise/' + casa_legislativa + periodicidade +
        palavras_chave + '$',
        "analises.views.redirect_json_analise_p_chave",
        name="redirect_json_analise_p_chave"),

    url(r'^analises/lista_de_votacoes_filtradas/' + casa_legislativa + '$',
        "analises.views.redirect_votacoes_filtradas",
        name="redirect_votacoes_filtradas"),

    url(r'^analises/lista_de_votacoes_filtradas/' + casa_legislativa +
        periodicidade + palavras_chave + '$',
        "analises.views.redirect_lista_votacoes_p_chave", 
        name="redirect_lista_votacoes_p_chave"),

    # Páginas da Plenária - Hackathon Eleições 2016
    url(r'^analises/' + url_plenaria + casa_legislativa +
        identificador_proposicao + '$',
        "analises.views.redirect_plenaria", name="redirect_plenaria"),

    url(r'^json_plenaria/' + casa_legislativa +
        identificador_proposicao + '$',
        "analises.views.redirect_json_plenaria", name="redirect_json_plenaria"),

    url(r'^dados$', "analises.views.redirect_dados", name="redirect_dados"),

    url(r'^importadores/$',
        "analises.views.redirect_importadores", name="redirect_importadores")
)
