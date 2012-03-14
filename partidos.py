# -*- coding: utf-8 -*-

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

"""Módulo partidos -- funções para caracterização e comparação dos partidos

Funcões:
vetor_votacoes -- calcula o vetor de votações de um partido 
semelhanca -- calcula a semelhança entre dois partidos

Contantes:
PARTIDOS: lista com os nomes dos partidos
"""

import algebra

PARTIDOS = ['PT', 'PSDB', 'PV', 'PSOL', 'PCdoB', 'PP', 'PR', 'DEM', 'PMDB', 'PSC', 'PTB', 'PDT', 'PSB', 'PPS', 'PRB']

def vetor_votacoes(partido, proposicoes):
    """Calcula o vetor de votações de um partido 
    Argumentos:
    partido  -- nome do partido (string)
    proposicoes -- lista de proposições contendo votações

    Retorna:
    Uma lista representando o vetor de votações do partido
    """    
    vetor = []
    for prop in proposicoes:
        for votacao in prop.votacoes:
            dic = votacao.por_partido()
            voto = dic[partido]
            #vi = (voto.sim + 0.5*voto.abstencao) / (voto.sim + voto.nao + voto.abstencao) # análise antigo
            vi = (1*voto.sim + 0*voto.abstencao -1*voto.nao) / (voto.sim + voto.nao + voto.abstencao)
            vetor.append(vi)
    return vetor  

def semelhanca_vetores(vetor1, vetor2):
    nv1 = algebra.normaliza(vetor1)
    nv2 = algebra.normaliza(vetor2)
    return algebra.prod_escalar(nv1, nv2)

def semelhanca(partido1, partido2, proposicoes):
    """Calcula a semelhança entre dois partidos 
    A semelhança é implementada como o produto escalar dos vetores de votações normalizados
    Argumentos:
    partido1, partido2  -- nomes do partidos (string)
    proposicoes -- lista de proposições contendo votações

    Retorna:
    Um valor real \in [0,1] representando a semelhança entre os partidos
    """    
    v1 = vetor_votacoes(partido1, proposicoes)
    v2 = vetor_votacoes(partido2, proposicoes)
    sem = semelhanca_vetores(v1, v2)
    return (sem+1)/2


