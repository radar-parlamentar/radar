# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Saulo Trento, Diego Rabatone, Guilherme Januário
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

"""Módulo analise"""

from __future__ import unicode_literals
import numpy
import pca
from django.utils.dateparse import parse_datetime
from django.db import connection
from modelagem import models
from matplotlib.pyplot import figure, show, scatter, text
from matplotlib.patches import Ellipse
import matplotlib.colors


class Analise:

    def __init__(self, data_inicio=None, data_fim=None, votacoes=None, partidos=None):
        """Argumentos:
            data_inicio e data_fim -- são strings no formato aaaa-mm-dd;
            Se este argumentos não são passadas, a análise é feita sobre todas as votações
            votacoes -- lista de objetos do tipo Votacao para serem usados na análise
                        se não for especificado, procura votações na base de dados de acordo data_inicio e data_fim.
            partidos -- lista de objetos do tipo Partido para serem usados na análise;
                        se não for especificado, usa todos os partidos no banco de dados.
        """

        self.ini = parse_datetime('%s 0:0:0' % data_inicio)
        self.fim = parse_datetime('%s 0:0:0' % data_fim)

        self.votacoes = votacoes
        if not self.votacoes: # pega votações do banco de dados
            if self.ini == None and self.fim == None:
                self.votacoes = models.Votacao.objects.all() 
            if self.ini == None and self.fim != None:
                self.votacoes = models.Votacao.objects.filter(data__lte=self.fim)
            if self.ini != None and self.fim == None:
                self.votacoes = models.Votacao.objects.filter(data__gte=self.ini)
            if self.ini != None and self.fim != None:
                self.votacoes = models.Votacao.objects.filter(data__gte=self.ini, data__lte=self.fim)

        # TODO que acontece se algum partido for ausente neste período?

        self.partidos = partidos
        if not self.partidos:
            self.partidos = models.Partido.objects.all()
        self.num_votacoes = len(self.votacoes)
        self.vetores_votacao = []
        self.pca_partido = []
        self.coordenadas = {}
        self.tamanhos_partidos = {}

    def _inicializa_tamanhos_partidos(self):
        """Retorna um dicionário cuja chave é o nome do partido, e o valor é a quantidade de parlamentares do partido no banco.

        Este dicionário é também salvo no atributo self.mapa_tamanho_partidos
        """
        self.tamanho_partidos = {}
        cursor = connection.cursor()
        for partido in self.partidos:
            # a linha comentada é mais django e mais portável, mas acho que a usada deve ser bem mais eficiente, 
            # pois não precisamos carregar os objetos
            # parlamentares = models.Parlamentar.objects.filter(partido=partido)
            # tamanho = len(parlamentares)
            cursor.execute("SELECT count(id) FROM modelagem_parlamentar WHERE partido_id = %s", [partido.id])
            tamanho = cursor.fetchone()[0]
            self.tamanhos_partidos[partido.nome] = tamanho
        return self.tamanhos_partidos

    def _inicializa_vetores(self):
        """Cria os 'vetores de votação' para cada partido. 

        O 'vetor' usa um número entre -1 (não) e 1 (sim) para representar a "posição média" do partido em cada votação, 
        tendo N dimensões correspondentes às N votações.
        Aproveita para calcular o tamanho dos partidos, presença dos parlamentares, etc.

        Retorna a 'matriz de votações', em que cada linha é um vetor de votações de um partido 
                A ordenação das linhas segue a ordem de self.partidos
        """

        # numpy.zeros((n,m)) gera matriz
        self.vetores_votacao = numpy.zeros((len(self.partidos), self.num_votacoes))
        self.debug = numpy.zeros(self.num_votacoes)

        iv =-1
        for v in self.votacoes:
            iv += 1
            self.debug[iv] = v.id_vot
            mapa_votos = v.por_partido() # mapa: chave é nome do partido, e valor é VotoPartido
            ip =-1
            for p in self.partidos:
                ip += 1
                if mapa_votos.has_key(p.nome):
                    votoPartido = mapa_votos[p.nome] # models.VotoPartido
                    self.vetores_votacao[ip][iv] = (float(votoPartido.sim) - float(votoPartido.nao)) / float(votoPartido.total())
                else:
                    self.vetores_votacao[ip][iv] = 0

        return self.vetores_votacao


    def _pca_partido(self):
        """Roda a análise de componentes principais por partidos.

        Guarda o resultado em self.pca
        Retorna um dicionário no qual as chaves são as siglas dos partidos
        e o valor de cada chave é um vetor com as n dimensões da análise pca
        """
        if not self.pca_partido:
            if not self.vetores_votacao:
                self._inicializa_vetores()
            matriz = self.vetores_votacao - self.vetores_votacao.mean(axis=0)
            self.pca_partido = pca.PCA(matriz)

        dicionario = {}
        for partido, vetor in zip(self.partidos, self.pca_partido.U):
            dicionario[partido.nome] = vetor
        return dicionario


    def partidos_2d(self):
        """Retorna mapa com as coordenadas dos partidos no plano 2D formado pelas duas primeiras componentes principais.

        A chave do mapa é o nome do partido (string) e o valor é uma lista de duas posições [x,y].
        """

        self.coordenadas = self._pca_partido()
        for partido in self.coordenadas.keys():
            self.coordenadas[partido] = (self.coordenadas[partido])[0:2]
        return self.coordenadas


    def _quantidade_movimento(self,dados_meus,dados_alheios,graus=0,espelho=0):
        """Calcula quantidade de movimento entre o instante i (corresponde ao ano anos[i]) e o instante i+1.
        No cálculo o instante i tem os eixos rotacionados (valor graus, entre 0 e 360), e o primeiro eixo multiplicado por -1 se espelho=0.
        """
        qm = 0
        antes = dados_meus.copy()
        depois = dados_alheios
        if espelho:
            for partido, coords in antes.items():
                antes[partido] = numpy.dot( coords,numpy.array( [[-1.,0.],[0.,1.]] ) )
        if graus != 0:
            for partido, coords in antes.items():
                antes[partido] = numpy.dot( coords,self._matrot(graus) )

        for p in self.partidos:
            #TODO esse selft.tamanhos_partidos antes pegava o do 'depois' - ver implicacoes da alteracao e arrumar
            qm += numpy.sqrt( numpy.dot( antes[p.nome] - depois[p.nome],  antes[p.nome] - depois[p.nome] ) ) * self.tamanhos_partidos[p.nome]
        return qm

    def _matrot(self,graus):
       """ Retorna matriz de rotação 2x2 que roda os eixos em graus (0 a 360) no sentido anti-horário (como se os pontos girassem no sentido horário em torno de eixos fixos).
       """ 
       graus = float(graus)
       rad = numpy.pi * graus/180.
       c = numpy.cos(rad)
       s = numpy.sin(rad)
       return numpy.array([[c,-s],[s,c]])

    def espelha_ou_roda(self, dados_alheios):
        print ' '
        print 'Espelhando e rotacionando...'
        dados_meus = self.partidos_2d()

        if not self.tamanhos_partidos:
            self._inicializa_tamanhos_partidos()

        # Rodar e espelhar eixos conforme a necessidade:
        # O sentido dos eixos que resultam na PCA é arbitrário, e se não dermos tanta importância ao significado do eixo x e do eixo y, mas sim principalmente à distância entre os partidos dois a dois que se reflete no plano, a rotação dos eixos é também arbitrária. Ao relacionar análises feitas em períodos de tempo diferentes (no caso, anos), os eixos de uma análise não têm relação com os da análise seguinte (pois foram baseados em votações distintas), então se fixarmos os eixos do ano i mais recente, o ano i-1 pode ter o eixo x espelhado ou não, e pode sofrer uma rotação de ângulo qualquer.
        # Gostaríamos que estas transformações fossem tais que minimizasse o movimento dos partidos: por exemplo se no ano i o partido A resultou no lado esquerdo do gráfico, e o partido B no lado direito, mas no ano i-1 o posicionamento resultou inverso, seria desejável espelhar o eixo x, ou então rodar os eixos de 180 graus.
        # Isso é alcançado através do algoritmo abaixo, de minimização da 'quantidade de movimento' total com a variação da rotação dos eixos e espelhamento do eixo x. Entre dois anos, esta quantidade de movimento é definida pela soma das distâncias euclidianas caminhadas pelos partidos ponderadas pelo tamanho do partido [no ano mais recente].
        qm_min = 1000000 # quero minimizar as quantidades de movimento
        campeao = (0,0) # (espelhar, graus)
        for espelhar in [0,1]:
            for graus in [0,45,90,135,180,225,270,315]:
                qm_agora = self._quantidade_movimento(dados_meus,dados_alheios,graus,espelhar)
                #print '%d, %d, %f' % (espelhar,graus,qm_agora )
                if qm_agora < qm_min:
                    campeao = (espelhar, graus)
                    qm_min = qm_agora
        print campeao
        if campeao[0] == 1: # espelhar
            for partido, coords in dados_alheios.items():
                dados_alheios[partido] = numpy.dot( coords, numpy.array([[-1.,0.],[0.,1.]]) )
        if campeao[1] != 0: # rotacionar
            for partido, coords in dados_alheios.items():
                dados_alheios[partido] = numpy.dot( coords, self._matrot(campeao[1]) )
        return dados_alheios

    
    #recebe um vetor onde cada elemento é um mapa de coordenadas
    def coaduna_bases(self, lista_dados):
        saida = []
        for d in lista_dados:
            saida.append(self.espelha_ou_roda(d))
        return saida




    def figura(self, escala=10):
        """Apresenta um plot de bolhas (usando matplotlib) com os partidos de tamanho maior ou igual a tamanho_min com o primeiro componente principal no eixo x e o segundo no eixo y.
        """

        if not self.tamanhos_partidos:
            self._inicializa_tamanhos_partidos()

        dados = self.coordenadas #self.partidos_2d()

        if not self.coordenadas:
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
        tamanhos = []
        for partido in self.partidos:
            x.append(dados[partido.nome][0])
            y.append(dados[partido.nome][1])
            tamanhos.append(self.tamanhos_partidos[partido.nome])
        size = numpy.array(tamanhos) * escala * 3
        scatter(x, y, size, range(len(x)), marker='o', cmap=colormap_partidos) #, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, faceted=True, verts=None, hold=None, **kwargs)

        for partido in self.partidos:
            text(dados[partido.nome][0]+.005,dados[partido.nome][1],partido.numero,fontsize=12,stretch=100,alpha=1)

        show()

