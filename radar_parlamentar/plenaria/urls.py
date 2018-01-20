from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.plenaria),
    path('<nome_curto_casa_legislativa>/', views.plenaria),
    path('<nome_curto_casa_legislativa>/<identificador_proposicao>/',
         views.plenaria),
    path('json/<nome_curto_casa_legislativa>/<identificador_proposicao>/',
         views.json_proposicao),
]
