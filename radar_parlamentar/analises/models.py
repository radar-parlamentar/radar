# coding=utf8

# Copyright (C) 2012, Leonardo Leite
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

class AnaliseTemporal:
    
    def __init__(self):
        self.casa_legislativa = None
        self.periodicidade = None
        self.area_total = 1
        self.analises_periodo = [] 
        self.votacoes = []


class AnalisePeriodo:
    
    def __init__(self):
        self.casa_legislativa = None
        self.periodo = None # PeriodoCasaLegislativa
        self.partidos = []
        self.votacoes = []
        self.num_votacoes = 0
        self.tamanhos_partidos = {}
        self.presencas_partidos = {}        
        self.soma_dos_tamanhos_dos_partidos = 0
        self.pca_partido = None
        self.coordenadas = {}
        
    

    