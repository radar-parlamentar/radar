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
from modelagem import models
from matplotlib.pyplot import figure, show, scatter, text
import matplotlib.colors
from math import hypot, atan2, pi
from models import PosicaoPartido
from models import PeriodoAnalise
import logging

logger = logging.getLogger("radar")

class Analise:

    def __init__(self, casa_legislativa, data_inicio=None, data_fim=None, votacoes=None, partidos=None):
        """Argumentos:
            casa_legislativa -- objeto do tipo CasaLegislativa; somente votações desta casa serão analisados.
            data_inicio e data_fim -- são strings no formato aaaa-mm-dd;
            Se este argumentos não são passadas, a análise é feita sobre todas as votações
            votacoes -- lista de objetos do tipo Votacao para serem usados na análise
                        se não for especificado, procura votações na base de dados de acordo data_inicio e data_fim.
            partidos -- lista de objetos do tipo Partido para serem usados na análise;
                        se não for especificado, usa todos os partidos no banco de dados.
        """

        self.casa_legislativa = casa_legislativa

        self.ini = parse_datetime('%s 0:0:0' % data_inicio)
        self.fim = parse_datetime('%s 0:0:0' % data_fim)

        self.votacoes = votacoes
        if not self.votacoes: 
            self.votacoes = self._inicializa_votacoes(self.casa_legislativa, self.ini, self.fim)

        # TODO que acontece se algum partido for ausente neste período?

        self.partidos = partidos
        if not self.partidos:
            self.partidos = models.Partido.objects.all()
        self.num_votacoes = len(self.votacoes)
        self.vetores_votacao = []
        self.pca_partido = []
        self.coordenadas = {}
        self.tamanhos_partidos = {}

    def _inicializa_votacoes(self, casa, ini, fim):
        """Pega votações do banco de dados
    
        Argumentos:
            casa -- obejto do tipo CasaLegislativa
            ini, fim -- objetos do tipo datetime

        Retorna lista de votações
        """

        if ini == None and fim == None:
            votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=casa) 
        if ini == None and fim != None:
            votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=casa).filter(data__lte=fim)
        if ini != None and fim == None:
            votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=casa).filter(data__gte=ini)
        if ini != None and fim != None:
            votacoes = models.Votacao.objects.filter(proposicao__casa_legislativa=casa).filter(data__gte=ini, data__lte=fim)
        return votacoes

    def _inicializa_tamanhos_partidos(self):
        """Retorna um dicionário cuja chave é o nome do partido, e o valor é a quantidade de parlamentares do partido no banco.

        Este dicionário é também salvo no atributo self.mapa_tamanho_partidos
        """
        self.tamanho_partidos = {}
        for partido in self.partidos:
            tamanho = len(models.Legislatura.objects.filter(partido=partido, casa_legislativa=self.casa_legislativa))
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

        iv =-1
        for v in self.votacoes:
            iv += 1
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
        """Roda a análise de componentes principais por partido.

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


    def _energia(self,dados_fixos,dados_meus,graus=0,espelho=0):
        """Calcula energia envolvida no movimento entre dois instantes (fixo e meu), onde o meu é rodado (entre 0 e 360 graus), e primeiro eixo multiplicado por -1 se espelho=1. Ver pdf intitulado "Solução Analítica para o Problema de Rotação dos Eixos de Representação dos Partidos no Radar Parlamentar" (algoritmo_rotacao.pdf).
        """
        e = 0
        dados_meus = dados_meus.copy()
        if espelho == 1:
            for partido, coords in dados_meus.items():
                dados_meus[partido] = numpy.dot( coords,numpy.array( [[-1.,0.],[0.,1.]] ) )
        if graus != 0:
            for partido, coords in dados_meus.items():
                dados_meus[partido] = numpy.dot( coords,self._matrot(graus) )

        for p in self.partidos:
            e += numpy.dot( dados_fixos[p.nome] - dados_meus[p.nome],  dados_fixos[p.nome] - dados_meus[p.nome] ) * self.tamanhos_partidos[p.nome]
        return e

    def _polar(self,x, y, deg=0):		# radian if deg=0; degree if deg=1
        """
        Convert from rectangular (x,y) to polar (r,w)
        r = sqrt(x^2 + y^2)
        w = arctan(y/x) = [-\pi,\pi] = [-180,180]
        """
        if deg:
            return hypot(x, y), 180.0 * atan2(y, x) / pi
        else:
            return hypot(x, y), atan2(y, x)
    
    def _matrot(self,graus):
        """ Retorna matriz de rotação 2x2 que roda os eixos em graus (0 a 360) no sentido anti-horário (como se os pontos girassem no sentido horário em torno de eixos fixos).
        """ 
        graus = float(graus)
        rad = numpy.pi * graus/180.
        c = numpy.cos(rad)
        s = numpy.sin(rad)
        return numpy.array([[c,-s],[s,c]])

    def espelha_ou_roda(self, dados_fixos):
        print ' '
        print 'Espelhando e rotacionando...'
        epsilon = 0.001
        dados_meus = self.partidos_2d()
        if not self.tamanhos_partidos:
            self._inicializa_tamanhos_partidos()

        numerador = 0;
        denominador = 0;
        for partido, coords in dados_meus.items():
            meu_polar = self._polar(coords[0],coords[1],0)
            alheio_polar = self._polar(dados_fixos[partido][0],dados_fixos[partido][1],0)
            numerador += self.tamanhos_partidos[partido] * meu_polar[0] * alheio_polar[0] * numpy.sin(alheio_polar[1])
            denominador += self.tamanhos_partidos[partido] * meu_polar[0] * alheio_polar[0] * numpy.cos(alheio_polar[1])
        if denominador < epsilon and denominador > -epsilon:
            teta1 = 90
            teta2 = 270
        else:
            teta1 = numpy.arctan(numerador/denominador) * 180 / 3.141592
            teta2 = teta1 + 180

        ex = numpy.array([self._energia(dados_fixos,dados_meus,graus=teta1,espelho=0),self._energia(dados_fixos,dados_meus,graus=teta2,espelho=0),self._energia(dados_fixos,dados_meus,graus=teta1,espelho=1), self._energia(dados_fixos,dados_meus,graus=teta2,espelho=1) ])
        print ex
        
        ganhou = ex.argmin()
        campeao = [0,0]
        if ganhou >= 2: # espelhar
            campeao[0] = 1
            for partido, coords in dados_meus.items():
                dados_meus[partido] = numpy.dot( coords, numpy.array([[-1.,0.],[0.,1.]]) )
        if ganhou == 0 or ganhou == 2: # girar de teta1
            campeao[1] = teta1
        else:
            campeao[1] = teta2
        for partido, coords in dados_meus.items():
            dados_meus[partido] = numpy.dot( coords, self._matrot(campeao[1]) )

        print campeao
        return dados_meus

    def _quantidade_movimento(self,dados_alheios,dados_meus,graus=0,espelho=0): # deprecated
        """Calcula quantidade de movimento entre o instante i (corresponde ao ano anos[i]) e o instante i+1.
        No cálculo o instante i tem os eixos rotacionados (valor graus, entre 0 e 360), e o primeiro eixo multiplicado por -1 se espelho=1.
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

    def espelha_ou_roda_qm(self, dados_alheios): # deprecated
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
                qm_agora = self._quantidade_movimento(dados_alheios,dados_meus,graus,espelhar)
                #print '%d, %d, %f' % (espelhar,graus,qm_agora )
                if qm_agora < qm_min:
                    campeao = (espelhar, graus)
                    qm_min = qm_agora
        print campeao
        if campeao[0] == 1: # espelhar
            for partido, coords in dados_meus.items():
                dados_meus[partido] = numpy.dot( coords, numpy.array([[-1.,0.],[0.,1.]]) )
        if campeao[1] != 0: # rotacionar
            for partido, coords in dados_meus.items():
                dados_meus[partido] = numpy.dot( coords, self._matrot(campeao[1]) )
        return dados_meus

    
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

        fig.add_subplot(111, autoscale_on=True) #, xlim=(-1,5), ylim=(-5,3))
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


class JsonAnaliseGenerator:

    def get_json(self, casa_legislativa):
        """Retorna JSON tipo {periodo:{nomePartido:{numPartido:1, tamanhoPartido:1, x:1, y:1}}"""
    
        periodos = self._faz_analises(casa_legislativa)
    
        analise = Analise(casa_legislativa)
        analise._inicializa_tamanhos_partidos()
    
        i = 0
        json = '{'
        for pa in periodos:
            json += '%s:%s ' % (pa.periodo, self._json_ano(pa.posicoes, analise))
            i += 1
        json = json.rstrip(', ')
        json += '}'
    
        return json
    
    def _json_ano(self, posicoes, analise):
    
        json = '{'
        for posicao in posicoes.all():
            nome_partido = posicao.partido.nome
            num = posicao.partido.numero
            tamanho = 1 # analise.tamanhos_partidos[posicao.partido.nome] Issue #44
            x = round(posicao.x, 2)
            y = round(posicao.y, 2)
            json += '"%s":{"numPartido":%s, "tamanhoPartido":%s, "x":%s, "y":%s}, ' % (nome_partido, num, tamanho, x, y)
        json = json.rstrip(', ')
        json += '}, '
        return json
    
    def _faz_analises(self, casa):
        """casa -- objeto do tipo CasaLegislativa"""
        
        if not PeriodoAnalise.objects.filter(casa_legislativa=casa): # Se a análise nunca foi feita, fazer e salvar no bd.
            a20102 = Analise(casa, None, '2011-01-01')
            a20111 = Analise(casa, '2011-01-02', '2011-07-01')
            a20112 = Analise(casa, '2011-07-02', '2012-01-01')
            a20121 = Analise(casa, '2011-01-02', None)
            analises = [a20111, a20112, a20121]
            a20102.partidos_2d()
            coadunados = [a20102.coordenadas]
            for a in analises:
                a.partidos_2d()
                coadunados.append(a.espelha_ou_roda(coadunados[-1])) # rodar o mais novo, minimizando energia
            a2010 = self._to_periodo_analise(coadunados[0], '20102', casa)
            a2011a = self._to_periodo_analise(coadunados[1], '20111', casa)
            a2011b = self._to_periodo_analise(coadunados[2], '20112', casa)
            a2012 = self._to_periodo_analise(coadunados[3], '20121', casa)
            return [a2010, a2011a, a2011b, a2012]
        else: # buscar análise já feita que foi salva no banco de dados.
            a2010 = PeriodoAnalise.objects.filter(periodo='20102', casa_legislativa=casa)[0]
            a2011a = PeriodoAnalise.objects.filter(periodo='20111', casa_legislativa=casa)[0]
            a2011b = PeriodoAnalise.objects.filter(periodo='20112', casa_legislativa=casa)[0]
            a2012 = PeriodoAnalise.objects.filter(periodo='20121', casa_legislativa=casa)[0]
            return [a2010, a2011a, a2011b, a2012]
        
    def _to_periodo_analise(self, coordenadas, periodo, casa):
    
        pa = PeriodoAnalise()
        pa.periodo = periodo
        pa.save()
        pa.casa_legislativa = casa
        posicoes = []
        for part, coord in coordenadas.items():
            posicao = PosicaoPartido()
            posicao.x = coord[0]
            posicao.y = coord[1]
            partido = models.Partido.objects.filter(nome=part)[0]
            posicao.partido = partido
            posicao.save()
            posicoes.append(posicao)
        pa.posicoes = posicoes
        pa.save()
        return pa




