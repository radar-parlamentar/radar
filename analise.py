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
"""

import re
import numpy
import pca
import sys
import sqlite3 as lite

class Analise:
    """ Cada instância a guarda os resultados da análise em um período de tempo entre self.data_inicial e self.data_final, onde sao considerados os partidoslistados em self.lista_partidos e as proposicoes dos tipos listados em self.tipos_proposicao.

    == Construtor ==
    ----------------
    Para criar uma instância a, que corresponde a uma análise por exemplo do primeiro semestre de 2010, usar:

    import analise
    a = analise.Analise('2010-01-01','2010-30-06')

    Se for desejado incluir apenas alguns tipos de proposição, usar o terceiro argumento, e se for desejado incluir apenas alguns partidos, usar o quarto, por exemplo:

    a2 = analise.Analise('2010-01-01','2010-30-06',['MPV','PEC'],['PT','PMDB','PSDB','DEM','PSOL'])

    == Atributos ==
    ---------------
    Seja a um objeto do tipo Analise, então a possui os atributos abaixo, onde as letras entre chaves indicam as dimensões de objetos (matrizes) do tipo numpy.array :
        a.data_inicial : string 'aaaa-mm-dd'.
        a.data_final : string 'aaaa-mm-dd'.
        a.tipos_proposicao : lista de strings.
        a.lista_partidos : lista de strings com P partidos.
        a.lista_votacoes : lista de tuplas (idProp,idVot) com V votações.
        a.vetores_votacao [P]x[V]: elemento ij é o voto médio do partido i na votação j, entre -1(não) e 1(sim).
        a.quadrivet_vot [P]x[V]: elemento ij é uma tupla de 4 elementos representando o número de votos sim, não, abst. e obstr. do partido i na votação j.
        a.vetores_tamanho [P]x[V]: elemento ij é o número de deputados do partido i presentes na votação j.
        a.vetores_presenca [P]x[V]: elemento ij é a fração de deputados do partido i presentes na votação j (usa a.tamanho_partido como aproximação para o tamanho dos partidos).
        a.tamanho_partido [P]: Número total de deputados do partido i que apareceu em pelo menos uma votação do período.
        a.vetores_votacao_uf [E]x[V]: Votação média por estado. 'E' é o número de UFs.
        a.vetores_tamanho_uf [E]x[V]: Deputados presentes por estado por votação.
        a.tamanho_uf [E]: Número total de deputados do estado i que apareceu em pelo menos uma votação do período.
        a.pca : objeto da classe pca.PCA
        a.pca_uf : idem, mas analisado por UF e não por partido.
        a.semelhancas [P]x[P] : matriz simétrica de valores entre 0 e 100 representando a porcentagem de semelhança entre os partidos i e j (calculado pelo produto escalar).
        a.semelhancas2 [P]x[P] : matriz simétrica de valores entre 0 e 100 representando a semelhança entre partidos i e j, calculada pelo método da convolução.

        Objetos da classe pca.PCA possuem entre outros os atributos:
        a.pca.U [P][C] : contém os vetores votação porém na base dos componentes principais (em número C=V), não mais das votações.
        a.pca.Vt [C][V] : informa como construir os componentes principais a partir das votações.
        a.pca.eigen [C] : autovalores. Para obter variâncias explicadas por cada c.p., basta fazer eigen[j]/eigen.sum() .

    == Métodos (dinâmicos) ==
    -------------------------
    Seja a um objeto tipo análise, aplicam-se os métodos:

        a.tamanho_sigla(siglaPartido) : retorna o tamanho do partido pela sigla, ou seja, número de deputados diferentes encontrados no período do estudo.
        a.tamanho_estado(siglaUF) : retorna o tamanho do estado pela sigla.
        a.partidos_2d(), a.partidos_2d(arquivo) : retorna matriz com as coordenadas dos partidos nas duas primeiras componentes principais, e se fornecido o nome de um arquivo escreve-as no mesmo.
        a.estados_2d(), a.estados_2d(arquivo) : analogamente para a pca por estados.
        a.sem(siglaP1,siglaP2,tipo=2) : imprime e retorna a semelhança entre os dois partidos dados pelas siglas, calculada pelo método do produto escalar se tipo=1 ou pelo método da convolução se tipo=2 (default).
    """

    # Constantes:
    lista_ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
    db = 'resultados/camara.db'

    def __init__(self,data_inicial='2011-01-01',data_final='2011-12-31',tipos_proposicao=[],lista_partidos=[]):
        """ Construtor de objetos do tipo Analise, pede como argumentos:
        * As datas inicial e final entre as quais devem ser consideradas as votações;
        * Uma lista de strings com os tipos de proposição a analisar, deixar vazio para considerar todos os tipos;
        * Uma lista de strings com os partidos a incluir na análise, deixar vazio para incluir todos os partidos.
        São feitas análises de tamanho dos partidos e das UFs, análise de componentes principais (pca) por partido e por UFs, e análise de semelhança percentual pelo método do produto escalar.
        """
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.tipos_proposicao = tipos_proposicao
        self.lista_partidos = lista_partidos
        self.lista_votacoes = []

        # Verificar se datas foram entradas corretamente:
        if not (re.match('(19)|(20)\d\d-[01]\d-[0123]\d',data_inicial) and re.match('(19)|(20)\d\d-[01]\d-[0123]\d',data_final)):
            raise StandardError('Datas devem estar no formato "aaaa-mm-dd", mês e dia obrigatoriamente com dois dígitos.')

        if not self.tipos_proposicao: # se lista vazia, usar todos os tipos
            con = lite.connect(Analise.db)
            self.tipos_proposicao = con.execute('SELECT distinct tipo FROM PROPOSICOES').fetchall()
            con.close()
            i = 0 #Transformar lista de tuplas em lista de strings:
            for tp in self.tipos_proposicao: 
                self.tipos_proposicao[i] = tp[0]
                i += 1

        if not self.lista_partidos: # se lista vazia, usar todos os partidos
            con = lite.connect(Analise.db)
            self.lista_partidos = con.execute('SELECT partido FROM PARTIDOS').fetchall()
            con.close()
            i = 0 #Transformar lista de tuplas em lista de strings:
            for lp in self.lista_partidos: 
                self.lista_partidos[i] = lp[0]
                i += 1
        lista_partidos = self.lista_partidos

        # Criar dicionario com id dos partidos
        con = lite.connect(Analise.db)
        tabela_partidos = con.execute('select idPart,partido from partidos').fetchall()
        idPartido = {}
        for tp in tabela_partidos:
            idPartido[tp[1]] = tp[0]

        # copiar do bd as votacoes a considerar:
        stipos=''
        for t in self.tipos_proposicao:
            stipos = stipos + "'" + t + "',"
        stipos = "(" + stipos[0:len(stipos)-1] + ")"
        con = lite.connect(Analise.db)
        votacoes = con.execute('SELECT votacoes.idProp,idVot,data,sim,nao,abstencao,obstrucao FROM VOTACOES,PROPOSICOES WHERE votacoes.idProp=proposicoes.idProp AND date(data)>date(?) AND date(data)<date(?) AND proposicoes.tipo IN %s' % stipos,(data_inicial,data_final)).fetchall()
        self.num_votacoes = len(votacoes)
        for i in range(len(votacoes)): 
            self.lista_votacoes.append(votacoes[:][i][0:2])
        # Criar vetores votacao (partidos nas linhas (primeira dimensão), votações nas colunas (segunda dimensão), valor é o voto médio do partido, entre -1 (não) e 1 (sim))
        self.vetores_votacao = numpy.zeros((len(lista_partidos),self.num_votacoes))
        self.quadrivet_vot = numpy.empty((len(lista_partidos),self.num_votacoes),dtype=object)
        self.vetores_tamanho = numpy.zeros((len(lista_partidos),self.num_votacoes))
        self.vetores_presenca = numpy.zeros((len(lista_partidos),self.num_votacoes))
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
                self.quadrivet_vot[ip][iv] = (nsim,nnao,nabs,nobs)
                if ntot != 0:
                    self.vetores_votacao[ip][iv] = (float(nsim) - float(nnao)) / float(ntot)
                else:
                    self.vetores_votacao[ip][iv] = 0
                
                # Contar deputados presentes:
                deps_presentes_list = [list(numpy.array(eval(v[3]))[numpy.where(numpy.array(eval(v[3]))/100000==idPartido[p])]) + list(numpy.array(eval(v[4]))[numpy.where(numpy.array(eval(v[4]))/100000==idPartido[p])]) + list(numpy.array(eval(v[5]))[numpy.where(numpy.array(eval(v[5]))/100000==idPartido[p])]) + list(numpy.array(eval(v[6]))[numpy.where(numpy.array(eval(v[6]))/100000==idPartido[p])]) ]
#                deps_presentes_list = numpy.reshape(deps_presentes_list,(1,numpy.size(deps_presentes_list)))
                self.vetores_tamanho[ip][iv] = numpy.size(deps_presentes_list)
                for d in deps_presentes_list[0]:
                    num_deputados.add(d) # repetidos não entrarão duas vezes no set, permitindo calcular tamanho_partido.
            self.tamanho_partido[ip] = len(num_deputados)
            # Calcular vetores_presenca:
            ivv = -1
            for v in votacoes:
                ivv += 1
                self.vetores_presenca[ip][ivv] = self.vetores_tamanho[ip][ivv]/self.tamanho_partido[ip]
        matriz = self.vetores_votacao - self.vetores_votacao.mean(axis=0)
        self.pca = pca.PCA(matriz)


        # Mesma análise, mas por UF e não por partido
        lista_ufs = Analise.lista_ufs
#['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
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

                nsim = numpy.where(((numpy.array(eval(v[3]))/1000)%100)==(ie+1))[0].size
                nnao = numpy.where(((numpy.array(eval(v[4]))/1000)%100)==(ie+1))[0].size
                nabs = numpy.where(((numpy.array(eval(v[5]))/1000)%100)==(ie+1))[0].size
                nobs = numpy.where(((numpy.array(eval(v[6]))/1000)%100)==(ie+1))[0].size
                ntot = nsim + nnao + nabs + nobs
                if ntot != 0:
                    self.vetores_votacao_uf[ie][iv] = (float(nsim) - float(nnao)) / float(ntot)
                else:
                    self.vetores_votacao_uf[ie][iv] = 0
                # Contar deputados presentes:
                deps_presentes_list_uf = [ list(numpy.array(eval(v[3]))[numpy.where((numpy.array(eval(v[3]))/1000)%100==(ie+1))]) + list(numpy.array(eval(v[4]))[numpy.where((numpy.array(eval(v[4]))/1000)%100==(ie+1))]) + list(numpy.array(eval(v[5]))[numpy.where((numpy.array(eval(v[5]))/1000)%100==(ie+1))]) + list(numpy.array(eval(v[6]))[numpy.where((numpy.array(eval(v[6]))/1000)%100==(ie+1))]) ]
#                deps_presentes_list_uf = numpy.reshape(deps_presentes_list,(1,numpy.size(deps_presentes_list)))
                self.vetores_tamanho_uf[ie][iv] = numpy.size(deps_presentes_list_uf)
                for d in deps_presentes_list_uf[0]:
                    num_deputados_uf.add(d) # repetidos não entrarão duas vezes no set
            self.tamanho_uf[ie] = len(num_deputados_uf)
        matriz = self.vetores_votacao_uf - self.vetores_votacao_uf.mean(axis=0)
        self.pca_uf = pca.PCA(matriz)


        # Semelhancas entre partidos, segundo o produto escalar, normalizadas entre 0 e 100[%]
        self.semelhancas = numpy.zeros((len(lista_partidos),len(lista_partidos)))
        for i in range(0,len(lista_partidos)):
            for j in range(0,len(lista_partidos)):
                self.semelhancas[i][j] = 100 *( ( numpy.dot(self.vetores_votacao[i],self.vetores_votacao[j]) / (numpy.sqrt(numpy.dot(self.vetores_votacao[i],self.vetores_votacao[i])) * numpy.sqrt(numpy.dot(self.vetores_votacao[j],self.vetores_votacao[j])) ) ) + 1 )/ 2

        # Semelhancas entre partidos, segundo o método da convolução, normalizadas entre 0 e 100[%]
        self.semelhancas2 = numpy.zeros((len(lista_partidos),len(lista_partidos)))
        for i in range(len(lista_partidos)):
            for j in range(len(lista_partidos)):
                x = 0
                for k in range(self.num_votacoes) :
                    x += Analise._convolui(self.quadrivet_vot[i][k],self.quadrivet_vot[j][k])
                x = 100 * x / self.num_votacoes
                self.semelhancas2[i][j] = x

    def __str__(self):
        x = 'Data inicial: ' + self.data_inicial + '\nData final: ' + self.data_final + '\nVotações: ' + str(self.num_votacoes) + '\nTipos: ' + str(self.tipos_proposicao) + '\nPartidos: ' + str(self.lista_partidos)
        return x


    def tamanho_sigla(self,siglaPartido):
        """Retorna o tamanho do partido dada sua sigla
        """
        return self.tamanho_partido[self.lista_partidos.index(siglaPartido)]

    def tamanho_estado(self,siglaEstado):
        """Retorna o tamanho do estado (número de deputados) dada sua sigla
        """
        return self.tamanho_uf[Analise.lista_ufs.index(siglaEstado.upper())]

    def partidos_2d(self,arquivo=''):
        """Retorna matriz com as coordenadas dos partidos no plano 2d formado pelas duas primeiras componentes principais. 

        Se for passado como argumento o nome (não vazio) de um arquivo, o resultado da pca é escrito neste arquivo, caso contrário é escrito em stdout.
        """
        coordenadas = self.pca.U[:,0:2]
        fechar = False
        if arquivo:
            fo = open(arquivo,'w')
            fechar = True
        else:
            fo = sys.stdout
        ip = -1
        fo.write('Análise PCA - por partido\n')
        fo.write('de %s a %s (ano-mês-dia)\n\n' % (self.data_inicial,self.data_final))
        fo.write('Fração da variância explicada pelas dimensões:\n')
        fo.write('%f\n' % (self.pca.eigen[0]/self.pca.eigen.sum()))
        fo.write('%f\n' % (self.pca.eigen[1]/self.pca.eigen.sum()))
        fo.write('%f\n' % (self.pca.eigen[2]/self.pca.eigen.sum()))
        fo.write('%f\n' % (self.pca.eigen[3]/self.pca.eigen.sum()))
        fo.write('\nCoordenadas:\n')
        for p in self.lista_partidos:
            ip += 1
            fo.write('%s: [%f, %f]\n' % (p,coordenadas[ip,0],coordenadas[ip,1]) )
        fo.write('Tamanhos=%s\n' % str(self.tamanho_partido))
        if fechar:
            fo.close()
        return coordenadas


    def estados_2d(self,arquivo=''):
        """Retorna matriz com as coordenadas dos estados no plano 2d formado pelas duas primeiras componentes principais. 

        Se for passado como argumento o nome (não vazio) de um arquivo, o resultado da pca é escrito neste arquivo, caso contrário é escrito em stdout.
        """
        coordenadas = self.pca_uf.U[:,0:2]
        fechar = False
        if arquivo:
            fo = open(arquivo,'w')
            fechar = True
        else:
            fo = sys.stdout
        ie = -1
        fo.write('Análise PCA - por estado\n')
        fo.write('de %s a %s (ano-mês-dia)\n\n' % (self.data_inicial,self.data_final))
        fo.write('Fração da variância explicada pelas dimensões:\n')
        fo.write('%f\n' % (self.pca_uf.eigen[0]/self.pca_uf.eigen.sum()))
        fo.write('%f\n' % (self.pca_uf.eigen[1]/self.pca_uf.eigen.sum()))
        fo.write('%f\n' % (self.pca_uf.eigen[2]/self.pca_uf.eigen.sum()))
        fo.write('%f\n' % (self.pca_uf.eigen[3]/self.pca_uf.eigen.sum()))
        fo.write('\nCoordenadas:\n')
        for e in Analise.lista_ufs:
            ie += 1
            fo.write('%s: [%f, %f]\n' % (e,coordenadas[ie,0],coordenadas[ie,1]) )
        fo.write('Tamanhos=%s\n' % str(self.tamanho_uf))
        if fechar:
            fo.close()
        return coordenadas

    def sem(self,siglaP1,siglaP2,tipo=2):
        x = self.semelhancas[self.lista_partidos.index(siglaP1),self.lista_partidos.index(siglaP2)]
        x2 = self.semelhancas2[self.lista_partidos.index(siglaP1),self.lista_partidos.index(siglaP2)]
        print 'Semelhança entre %s e %s:' % (siglaP1,siglaP2)
        if tipo==1:
            print 'Método 1 (p. escalar): %5.1f%% <- valor retornado' % x
            print 'Método 2 (convolução): %5.1f%%' % x2
            return x
        elif tipo==2:
            print 'Método 1 (p. escalar): %5.1f%%' % x
            print 'Método 2 (convolução): %5.1f%% <- valor retornado' % x2
            return x2

    @staticmethod
    def _convolui(u,v):
        """Recebe duas tuplas de 4 inteiros u e v, representando os votos de dois partidos em uma votação. Por exemplo se u=(4,3,0,3) houve 4 sim, 3 não, 0 abstenções e 3 obstruções do partido na votação.
        Cada tupla é normalizada dividindo pela soma dos quadrados dos elementos, e a função retorna o produto escalar das duas tuplas normalizadas.
         """
        if sum(u)==0 or sum(v)==0:
            return numpy.NaN
        un= numpy.array(u,dtype=float)
        vn= numpy.array(v,dtype=float)
        x = numpy.dot(un,vn)
        x = x / ( numpy.sqrt(numpy.dot(un,un)) * numpy.sqrt(numpy.dot(vn,vn)) ) # normalizar
        return x
