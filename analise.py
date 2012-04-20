# -*- coding: utf-8 -*-

# Copyright (C) 2012, Leonardo Leite, Saulo Trento, Diego Rabatone
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

"""Módulo analise -- Define a classe Analise, que possui os métodos para diversas análises, incluindo análise de semelhança e de componentes principais. Cada instância desta classe guarda os resultados da análise de um subconjunto dos dados, definido por um intervalo de tempo, pelos tipos de proposição a considerar e pelos partidos a considerar.

Funcões:
obter_votacao -- obtém votacões e detalhes de uma proposicão
obter_nomeProp_porid -- Obtém nome da proposição dado o id.
"""

import re
import numpy
import pca
import sqlite3 as lite

class Analise:
    """ Cada instância a guarda os resultados da análise em um período de tempo entre a.data_inicial e a.data_final, onde sao considerados os partidoslistados em a.lista_partidos e as proposicoes dos tipos listados em a.tipos_proposicao.
    """

    def __init__(self,data_inicial,data_final,tipos_proposicao=[],lista_partidos=[]):
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.tipos_proposicao = tipos_proposicao
        self.lista_partidos = lista_partidos

        # Verificar se datas foram entradas corretamente:
        if not (re.match('(19)|(20)\d\d-[01]\d-[0123]\d',data_inicial) and re.match('(19)|(20)\d\d-[01]\d-[0123]\d',data_final)):
            raise StandardError('Datas devem estar no formato "aaaa-mm-dd", mês e dia obrigatoriamente com dois dígitos.')

        if not self.tipos_proposicao: # se lista vazia, usar todos os tipos
            con = lite.connect('resultados/camara.db')
            self.tipos_proposicao = con.execute('SELECT distinct tipo FROM PROPOSICOES').fetchall()
            con.close()
            i = 0 #Transformar lista de tuplas em lista de strings:
            for tp in self.tipos_proposicao: 
                self.tipos_proposicao[i] = tp[0]
                i += 1

        if not self.lista_partidos: # se lista vazia, usar todos os partidos
            con = lite.connect('resultados/camara.db')
            self.lista_partidos = con.execute('SELECT partido FROM PARTIDOS').fetchall()
            con.close()
            i = 0 #Transformar lista de tuplas em lista de strings:
            for lp in self.lista_partidos: 
                self.lista_partidos[i] = lp[0]
                i += 1
        lista_partidos = self.lista_partidos

        # Criar dicionario com id dos partidos
        con = lite.connect('resultados/camara.db')
        tabela_partidos = con.execute('select idPart,partido from partidos').fetchall()
        idPartido = {}
        for tp in tabela_partidos:
            idPartido[tp[1]] = tp[0]

        # copiar do bd as votacoes a considerar:
        stipos=''
        for t in self.tipos_proposicao:
            stipos = stipos + "'" + t + "',"
        stipos = "(" + stipos[0:len(stipos)-1] + ")"
        con = lite.connect('resultados/camara.db')
        votacoes = con.execute('SELECT votacoes.idProp,idVot,data,sim,nao,abstencao,obstrucao FROM VOTACOES,PROPOSICOES WHERE votacoes.idProp=proposicoes.idProp AND date(data)>date(?) AND date(data)<date(?) AND proposicoes.tipo IN %s' % stipos,(data_inicial,data_final)).fetchall()
        self.num_votacoes = len(votacoes)
        # Criar vetores votacao (partidos nas linhas (primeira dimensão), votaçõess nas colunas (segunda dimensão), valor é o voto médio do partido, entre -1 (não) e 1 (sim))
        self.vetores_votacao = numpy.zeros((len(lista_partidos),self.num_votacoes))
        self.vetores_tamanho = numpy.zeros((len(lista_partidos),self.num_votacoes))
        self.tamanho_partido = [0]*len(lista_partidos)
        ip =-1
        for p in lista_partidos:
            ip += 1
            num_deputados = set() # Número de deputados diferentes de um partido que apareceram em pelo menos uma votação no período.
            iv =-1
            for v in votacoes:
                iv += 1

                nsim = numpy.where((numpy.array(eval(v[3]))/100000)==idPartido[p])[0].size
                nnao = numpy.where((numpy.array(eval(v[4]))/100000)==idPartido[p])[0].size
                nabs = numpy.where((numpy.array(eval(v[5]))/100000)==idPartido[p])[0].size
                nobs = numpy.where((numpy.array(eval(v[6]))/100000)==idPartido[p])[0].size
                ntot = nsim + nnao + nabs + nobs
                if ntot != 0:
                    self.vetores_votacao[ip][iv] = (nsim - nnao)/ntot
                else:
                    self.vetores_votacao[ip][iv] = 0
                # Contar deputados presentes:
                deps_presentes_list = [list(numpy.array(eval(v[3]))[numpy.where(numpy.array(eval(v[3]))/100000==idPartido[p])]) + list(numpy.array(eval(v[4]))[numpy.where(numpy.array(eval(v[4]))/100000==idPartido[p])]) + list(numpy.array(eval(v[5]))[numpy.where(numpy.array(eval(v[5]))/100000==idPartido[p])]) + list(numpy.array(eval(v[6]))[numpy.where(numpy.array(eval(v[6]))/100000==idPartido[p])]) ]
#                deps_presentes_list = numpy.reshape(deps_presentes_list,(1,numpy.size(deps_presentes_list)))
                self.vetores_tamanho[ip][iv] = numpy.size(deps_presentes_list)
                for d in deps_presentes_list[0]:
                    num_deputados.add(d) # repetidos não entrarão duas vezes no set
            self.tamanho_partido[ip] = len(num_deputados)
        matriz = self.vetores_votacao - self.vetores_votacao.mean(axis=0)
        self.pca = pca.PCA(matriz)


        # Mesma análise, mas por UF e não por partido
        lista_ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
        self.vetores_votacao_uf = numpy.zeros((len(lista_ufs),self.num_votacoes))
        self.vetores_tamanho_uf = numpy.zeros((len(lista_ufs),self.num_votacoes))
        self.tamanho_uf = [0]*len(lista_ufs)
        ie =-1
        for e in lista_ufs:
            ie += 1
            num_deputados_uf = set() # Número de deputados diferentes de um estado que apareceram em pelo menos uma votação no período.
            iv =-1
            for v in votacoes:
                iv += 1

                nsim = numpy.where(((numpy.array(eval(v[3]))/1000)%100)==ie)[0].size
                nnao = numpy.where(((numpy.array(eval(v[4]))/1000)%100)==ie)[0].size
                nabs = numpy.where(((numpy.array(eval(v[5]))/1000)%100)==ie)[0].size
                nobs = numpy.where(((numpy.array(eval(v[6]))/1000)%100)==ie)[0].size
                ntot = nsim + nnao + nabs + nobs
                if ntot != 0:
                    self.vetores_votacao_uf[ie][iv] = (nsim - nnao)/ntot
                else:
                    self.vetores_votacao_uf[ie][iv] = 0
                # Contar deputados presentes:
                deps_presentes_list_uf = [ list(numpy.array(eval(v[3]))[numpy.where((numpy.array(eval(v[3]))/1000)%100==ie)]) + list(numpy.array(eval(v[4]))[numpy.where((numpy.array(eval(v[4]))/1000)%100==ie)]) + list(numpy.array(eval(v[5]))[numpy.where((numpy.array(eval(v[5]))/1000)%100==ie)]) + list(numpy.array(eval(v[6]))[numpy.where((numpy.array(eval(v[6]))/1000)%100==ie)]) ]
                deps_presentes_list_uf = numpy.reshape(deps_presentes_list,(1,numpy.size(deps_presentes_list)))
                self.vetores_tamanho_uf[ie][iv] = numpy.size(deps_presentes_list_uf)
                for d in deps_presentes_list_uf[0]:
                    num_deputados_uf.add(d) # repetidos não entrarão duas vezes no set
            self.tamanho_uf[ie] = len(num_deputados_uf)
        matriz = self.vetores_votacao_uf - self.vetores_votacao_uf.mean(axis=0)
        self.pca_uf = pca.PCA(matriz)


        # Distancias entre partidos
        self.distancias = numpy.zeros((len(lista_partidos),len(lista_partidos)))
        for i in range(0,len(lista_partidos)):
            for j in range(0,len(lista_partidos)):
                self.distancias = numpy.dot(self.vetores_votacao[i],self.vetores_votacao[j])


    def __str__(self):
        x = 'Data inicial: ' + self.data_inicial + '\nData final: ' + self.data_final + '\nVotações: ' + str(self.num_votacoes) + '\nTipos: ' + str(self.tipos_proposicao) + '\nPartidos: ' + str(self.lista_partidos)
        return x
