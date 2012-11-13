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
from models import AnalisePeriodo as Modelo_AnalisePeriodo
from models import AnaliseTemporal as Modelo_AnaliseTemporal
from calendar import monthrange
import datetime
import logging
from hashlib import md5
import pdb        #pdb.set_trace()

logger = logging.getLogger("radar")

class AnalisePeriodo:

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
            logger.info('Lista de partidos nao foi especificada. Usando todos do universo.')
            self.partidos = models.Partido.objects.all()
        self.num_votacoes = len(self.votacoes)
        self.vetores_votacao = [] # { sao calculados por    
        self.vetores_presenca = []#   self._inicializa_vetores() 
        self.tamanhos_partidos = {} #  }
        self.pca_partido = None # É calculado por self._pca_partido()
        self.coordenadas = {}
        self.soma_dos_quadrados_dos_tamanhos_dos_partidos = 0

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

#    def _inicializa_tamanhos_partidos(self):
#        """Retorna um dicionário cuja chave é o nome do partido, e o valor é a quantidade de parlamentares do partido no banco.
#
#        Este dicionário é também salvo no atributo self.tamanho_partidos
#        """
#        self.tamanho_partidos = {}
#        self.soma_dos_quadrados_dos_tamanhos_dos_partidos = 0
#        for partido in self.partidos:
#            tamanho = len(models.Legislatura.objects.filter(partido=partido, casa_legislativa=self.casa_legislativa))
#            logger.info('init tamanhos PARTIDO: %s -%s , TAMANHO: %d ' % (partido.nome,partido.numero,tamanho))
#            self.tamanhos_partidos[partido.nome] = tamanho
#            self.soma_dos_quadrados_dos_tamanhos_dos_partidos += tamanho*tamanho
#        return self.tamanhos_partidos

    def _inicializa_vetores(self):
        """Cria os 'vetores de votação' para cada partido. 

        O 'vetor' usa um número entre -1 (não) e 1 (sim) para representar a "posição média"
        do partido em cada votação, tendo N dimensões correspondentes às N votações.
        Aproveita para calcular o tamanho dos partidos, presença dos parlamentares, etc.

        Retorna a 'matriz de votações', em que cada linha é um vetor de votações de um partido 
                A ordenação das linhas segue a ordem de self.partidos
        """

        # Inicializar matriz nula de vetores de votação e vetores presença
        self.vetores_votacao = numpy.zeros((len(self.partidos), self.num_votacoes))
        self.vetores_presenca = numpy.zeros((len(self.partidos), self.num_votacoes))
        # Inicializar dicionário de tamanhos dos partidos com valores nulos:
        self.tamanhos_partidos = {}
        for p in self.partidos:
            self.tamanhos_partidos[p.nome]=0
        # Inicializar um conjunto nulo de legislaturas que já foram vistas em votações anteriores:
        legislaturas_ja_vistas = []
        iv = -1
        for V in self.votacoes:
            iv += 1
            dic_partido_votos = {}
            votos_de_V = V.votos()
            for voto in votos_de_V:
                # colocar legislatura na lista de já vistas,
                # e somar um no tamanho do partido correspondente:
                if voto.legislatura not in legislaturas_ja_vistas:
                    legislaturas_ja_vistas.append(voto.legislatura)
                    self.tamanhos_partidos[voto.legislatura.partido.nome] += 1
                
                part = voto.legislatura.partido.nome
                if not dic_partido_votos.has_key(part):
                    dic_partido_votos[part] = models.VotoPartido(part) #cria um VotoPartido
                voto_partido = dic_partido_votos[part]
                voto_partido.add(voto.opcao) # preenche o VotoPartido criado
            # todos os votos da votacao V já estão em dic_partido_votos
            ip = -1  
            for p in self.partidos:
                ip += 1
                if dic_partido_votos.has_key(p.nome):
                    votoPartido = dic_partido_votos[p.nome] # models.VotoPartido
                    votoPartido_total = votoPartido.total()
                    if votoPartido_total > 0:
                        self.vetores_votacao[ip][iv] = (float(votoPartido.sim) - float(votoPartido.nao)) / float(votoPartido_total)
                    else:
                        self.vetores_votacao[ip][iv] = 0
                    self.vetores_presenca[ip][iv] = votoPartido_total
                else:
                    self.vetores_votacao[ip][iv] = 0
                    self.vetores_presenca[ip][iv] = 0
        # Calcular um valor proporcional à soma das áreas dos partidos, para usar 
        # no fator de escala de exibição do gráfico de bolhas:
        for p in self.partidos:
            stp = self.tamanhos_partidos.get(p.nome,0)
            self.soma_dos_quadrados_dos_tamanhos_dos_partidos += stp*stp
        return self.vetores_votacao

    def _pca_partido(self):
        """Roda a análise de componentes principais por partido.

        Guarda o resultado em self.pca
        Retorna um dicionário no qual as chaves são as siglas dos partidos
        e o valor de cada chave é um vetor com as n dimensões da análise pca
        """
        # Fazer pca, se ainda não foi feita:
        if not self.pca_partido:
            if self.vetores_votacao != None and len(self.vetores_votacao) > 0:
                self._inicializa_vetores()
            # Partidos de tamanho nulo devem ser excluidos da PCA:
            ipnn = [] # lista de indices dos partidos nao nulos
            ip = -1
            for p in self.partidos:
                ip += 1
                if self.tamanhos_partidos[p.nome] != 0:
                    ipnn.append(ip)
            
            matriz = self.vetores_votacao
            matriz = matriz[ipnn,:] # excluir partidos de tamanho zero
            # Centralizar dados:
            matriz = matriz - matriz.mean(axis=0)
            # Fazer pca:
            self.pca_partido = pca.PCA(matriz,fraction=1)
            # Recuperar partidos de tamanho nulo, atribuindo zero em
            # em todas as dimensões no espaço das componentes principais:
            U2 = self.pca_partido.U.copy() # Salvar resultado da pca em U2
            self.pca_partido.U = numpy.zeros((len(self.partidos), self.num_votacoes))
            ip = -1
            ipnn2 = -1
            for p in self.partidos:
                ip += 1
                if ip in ipnn: # Se este partido for um partido não nulo
                    ipnn2 += 1
                    cpmaximo = U2.shape[1]
                     # colocar nesta linha os valores que eu salvei antes em U2
                    self.pca_partido.U[ip,0:cpmaximo] = U2[ipnn2,:]
                else:
                    self.pca_partido.U[ip,:] = numpy.zeros((1,self.num_votacoes))
            logger.info("PCA terminada com sucesso. ini=%s, fim=%s" % (str(self.ini),str(self.fim)))

        # Criar dicionario a ser retornado:
        dicionario = {}
        for partido, vetor in zip(self.partidos, self.pca_partido.U):
            dicionario[partido.nome] = vetor
        return dicionario


    def partidos_2d(self):
        """Retorna mapa com as coordenadas dos partidos no plano 2D formado
        pelas duas primeiras componentes principais.

        A chave do mapa é o nome do partido (string) e o valor é uma lista 
        de duas posições [x,y].
        """

        self.coordenadas = self._pca_partido()
        if self.num_votacoes > 1:
            for partido in self.coordenadas.keys():
                self.coordenadas[partido] = (self.coordenadas[partido])[0:2]
        elif self.num_votacoes == 1: # se só tem 1 votação, só tem 1 C.P. Jogar tudo zero na segunda CP.
            for partido in self.coordenadas.keys():
                self.coordenadas[partido] = numpy.array([ (self.coordenadas[partido])[0] , 0. ])
        else: # Zero votações no período. Os partidos são todos iguais. Tudo zero.
            for partido in self.coordenadas.keys():
                self.coordenadas[partido] = numpy.array([ 0. , 0. ])
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
        dados_meus = self.partidos_2d() # calcula coordenadas, grava em self.coordenadas, e as retorna.
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

        self.coordenadas = dados_meus; # altera coordenadas originais da instância.
        print campeao
        return dados_meus
    
    def figura(self, escala=10):
        """Apresenta um plot de bolhas (usando matplotlib) com os partidos de tamanho maior ou igual a tamanho_min com o primeiro componente principal no eixo x e o segundo no eixo y.
        """

        #if not self.tamanhos_partidos:
        #    self._inicializa_tamanhos_partidos()

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


class AnaliseTemporal:
    """Um objeto da classe AnaliseTemporal é um envelope para um conjunto de
    objetos do tipo AnalisePeriodo.

    Uma análise de um período é uma análise de componentes principais dos
    votos de um dado período, por exemplo do ano de 2010. Para fazer um gráfico
    animado, é preciso fazer análises de dois ou mais períodos consecutivos, 
    por exemplo 2010, 2011 e 2012, e rotacionar adequadamente os resultados 
    para que os partidos globalmente caminhem o mínimo possível de um lado para
    o outro (vide algoritmo de rotação).

    data_inicio e data_fim: strings no formato 'aaaa-mm-dd'.

    A classe AnaliseTemporal tem métodos para criar os objetos AnalisePeriodo e
    fazer as análises.
    """
    def __init__(self, casa_legislativa,data_inicio=None, data_fim=None, periodicidade='semestral', votacoes=None, partidos=None):

        self.casa_legislativa = casa_legislativa

        self.ini = parse_datetime('%s 0:0:0' % data_inicio)
        self.fim = parse_datetime('%s 0:0:0' % data_fim)
        self.periodicidade = periodicidade

        self.votacoes = votacoes 
        # OBS: Se votacoes==None, a classe AnalisePeriodo usará 
        #      todas as votações disponíveis no período solicitado.

        self.partidos = partidos
        if not self.partidos:
            logger.info('Lista de partidos nao foi especificada. Usando todos do universo.')
            self.partidos = models.Partido.objects.all()
        self.area_total = 1
        self.analises_periodo = [] # lista de objetos da classe AnalisePeriodo
        self.periodos = [] # lista de tuplas (datetime de inicio,datetime de fim)

    def _faz_analises(self):
        """ Método da classe AnaliseTemporal que cria os objetos AnalisePeriodo e faz as análises.
        """
        # Inicializar periodos, que é a lista de pares ordenados 
        # com datas de inicio e fim de cada análise:
        if self.periodicidade == 'semestral':
            delta_mes = 5
        elif self.periodicidade == 'anual':
            delta_mes = 11
        elif self.periodicidade == 'trimestral':
            delta_mes = 3
        elif self.periodicidade == 'quadrimestral':
            delta_mes = 2
        else:
            logger.info("Periodicidade '%s' desconhecida. Usando periodicidade semestral (delta_mes=6).") % self.periodicidade
            delta_mes = 6
        dias_que_faltam = 1
        data_inicial = self.ini
        while dias_que_faltam > 0:
            mes = data_inicial.month
            ano = data_inicial.year
            mes = mes + delta_mes
            while mes > 12:
                mes = mes - 12
                ano = ano + 1
            data_final = data_inicial.replace(month=mes,year=ano)
            # ir ate ultimo dia do mes:
            dia_final = monthrange(data_final.year,data_final.month)[1]
            data_final = data_final.replace(day=dia_final)
            self.periodos.append((data_inicial,data_final))
            data_inicial = data_final + datetime.timedelta(days=1)
            delta_que_falta = self.fim - data_final
            dias_que_faltam = delta_que_falta.days

        # Fazer as análises:
        for datas in self.periodos:
            data_ini_str = datas[0].strftime('%Y-%m-%d')
            data_fim_str = datas[1].strftime('%Y-%m-%d')
            # inicializa objeto AnalisePeriodo
            x = AnalisePeriodo(self.casa_legislativa, data_inicio=data_ini_str, data_fim=data_fim_str, votacoes=self.votacoes, partidos=self.partidos)
            # Pede as coordenadas 2d, o que efetivamente fará o cálculo ser feito:
            x.partidos_2d()
            # Coloca esta análise na lista de análises
            self.analises_periodo.append(x)
            
        # Rotacionar as análises, e determinar área máxima:
        maior = self.analises_periodo[0].soma_dos_quadrados_dos_tamanhos_dos_partidos
        for i in range(1,len(self.analises_periodo)): # a partir da segunda analise
            # Rotacionar/espelhar a análise baseado na análise anterior
            self.analises_periodo[i].espelha_ou_roda(self.analises_periodo[i-1].coordenadas)
            # Área Máxima:
            candidato = self.analises_periodo[i].soma_dos_quadrados_dos_tamanhos_dos_partidos
            if candidato > maior:
                maior = candidato
        self.area_total = maior
            
    def salvar_no_bd(self):
        """Salva uma instância de AnaliseTemporal no banco de dados."""
        # 'modat' é o modelo análise temporal que vou salvar.
        modat = Modelo_AnaliseTemporal()
        modat.casa_legislativa = self.casa_legislativa
        modat.periodicidade = self.periodicidade
        modat.data_inicio = self.ini
        modat.data_fim = self.fim
        modat.votacoes = self.votacoes
        modat.partidos = self.partidos
        modat.area_total = self.area_total
        # Criar um hash para servir de primary key desta análise temporal:
        hash_id = md5()
        hash_id.update(str(self.casa_legislativa))
        hash_id.update(self.periodicidade)
        hash_id.update(str(self.ini))
        hash_id.update(str(self.fim))
        hash_id.update(str(self.votacoes)) # talvez nao sirva
        hash_id.update(str(self.partidos)) # talvez nao sirva
        modat.hash_id = hash_id.hexdigest()
        # Salvar no bd, ainda sem as análises
        modat.save()
        # Salvar as análises por período no bd:
        for ap in self.analises_periodo:
            modap = Modelo_AnalisePeriodo()
            modap.casa_legislativa = ap.casa_legislativa
            modap.data_inicio = ap.ini.strftime('%Y-%m-%d')
            modap.data_fim = ap.fim.strftime('%Y-%m-%d')
            #votacoes = self.votacoes
            #partidos = self.partidos
            modap.analiseTemporal = self
            posicoes = []
            for part, coord in ap.coordenadas.items():
                posicao = PosicaoPartido() # Cria PosicaoPartido no bd
                posicao.x = coord[0]
                posicao.y = coord[1]
                posicao.partido = models.Partido.objects.filter(nome=part)[0]
                posicao.save() # Salva PosicaoPartido no bd
                posicoes.append(posicao)
            modap.posicoes = posicoes
            modap.save() # Salva a análise do período no bd, associada a uma AnaliseTemporal

class JsonAnaliseGenerator:

    def get_json(self, casa_legislativa):
        """Retorna JSON tipo {periodo:{nomePartido:{numPartido:1, tamanhoPartido:1, x:1, y:1}}"""

        analise = AnaliseTemporal(casa_legislativa, data_inicio='2010-07-01', data_fim='2011-06-30', periodicidade='semestral', votacoes=None, partidos=None)
        
        # TODO: nao fazer análise se já estiver no bd,
        #       e se tiver que fazer, salvar no bd (usando metodo analiseTemporal.salvar_no_bd())
        analise._faz_analises()

        # Usar mesma escala para os tamanhos dos partidos em todas as análises
        soma_quad_tam_part_max = 0
        for ap in analise.analises_periodo:
            candidato = ap.soma_dos_quadrados_dos_tamanhos_dos_partidos
            if candidato > soma_quad_tam_part_max:
                soma_quad_tam_part_max = candidato

        fator_de_escala_de_tamanho = 4000 # Ajustar esta constante para mudar o tamanho dos circulos
        escala_de_tamanho = fator_de_escala_de_tamanho / numpy.sqrt(soma_quad_tam_part_max)
        
        i = 0
        json = '{'
        for per in analise.periodos:
            json += '%s:%s ' % (str(i+1000), self._json_ano(analise.analises_periodo[i],escala_de_tamanho))
            i += 1
        json = json.rstrip(', ')
        json += '}'
        return json

    def _json_ano(self, analise,escala_de_tamanho):
        json = '{'
        for part in analise.coordenadas:
            nome_partido = part
            tamanho = analise.tamanhos_partidos[part]
            tamanho =  tamanho * escala_de_tamanho
            tamanho = int(tamanho)
            num = models.Partido.objects.get(nome=nome_partido).numero
            x = round(analise.coordenadas[part][0], 2)
            y = round(analise.coordenadas[part][1], 2)            
            json += '"%s":{"numPartido":%s, "tamanhoPartido":%s, "x":%s, "y":%s}, ' % (nome_partido, num, tamanho, x, y)
            #logger.info('PARTIDO: %s , (%s,%s), TAMANHO: %s' % (nome_partido,x,y,tamanho))
        json = json.rstrip(', ')
        json += '}, '
        return json




