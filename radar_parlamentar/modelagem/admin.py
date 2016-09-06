# coding=utf8

# Copyright (C) 2014, Saulo Trento
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

from modelagem.models import *
from django.contrib import admin


class ParlamentarAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'genero')
    list_filter = ['genero']


class ProposicaoAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'sigla', 'numero', 'ano', 'ementa',
                    'descricao', 'indexacao', 'data_apresentacao',
                    'casa_legislativa')
    list_filter = ['ano', 'casa_legislativa']
    search_fields = ['sigla', 'numero', 'ano', 'ementa', 'descricao',
                     'indexacao']


class VotacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'data', 'resultado', 'proposicao')
    search_fields = ['descricao', 'proposicao']
    date_hierarchy = 'data'


class VotoAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'votacao')

admin.site.register(Indexadores)
admin.site.register(Partido)
admin.site.register(CasaLegislativa)
admin.site.register(Parlamentar, ParlamentarAdmin)
admin.site.register(Proposicao, ProposicaoAdmin)
admin.site.register(Votacao, VotacaoAdmin)
admin.site.register(Voto, VotoAdmin)
admin.site.register(ChefeExecutivo)
