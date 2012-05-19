# coding=utf8

# Copyright (C) 2012, Leonardo Leite
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError

class Partido:
    """Partido político.

    Atributos:
        nome -- string; ex: 'PT' 
        numero -- string; ex: '13'
    """

    def __init__(self):
        self.nome = ''
        self.numero = ''

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return unicode(self).encode('utf-8')


class Proposicao:
    """Proposição parlamentar (proposta de lei)
    
    Atributos:
        id -- string identificadora da string
        sigla, numero, ano -- string que juntas formam o nome legal da proposição
        ementa-- descrição sucinta e oficial
        descricao -- descrição mais detalhada
        indexacao -- palavras chaves
        autores -- lista de objetos do tipo Parlamentar
        data_apresentacao -- quando foi proposta
        situacao -- como está agora
        casa_legislativa -- objeto do tipo CasaLegislativa

    Métodos:
        nome: retorna "sigla numero/ano"
    """

    def __init__(self):
        self.id = ''
        self.sigla = ''
        self.numero = ''
        self.ano = ''
        self.ementa = ''
        self.descricao = ''
        self.indexacao = ''
        self.autores = []
        self.data_apresentacao = ''
        self.situacao = ''
        self.casa_legislativa = ''

    
    def nome(self):
        return "%s %s/%s" % (self.sigla, self.numero, self.ano)

    def __unicode__(self):
        return "[%s] %s" % (self.nome, self.ementa) 

    def __str__(self):
        return unicode(self).encode('utf-8')


