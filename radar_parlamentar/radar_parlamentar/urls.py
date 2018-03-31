from django.urls import include, path
from django.shortcuts import redirect

from . import views as radar_views
from analises import views as analises_views
from importadores import views as importadores_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

genero_patterns = [
    path('', radar_views.genero, name="genero"),
    path('tematica/partido/', radar_views.genero_matriz,
         name="genero_matriz"),
    path('perfil/partido/', radar_views.genero_perfil_partido,
         name="genero_perfil_partido"),
    path('perfil/partido/comparacao/',
         radar_views.genero_comparativo_partidos,
         name="genero_comparativo_partidos"),
    path('perfil/legislaturas/',
         radar_views.genero_historia_legislaturas,
         name="genero_historia_legislaturas"),
    path('tematica/treemap/', radar_views.genero_treemap,
         name="genero_treemap"),
    path('tematica/legislador/', radar_views.genero_futuro,
         name="genero_futuro"),
    path('tematica/nuvem/', radar_views.genero_termos_nuvem,
         name="genero_termos_nuvem"),
    path('tematica/nuvem/?Pcasa_legislativa=',
         radar_views.genero_termos_nuvem),
]

radar_patterns = [
    path("<nome_curto_casa_legislativa>/", analises_views.analise),
    path("json/<nome_curto_casa_legislativa>/<periodicidade>/",
         analises_views.json_analise),
    path("json/<nome_curto_casa_legislativa>/<periodicidade>/<palavras_chave>/",
         analises_views.json_analise),
]

votacoes_patterns = [
    path("<nome_curto_casa_legislativa>/",
         analises_views.lista_de_votacoes_filtradas),
    path("<nome_curto_casa_legislativa>/<periodicidade>/<palavras_chave>/",
         analises_views.lista_de_votacoes_filtradas),
]

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
    path('dados/', radar_views.dados_utilizados),  # URL legada
    path('dados/downloads/', radar_views.dados_utilizados),
    path('dados/importadores/', radar_views.importadores, name="importadores"),
    path('importar/<nome_curto_casa_legislativa>/',
         importadores_views.importar),
    path('plenaria/', include('plenaria.urls')),
    path('genero/', include(genero_patterns)),
    path('radar/', include(radar_patterns)),
    path('votacoes/', include(votacoes_patterns)),
]
