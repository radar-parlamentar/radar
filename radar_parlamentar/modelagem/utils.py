# coding=utf8

# Copyright (C) 2013, Leonardo Leite
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

from __future__ import unicode_literals
from django.utils.dateparse import parse_datetime

class MandatoLists:

    def get_mandatos_municipais(self, ini_date, end_date):
        """Retorna datas do início de cada mandato no período compreendido entre ini_date e end_date
            Argumentos:
                ini_date, end_date -- tipo date
            Retorno:
                lista do tipo date
            Obs: início de cada mandato é sempre em 1 de janeiro
        """
        ANO_INICIO_DE_ALGUM_MANDATO = 2009
        ANO_DE_REFERENCIA = ANO_INICIO_DE_ALGUM_MANDATO-4*500 # suficientemente no passado 
        defasagem = (abs(ANO_DE_REFERENCIA - ini_date.year)) % 4
        y = ini_date.year - defasagem 
        mandatos = []
        while y <= end_date.year:
            date_ini_mandato = parse_datetime('%s-01-01 00:00:00' % y)
            mandatos.append(date_ini_mandato)
            y += 4
        return mandatos
    
    
    
    
    
    
    
    