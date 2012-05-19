#!/usr/bin/python
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
import model
from matplotlib.pyplot import figure, show, scatter,text
from matplotlib.patches import Ellipse
import matplotlib.colors

class Analise:
    """ Cada instância a guarda os resultados da análise em um período de tempo entre self.data_inicial e self.data_final, onde sao considerados os partidos listados em self.lista_partidos e as proposicoes dos tipos listados em self.tipos_proposicao.

    == Construtor ==
    ----------------
    Para criar uma instância ANLS, que corresponde a uma análise por exemplo do primeiro semestre de 2010, usar:

    import analise
    ANLS = analise.Analise('2010-01-01','2010-30-06')

    Se for desejado incluir apenas alguns tipos de proposição, usar o terceiro argumento, e se for desejado incluir apenas alguns partidos, usar o quarto, por exemplo:

    ANLS2 = analise.Analise('2010-01-01','2010-30-06',['MPV','PEC'],['PT','PMDB','PSDB','DEM','PSOL'])

    Em vez de uma lista de partidos, o quarto argumento pode ser um inteiro N para incluir apenas partidos com N ou mais deputados. Por exemplo para usar todos os tipos de proposição mas apenas partidos com 6 ou mais deputados:

    ANLS3 = analise.Analise('2010-01-01','2010-30-06',[],6)

    == Atributos ==
    ---------------
    Seja ANLS um objeto do tipo Analise, então ANLS possui os atributos abaixo, onde as letras entre chaves indicam as dimensões de objetos (matrizes) do tipo numpy.array :
        ANLS.data_inicial : string 'aaaa-mm-dd'
        ANLS.data_final : string 'aaaa-mm-dd'
        ANLS.tipos_proposicao : lista de strings
        TODO: Substituir 'lista_partidos' por 'partidos'
        ANLS.lista_partidos : lista de strings com P partidos 
        ANLS.partidos : lista de objetos do tipo Partido
        ANLS.lista_votacoes : lista de tuplas (idProp,idVot) com V votações
        ANLS.vetores_votacao [P]x[V]: elemento ij é o voto médio do partido i na votação j, entre -1(não) e 1(sim)
        ANLS.quadrivet_vot [P]x[V]: elemento ij é uma tupla de 4 elementos representando o número de votos sim, não, abst. e obstr. do partido i na votação j
        ANLS.vetores_tamanho [P]x[V]: elemento ij é o número de deputados do partido i presentes na votação j
        ANLS.vetores_presenca [P]x[V]: elemento ij é a fração de deputados do partido i presentes na votação j (usa a.tamanho_partidos como aproximação para o tamanho dos partidos)
        ANLS.tamanho_partidos [P]: Lista com número total de deputados, com presença mínima de 1 votação no período, do partido i
        ANLS.vetores_votacao_uf [E]x[V]: Votação média por estado. 'E' é o número de UFs
        ANLS.vetores_tamanho_uf [E]x[V]: Deputados presentes por estado por votação
        ANLS.tamanho_uf [E]: Número total de deputados, com presença mínima de 1 votação no período, do estado i
        ANLS.pca : objeto da classe pca.PCA
        ANLS.pca_partido : objeto da classe pca.PCA analisado por partido
        ANLS.pca_uf : objeto da classe pca.PCA analisado por UF
        ANLS.semelhancas_escalar [P]x[P] : matriz simétrica de valores entre 0 e 100 representando a porcentagem de semelhança entre os partidos i e j (calculado pelo produto escalar)
        ANLS.semelhancas_convolucao [P]x[P] : matriz simétrica de valores entre 0 e 100 representando a semelhança entre partidos i e j, calculada pelo método da convolução

        Objetos da classe pca.PCA possuem entre outros os atributos:
        a.pca.U [P][C] : contém os vetores votação porém na base dos componentes principais (em número C=V), não mais das votações
        a.pca.Vt [C][V] : informa como construir os componentes principais a partir das votações
        a.pca.eigen [C] : autovalores. Para obter variâncias explicadas por cada c.p., basta fazer eigen[j]/eigen.sum() 

    == Métodos (dinâmicos) ==
    -------------------------
    Seja ANLS um objeto tipo análise, aplicam-se os métodos:

        TODO: Juntar 'tamanho_sigla' e 'tamanho_estado' num único método, passando como parâmetro a entidade que se quer ter o tamanho (partido ou UF)
        ANLS.tamanho_sigla(siglaPartido) : retorna o tamanho do partido pela sigla, ou seja, número de deputados diferentes encontrados no período do estudo
        ANLS.tamanho_estado(siglaUF) : retorna o tamanho do estado pela sigla
        TODO: Juntar 'partidos_2d' e 'estados_2d' num único método
        ANLS.partidos_2d(), a.partidos_2d(arquivo) : retorna matriz com as coordenadas dos partidos nas duas primeiras componentes principais, e se fornecido o nome de um arquivo escreve-as no mesmo
        ANLS.estados_2d(), a.estados_2d(arquivo) : analogamente para a pca por estados
        ANLS.sem(siglaP1,siglaP2,tipo=2) : imprime e retorna a semelhança entre os dois partidos dados pelas siglas, calculada pelo método do produto escalar (tipo=1) ou pelo método da convolução (tipo=2)(default)
        ANLS.figura(escala=10) : apresenta um gráfico de bolhas dos partidos com a primeira componente principal no eixo x e a segunda no eixo y, o tamanho da bolha proporcional ao tamanho do partido
    """

    # Constantes:
    lista_ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
    db = 'resultados/camara.db'

    def __init__(self,data_inicial='2011-01-01',data_final='2011-12-31',tipos_proposicao=[],lista_partidos=[],partidos=[]):
        """ Construtor de objetos do tipo Analise, pede como argumentos:
        * As datas inicial e final entre as quais devem ser consideradas as votações;
        * Uma lista de strings com os tipos de proposição a analisar, deixar vazio para considerar todos os tipos;
        * Uma lista de strings com os partidos a incluir na análise (deixar vazio para incluir todos os partidos), ou um inteiro N para usar partidos que tenham N ou mais deputados no período 
        São feitas análises de tamanho dos partidos e das UFs, análise de componentes principais (pca) por partido e por UFs, e análise de semelhança percentual por dois métodos.
        """
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.tipos_proposicao = tipos_proposicao
        self.lista_partidos = lista_partidos
        self.partidos = partidos
        self.num_votacoes = 0     # { calculados por
        self.lista_votacoes = []  #   self._buscaVotacoes() }
        self.vetores_votacao = [] # {
        self.quadrivet_vot = []   #   calculados por   
        self.vetores_tamanho = [] #   self._inicializa_vetores() 
        self.vetores_presenca = []#
        self.tamanho_partidos = [] #  }
        self.vetores_votacao_uf = [] # { calculados por
        self.vetores_tamanho_uf = [] #   self_inicializa_vetores_uf()
        self.tamanho_uf = []         # }
        self.pca_partido = None # calculado por self._pca_partido()
        self.pca_uf = None # calculado por self._pca_uf()
        self.semelhancas_escalar = [] # self._calcula_semelhancas()
        self.semelhancas_convolucao = [] # idem

        # Verificar se datas foram entradas corretamente:
        if not (re.match('(19)|(20)\d\d-[01]\d-[0123]\d',data_inicial) and re.match('(19)|(20)\d\d-[01]\d-[0123]\d',data_final)):
            raise StandardError('Datas devem estar no formato "aaaa-mm-dd", mês e dia obrigatoriamente com dois dígitos.')

        # se lista 'tipos_proposicao' vazia, usar todos os tipos de proposição
        if not self.tipos_proposicao: 
            con = lite.connect(Analise.db)
            lista = con.execute('SELECT distinct tipo FROM PROPOSICOES')
            for tipo in lista:
                self.tipos_proposicao.append(tipo[0])
            con.close()

        # se lista vazia, usar todos os partidos
        if not self.lista_partidos:
            popula_partidos = 0
            if not self.partidos:
                popula_partidos = 1
            con = lite.connect(Analise.db)
            lista = con.execute('SELECT * FROM PARTIDOS')
            lista_gambiarra = ['PT', 'PSDB', 'PV', 'PSOL', 'PCdoB', 'PP', 'PR', 'DEM', 'PMDB', 'PSC', 'PTB', 'PDT', 'PSB', 'PPS', 'PRB']
            for item in lista:
                if item[1] in lista_gambiarra:
                    self.lista_partidos.append(item[1])
                    if popula_partidos:
                        partido = model.Partido(item[1],item[0])
                        self.partidos.append(partido)
            con.close()
        # se inteiro, usar partidos maiores ou iguais a este inteiro
        elif isinstance(self.lista_partidos,int): 
            N = self.lista_partidos
            self.lista_partidos = partidos_expressivos(N,self.data_inicial,self.data_final,self.tipos_proposicao)

    #imprime informações principais da classe analise - utilizado ao se dar 'print' do objeto 'ANA'
    def __str__(self):
        retorno = ''
        retorno = retorno + 'Data inicial da análise : ' + self.data_inicial + '\n'
        retorno = retorno + 'Data final da análise: ' + self.data_final + '\n'
        retorno = retorno + 'Total de Votações analisadas: ' + str(self.num_votacoes) + '\n'
        retorno = retorno + 'Tipos de matérias analisadas: ' + '\n'
        for tipo in self.tipos_proposicao:
            retorno = retorno + '    ' + tipo + '\n'
        retorno = retorno + 'Partidos analisados: ' + '\n'
        for partido in self.partidos:
            retorno = retorno + '    ' + partido.nome + '\n'
        return retorno

    def _buscaVotacoes(self):
        """Copia votações do BD (sqlite) para uma lista (python), e a retorna."""
        filtro_tipos='('
        for tipo in self.tipos_proposicao:
            filtro_tipos = filtro_tipos + "'" + tipo + "',"
        filtro_tipos = filtro_tipos[0:len(filtro_tipos)-1] + ")"
        con = lite.connect(Analise.db)
        votacoes = con.execute('SELECT votacoes.idProp,idVot,data,sim,nao,abstencao,obstrucao FROM VOTACOES,PROPOSICOES WHERE votacoes.idProp=proposicoes.idProp AND date(data)>date(?) AND date(data)<date(?) AND proposicoes.tipo IN %s' % filtro_tipos,(self.data_inicial,self.data_final)).fetchall()
        self.num_votacoes = len(votacoes)
        for i in range(len(votacoes)): 
            self.lista_votacoes.append(votacoes[:][i][0:2])
        return votacoes


    def _inicializa_vetores(self):
        """Cria os 'vetores' e 'quadrivetores' votação agregados por partido. Aproveita para calcular o tamanho dos partidos, presença dos deputados, etc.
        O 'vetor' usa um número entre -1 (não) e 1 (sim) para representar a posição global do partido em cada votação, sendo o vetor em si um de dimensão N formado pelas N votações.
        O 'quadrivetor' usa uma tupla de 4 inteiros para representar a posição do partido em cada votação, os inteiros são o número de deputados que votaram sim, não, abstenção e obstrução. O quadrivetor em si é um vetor com N destas tuplas."""
        # Pegar votações no BD:
        votacoes = self._buscaVotacoes()
        # Criar dicionario com id dos partidos
        con = lite.connect(Analise.db)
        tabela_partidos = con.execute('select numero,nome from partidos').fetchall()
        idPartido = {}
        for tp in tabela_partidos:
            idPartido[tp[1]] = tp[0]

        self.vetores_votacao = numpy.zeros((len(self.lista_partidos),self.num_votacoes))
        self.quadrivet_vot = numpy.empty((len(self.lista_partidos),self.num_votacoes),dtype=object)
        self.vetores_tamanho = numpy.zeros((len(self.lista_partidos),self.num_votacoes))
        self.vetores_presenca = numpy.zeros((len(self.lista_partidos),self.num_votacoes))
        self.tamanho_partidos = [0]*len(self.lista_partidos)
        ip =-1
        for p in self.lista_partidos:
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
                    num_deputados.add(d) # repetidos não entrarão duas vezes no set, permitindo calcular tamanho_partidos.
            self.tamanho_partidos[ip] = len(num_deputados)
            # Calcular vetores_presenca:
            ivv = -1
            for v in votacoes:
                ivv += 1
                self.vetores_presenca[ip][ivv] = self.vetores_tamanho[ip][ivv]/self.tamanho_partidos[ip]
        return


    def _pca_partido(self):
        """Roda a análise de componentes principais por partidos.
        Guarda o resultado em self.pca
        Retorna um dicionário no qual as chaves são as siglas dos partidos
        e o valor de cada chave é um vetor com as n dimensões da análise pca"""
        if not bool(self.pca_partido):
            if self.vetores_votacao==[]:
                self._inicializa_vetores()
            matriz = self.vetores_votacao - self.vetores_votacao.mean(axis=0)
            self.pca_partido = pca.PCA(matriz)
        dicionario = {}
        for partido, vetor in zip(self.partidos, self.pca_partido.U):
            dicionario[partido.nome] = vetor
        return dicionario

    def _inicializa_vetores_uf(self):
        """Análogo a _inicializa_vetores(self), mas agregado por estados e não por partidos."""
        # Pegar votações no BD:
        votacoes = self._buscaVotacoes()

        self.vetores_votacao_uf = numpy.zeros((len(Analise.lista_ufs),self.num_votacoes))
        self.vetores_tamanho_uf = numpy.zeros((len(Analise.lista_ufs),self.num_votacoes))
        self.tamanho_uf = [0]*len(Analise.lista_ufs)
        ie =-1
        for e in Analise.lista_ufs:
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
        return

    def _pca_uf(self):
        """Roda a análise de componentes principais por UF.
        Guarda o resultado em self.pca
        Retorna um dicionário no qual as chaves são as siglas dos partidos
        e o valor de cada chave é um vetor com as n dimensões da análise pca"""
        if not bool(self.pca_uf):
            if self.vetores_votacao_uf==[]:
                self._inicializa_vetores_uf()
            matriz = self.vetores_votacao_uf - self.vetores_votacao_uf.mean(axis=0)
            self.pca_uf = pca.PCA(matriz)
        dicionario = {}
        for uf, vetor in zip(self.lista_ufs, self.pca_uf.U):
            dicionario[uf]=vetor
        return dicionario

    def _calcula_semelhancas(self):
        """Calcula semelhancas entre todos os partidos da análise, dois a dois, segundo o produto escalar e o método da convolução, normalizadas entre 0 e 100[%].
        O resultado é guardado nos atributos self.semelhancas (produto escalar) e self.semelhancas2 (convolução). """
        if self.vetores_votacao==[]:
            self._inicializa_vetores()
        self.semelhancas_escalar = numpy.zeros((len(self.lista_partidos),len(self.lista_partidos)))
        self.semelhancas_convolucao = numpy.zeros((len(self.lista_partidos),len(self.lista_partidos)))
        for i in range(0,len(self.lista_partidos)):
            for j in range(0,len(self.lista_partidos)):
                # método 1:
                self.semelhancas_escalar[i][j] = 100 *( ( numpy.dot(self.vetores_votacao[i],self.vetores_votacao[j]) / (numpy.sqrt(numpy.dot(self.vetores_votacao[i],self.vetores_votacao[i])) * numpy.sqrt(numpy.dot(self.vetores_votacao[j],self.vetores_votacao[j])) ) ) + 1 )/ 2
                # método 2:
                x = 0
                for k in range(self.num_votacoes) :
                    x += Analise._convolui(self.quadrivet_vot[i][k],self.quadrivet_vot[j][k])
                x = 100 * x / self.num_votacoes
                self.semelhancas_convolucao[i][j] = x
        return

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


    def tamanho_sigla(self,siglaPartido):
        """Retorna o tamanho do partido dada sua sigla.
        """
        if self.tamanho_partidos==0:
            self._inicializa_vetores()
        try:
            return self.tamanho_partidos[self.lista_partidos.index(siglaPartido)]
        except ValueError:
            print "WARNING: Partido %s não presente na análise. Dados da análise:\n%s" % (siglaPartido,self)
            return 0

    def tamanho_estado(self,siglaEstado):
        """Retorna o tamanho do estado (número de deputados) dada sua sigla.
        """
        if self.tamanho_uf==[]:
            self._inicializa_vetores_uf()
        try:
            return self.tamanho_uf[Analise.lista_ufs.index(siglaEstado.upper())]
        except ValueError:
            raise ValueError('Estado "%s" inválido.'%siglaEstado)

    def partidos_2d(self,arquivo=''):
        """Retorna matriz com as coordenadas dos partidos no plano 2d formado pelas duas primeiras componentes principais. 

        Se for passado como argumento o nome (não vazio) de um arquivo, o resultado da pca é escrito neste arquivo, caso contrário é escrito em stdout.
        """
        coordenadas = self._pca_partido()
        for partido in coordenadas.keys():
            coordenadas[partido] = (coordenadas[partido])[0:2]
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
        fo.write('%f\n' % (self.pca_partido.eigen[0]/self.pca_partido.eigen.sum()))
        fo.write('%f\n' % (self.pca_partido.eigen[1]/self.pca_partido.eigen.sum()))
        fo.write('%f\n' % (self.pca_partido.eigen[2]/self.pca_partido.eigen.sum()))
        fo.write('%f\n' % (self.pca_partido.eigen[3]/self.pca_partido.eigen.sum()))
        fo.write('\nCoordenadas:\n')
        for partido in coordenadas.keys():
            fo.write('%s: [%f, %f]\n' % (partido,coordenadas[partido][0],coordenadas[partido][1]) )
        fo.write('Tamanhos=%s\n' % str(self.tamanho_partidos))
        if fechar:
            fo.close()
        return coordenadas


    def estados_2d(self,arquivo=''):
        """Retorna matriz com as coordenadas dos estados no plano 2d formado pelas duas primeiras componentes principais. 

        Se for passado como argumento o nome (não vazio) de um arquivo, o resultado da pca é escrito neste arquivo, caso contrário é escrito em stdout.
        """
        if not bool(self.pca_uf):
            self._pca_uf()
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
        if self.semelhancas_escalar==[]:
            self._calcula_semelhancas()
        x = self.semelhancas_escalar[self.lista_partidos.index(siglaP1),self.lista_partidos.index(siglaP2)]
        x2 = self.semelhancas_convolucao[self.lista_partidos.index(siglaP1),self.lista_partidos.index(siglaP2)]
        print 'Semelhança entre %s e %s:' % (siglaP1,siglaP2)
        if tipo==1:
            print 'Método 1 (p. escalar): %5.1f%% <- valor retornado' % x
            print 'Método 2 (convolução): %5.1f%%' % x2
            return x
        elif tipo==2:
            print 'Método 1 (p. escalar): %5.1f%%' % x
            print 'Método 2 (convolução): %5.1f%% <- valor retornado' % x2
            return x2


    def figura(self, escala=10):
        """Apresenta um plot de bolhas (usando matplotlib) com os partidos de tamanho maior ou igual a tamanho_min com o primeiro componente principal no eixo x e o segundo no eixo y.
        """
        dados = self.partidos_2d()

        fig = figure(1)
        fig.clf()

        cores_partidos = {'PT'   :'#FF0000',
                      'PSOL' :'#FFFF00',
                      'PV'   :'#00CC00',
                      'DEM'  :'#002664',
                      'PSDB' :'#0059AB',
                      'PSD'  :'#80c341',
                      'PMDB' :'#CC0000',
                      'PR'   :'#110274',
                      'PSC'  :'#25b84a',
                      'PSB'  :'#ff8d00',
                      'PP'   :'#203487',
                      'PCdoB':'#da251c',
                      'PTB'  :'#1f1a17',
                      'PPS'  :'#fea801',
                      'PDT'  :'#6c85b1',
                      'PRB'  :'#67a91e'}

        lista_cores_partidos = []
        for partido in self.partidos:
            if partido.nome in cores_partidos:
                lista_cores_partidos.append(cores_partidos[partido.nome])
            else:
                lista_cores_partidos.append((1,1,1))

        colormap_partidos = matplotlib.colors.ListedColormap(lista_cores_partidos,name='partidos')

        ax = fig.add_subplot(111, autoscale_on=True) #, xlim=(-1,5), ylim=(-5,3))
        x = []
        y = []
        for partido in self.partidos:
            x.append(dados[partido.nome][0])
            y.append(dados[partido.nome][1])
        size = numpy.array(self.tamanho_partidos) * escala
        scatter(x, y, size, range(len(x)), marker='o', cmap=colormap_partidos) #, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, faceted=True, verts=None, hold=None, **kwargs)

        for partido in self.partidos:
            text(dados[partido.nome][0]+.005,dados[partido.nome][1],partido.numero,fontsize=12,stretch=100,alpha=1)

        show()


def partidos_expressivos(N=1,data_inicial='2011-01-01',data_final='2011-12-31',tipos_proposicao=[]):
    """Retorna uma lista com os partidos com pelo menos N deputados diferentes que tenham vindo em votações entre as datas data_inicial e data_final. Consideram-se as proposições em tipos_proposição, ou todas se tipos_proposicao=[]."""
    # Criar dicionario com id dos partidos:
    con = lite.connect(Analise.db)
    tabela_partidos = con.execute('select numero,nome from partidos').fetchall()
    idPartido = {}
    for tp in tabela_partidos:
        idPartido[tp[1]] = tp[0]
    
    # Criar lista de todos os partidos:
    lista_todos_partidos = con.execute('SELECT nome FROM PARTIDOS').fetchall()
    con.close()
    # Pegar votacoes no bd:
    a = Analise(data_inicial,data_final,tipos_proposicao)
    votacoes = a._buscaVotacoes()
    # Inicializar variáveis
    tamanho_partidos = [0]*len(lista_todos_partidos) 
    vetores_tamanho = numpy.zeros((len(lista_todos_partidos),a.num_votacoes))
    #Transformar lista de tuplas em lista de strings:
    i = 0 
    for lp in lista_todos_partidos: 
        lista_todos_partidos[i] = lp[0]
        i += 1
    # Calcular tamanho dos partidos:
    ip =-1
    for p in lista_todos_partidos:
        ip += 1
        num_deputados = set() # Número de deputados diferentes de um partido que apareceram em pelo menos uma votação no período.
        iv =-1
        for v in votacoes:
            iv += 1
            # Contar deputados presentes:
            deps_presentes_list = [list(numpy.array(eval(v[3]))[numpy.where(numpy.array(eval(v[3]))/100000==idPartido[p])]) + list(numpy.array(eval(v[4]))[numpy.where(numpy.array(eval(v[4]))/100000==idPartido[p])]) + list(numpy.array(eval(v[5]))[numpy.where(numpy.array(eval(v[5]))/100000==idPartido[p])]) + list(numpy.array(eval(v[6]))[numpy.where(numpy.array(eval(v[6]))/100000==idPartido[p])]) ]
            vetores_tamanho[ip][iv] = numpy.size(deps_presentes_list)
            for d in deps_presentes_list[0]:
                num_deputados.add(d) # repetidos não entrarão duas vezes no set, permitindo calcular tamanho_partidos.
        tamanho_partidos[ip] = len(num_deputados)
    # Fazer lista de partidos maiores do que N:
    expressivos = []
    ip = -1
    for p in lista_todos_partidos:
        ip += 1
        if tamanho_partidos[ip] >= N:
            expressivos.append(p)
    return expressivos

if __name__ == "__main__":
    Analise().figura()
