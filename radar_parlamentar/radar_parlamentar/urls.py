from django.urls import include, path
from django.shortcuts import redirect

from . import views as radar_views
from analises import views as analises_views
from importadores import views as importadores_views
from plenaria import views as plenaria_views

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', radar_views.index, name="index"),
    path('index/', redirect, {'url': '/'}),
    path('origem/', radar_views.origem, name="origem"),
    path('ogrupo/', radar_views.ogrupo, name="ogrupo"),
    path('premiacoes/', radar_views.premiacoes, name="premiacoes"),
    path('radarnamidia/', radar_views.radar_na_midia, name="radar_na_midia"),
    path('sim-voto-aberto/', radar_views.votoaberto, name="votoaberto"),
    path('blog/', radar_views.generate_blog_news, name="blog"),
    path('dados/downloads/', radar_views.dados_utilizados),
    path('dados', radar_views.dados_utilizados),  # URL legada
]

urlpatterns += [
    path('dados/importadores/', radar_views.importadores, name="importadores"),
    path('importar/<nome_curto_casa_legislativa>/',
         importadores_views.importar),
    # Páginas do Projeto Gênero do Hackathon da Câmara dos Deputados em 2013
    path('genero/', radar_views.genero, name="genero"),
    path('genero/tematica/partido/', radar_views.genero_matriz,
         name="genero_matriz"),
    path('genero/perfil/partido/', radar_views.genero_perfil_partido,
         name="genero_perfil_partido"),
    path('genero/perfil/partido/comparacao/',
         radar_views.genero_comparativo_partidos,
         name="genero_comparativo_partidos"),
    path('genero/perfil/legislaturas/',
         radar_views.genero_historia_legislaturas,
         name="genero_historia_legislaturas"),
    path('genero/tematica/treemap/', radar_views.genero_treemap,
         name="genero_treemap"),
    path('genero/tematica/legislador/', radar_views.genero_futuro,
         name="genero_futuro"),
    path('genero/tematica/nuvem/', radar_views.genero_termos_nuvem,
         name="genero_termos_nuvem"),
    path('genero/tematica/nuvem/?Pcasa_legislativa=',
         radar_views.genero_termos_nuvem),

    # Serviço que retorna conteúdo para plotar o mapa
    path(url_radar + casa_legislativa, analises_views.analise),
    path(url_json_radar + casa_legislativa + periodicidade,
         analises_views.json_analise),
    path(url_json_radar + casa_legislativa + periodicidade + palavras_chave,
         analises_views.json_analise),
    path(url_lista + casa_legislativa,
         analises_views.lista_de_votacoes_filtradas),
    path(url_lista + casa_legislativa + periodicidade + palavras_chave,
         analises_views.lista_de_votacoes_filtradas),

    # Páginas da Plenária - Hackathon Eleições 2016
    path(url_plenaria, plenaria_views.plenaria),
    path(url_plenaria + casa_legislativa, plenaria_views.plenaria),
    path(url_plenaria + casa_legislativa + identificador_proposicao,
         plenaria_views.plenaria),
    path(url_json_plenaria + casa_legislativa + identificador_proposicao,
         plenaria_views.json_proposicao),

    ###########################################################################
    # URLS legadas
    #
    # Aqui temos definidas algumas urls com redirects para manter
    # compatibilidade com links já divulgados publicamente com urls que não
    # serão mais utilizadas.
    #
    # Serviço que retorna conteúdo para plotar o mapa

    path('analises/analise/' + casa_legislativa,
         analises_views.redirect_analise, name="redirect_analise"),

    path('analises/json_analise/' + casa_legislativa + periodicidade,
         analises_views.redirect_json_analise, name="redirect_json_analise"),

    path('analises/json_analise/' + casa_legislativa + periodicidade +
         palavras_chave, analises_views.redirect_json_analise_p_chave,
         name="redirect_json_analise_p_chave"),

    path('analises/lista_de_votacoes_filtradas/' + casa_legislativa,
         analises_views.redirect_votacoes_filtradas,
         name="redirect_votacoes_filtradas"),

    path('analises/lista_de_votacoes_filtradas/' + casa_legislativa +
         periodicidade + palavras_chave,
         analises_views.redirect_lista_votacoes_p_chave,
         name="redirect_lista_votacoes_p_chave"),

    # Páginas da Plenária - Hackathon Eleições 2016
    path('analises/' + url_plenaria + casa_legislativa +
         identificador_proposicao,
         analises_views.redirect_plenaria, name="redirect_plenaria"),

    path('json_plenaria/' + casa_legislativa + identificador_proposicao,
         analises_views.redirect_json_plenaria, name="redirect_json_plenaria"),

    path('dados', analises_views.redirect_dados, name="redirect_dados"),

    path('importadores/',
         analises_views.redirect_importadores, name="redirect_importadores")
]
