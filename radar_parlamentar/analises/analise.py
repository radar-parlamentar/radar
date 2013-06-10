# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Saulo Trento, Diego Rabatone, Guilherme Januário
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

"""Módulo analise"""

from __future__ import unicode_literals
from hashlib import md5
from math import hypot, atan2, pi
from models import AnalisePeriodo, AnaliseTemporal, PosicaoPartido, JsonAnaliseTemporal
from modelagem import models
import grafico
import logging
import numpy
import pca
import json

logger = logging.getLogger("radar")

class AnalisadorPeriodo:

    def __init__(self, casa_legislativa, periodo=None, votacoes=None, partidos=None):
        """Argumentos:
            casa_legislativa -- objeto do tipo CasaLegislativa; somente votações desta casa serão analisados.
            data_inicio e data_fim -- são strings no formato aaaa-mm-dd;
            Se este argumentos não são passadas, a análise é feita sobre todas as votações
            periodo -- objeto do tipo PeriodoCasaLegislativa
            votacoes -- lista de objetos do tipo Votacao para serem usados na análise
                        se não for especificado, procura votações na base de dados de acordo data_inicio e data_fim.
            partidos -- lista de objetos do tipo Partido para serem usados na análise;
                        se não for especificado, usa todos os partidos no banco de dados.
        """

        self.casa_legislativa = casa_legislativa
        self.periodo = periodo
        if (periodo != None):
            self.ini = periodo.ini
            self.fim = periodo.fim
        else:
            self.ini = None
            self.fim = None
            
        self.partidos = partidos
        if not partidos:
            self.partidos = self.casa_legislativa.partidos()

        self.votacoes = votacoes
        if not self.votacoes: 
            self.votacoes = self._inicializa_votacoes(self.casa_legislativa, self.ini, self.fim)

        # TODO que acontece se algum partido for ausente neste período?
        self.num_votacoes = len(self.votacoes)
        self.vetores_votacao = [] # { sao calculados por    
        self.vetores_presenca = []#   self._inicializa_vetores() 
        self.tamanhos_partidos = {} # 
        self.presencas_partidos = {} # }
        self.pca_partido = None # É calculado por self._pca_partido()
        self.coordenadas = {}
        self.soma_dos_tamanhos_dos_partidos = 0
        self.analise_ja_feita = False # quando a analise for feita, vale True.
        self.theta = 0 # em graus, eventual rotação feita por self.espelha_ou_roda()

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
        self.presencas_partidos = {}
        for p in self.partidos:
            self.tamanhos_partidos[p.nome]=0
            self.presencas_partidos[p.nome]=0
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
        # no fator de escala de exibição do gráfico de bolhas. Calcular também o
        # dicionário de presenças:
        ip = -1
        for p in self.partidos:
            ip += 1
            stp = self.tamanhos_partidos.get(p.nome,0)
            self.soma_dos_tamanhos_dos_partidos += stp
            if stp == 0: # partido de tamanho zero tem presenca zero
                self.presencas_partidos[p.nome] = 0
            else:
                self.presencas_partidos[p.nome] = numpy.mean(self.vetores_presenca[ip])/stp # presenca média, valor entre 0 e 1.
        return self.vetores_votacao

    def _pca_partido(self):
        """Roda a análise de componentes principais por partido.

        Guarda o resultado em self.pca
        Retorna um dicionário no qual as chaves são as siglas dos partidos
        e o valor de cada chave é um vetor com as n dimensões da análise pca
        """
        # Fazer pca, se ainda não foi feita:
        if not self.pca_partido:
            if self.vetores_votacao == None or len(self.vetores_votacao) == 0:
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
        pelas duas primeiras componentes principais. Para isso é preciso
        fazer uma análise de componentes principais (pca); se esta já tiver
        sido feita, o método apenas retorna o resultado já previamente salvo
        na variável self.coordenadas. Caso contrário a análise é feita.

        A chave do mapa é o nome do partido (string) e o valor é uma lista 
        de duas posições [x,y].
        """
        if not self.analise_ja_feita: # A análise pca ainda tem que ser feita.
            self.coordenadas = self._pca_partido() # Fazer análise pca.
            if self.num_votacoes > 1:
                for partido in self.coordenadas.keys():
                    self.coordenadas[partido] = (self.coordenadas[partido])[0:2]
            elif self.num_votacoes == 1: # se só tem 1 votação, só tem 1 C.P. Jogar tudo zero na segunda CP.
                for partido in self.coordenadas.keys():
                    self.coordenadas[partido] = [(self.coordenadas[partido])[0], 0.]
            else: # Zero votações no período. Os partidos são todos iguais. Tudo zero.
                for partido in self.coordenadas.keys():
                    self.coordenadas[partido] = [ 0. , 0. ]
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
        self.theta = campeao[1]
        print campeao
        return dados_meus

class AnalisadorTemporal:
    """Um objeto da classe AnalisadorTemporal é um envelope para um conjunto de
    objetos do tipo AnalisadorPeriodo.

    Uma análise de um período é uma análise de componentes principais dos
    votos de um dado período, por exemplo do ano de 2010. Para fazer um gráfico
    animado, é preciso fazer análises de dois ou mais períodos consecutivos, 
    por exemplo 2010, 2011 e 2012, e rotacionar adequadamente os resultados 
    para que os partidos globalmente caminhem o mínimo possível de um lado para
    o outro (vide algoritmo de rotação).

    A classe AnalisadorTemporal tem métodos para criar os objetos AnalisadorPeriodo e
    fazer as análises.

    Atributos:
        data_inicio e data_fim -- strings no formato 'aaaa-mm-dd'.
        analisadores_periodo -- lista de objetos da classe AnalisadorPeriodo

    """
    def __init__(self, casa_legislativa, periodicidade=models.BIENIO, votacoes=[]):

        self.casa_legislativa = casa_legislativa
        self.periodos = self.casa_legislativa.periodos(periodicidade)
        self.ini = self.periodos[0].ini
        self.fim = self.periodos[len(self.periodos)-1].fim
        self.periodicidade = periodicidade
        self.area_total = 1
        self.analisadores_periodo = [] # lista de objetos da classe AnalisadorPeriodo
        self.votacoes = votacoes
        self.partidos = []
        self.json = ""

    def _calcula_hash(self):
        hash_id = md5()
        hash_id.update(str(self.casa_legislativa))
        hash_id.update(self.periodicidade)
        hash_id.update(str(self.ini))
        hash_id.update(str(self.fim))
        hash_id.update(str(self.votacoes)) # talvez nao sirva
        hash_id.update(str(self.partidos)) # talvez nao sirva
        self.hash_id = hash_id.hexdigest()
        return self.hash_id

    def get_json(self):
        # Calcular o hash md5 da análise solicitada para ver se já está no bd
        self.hash_id = self._calcula_hash()
        logger.info("hash_id desta análise temporal é %s." % self.hash_id)
        logger.info("casa legislativa é %s" % self.casa_legislativa)
        json_do_bd = JsonAnaliseTemporal.objects.filter(hash_id__exact=self.hash_id)
        if len(json_do_bd) == 0:
            logger.info("Análises serão feitas (json ainda não existe no BD).")
            self._faz_analises()
            self._cria_json()
            self._salvar_json_no_bd()
            logger.info("Json da análise salvo no BD.")
            return self.json
        else:
            logger.info("Análises já existem, json recuperado do BD.")
            return json_do_bd[0].json

    #deprecated (serve para o json antigo funcionar)
    def get_analises(self):
        """ Método que deve ser usado por classes exteriores para acessar os dados desta instância. Este método irá verificar se a análise já foi feita e está disponível no banco de dados. Se não estiver, os cálculos são realizados, e a análise é salva no bd.
        Este método poderá ser apagado quando o json antigo não for mais usado (ou seja, quando o método get_json da classe JsonAnaliseGenerator do módulo gráfico não for mais usado)."""
        # Calcular o hash md5 da análise solicitada para ver se já está no bd
        self.hash_id = self._calcula_hash()
        logger.info("hash_id desta análise temporal é %s." % self.hash_id)
        logger.info("casa legislativa é %s" % self.casa_legislativa)
        analiseT_do_bd = AnaliseTemporal.objects.filter(hash_id__exact=self.hash_id)
        if len(analiseT_do_bd) == 0:
            logger.info("Análises serão feitas (ainda não existem no BD).")
            self._faz_analises()
            self.salvar_no_bd()
            logger.info("Análises salvas no BD.")
        else:
            logger.info("Análises já existem.")
            # criar lista de analisadores_periodo com dicionarios de coordenadas.
            if len(self.votacoes) == 0:
                votacoes = None
            else:
                votacoes = self.votacoes
            if len(self.partidos) == 0:
                partidos = None
            else:
                partidos = self.partidos
            analiseT_do_bd = analiseT_do_bd[0]
            self.area_total = analiseT_do_bd.area_total
            self.area_total = analiseT_do_bd.area_total
            for ap_do_bd in analiseT_do_bd.analiseperiodo_set.all():
                periodocl = models.PeriodoCasaLegislativa(ap_do_bd.data_inicio,ap_do_bd.data_fim)
                ap = AnalisadorPeriodo(self.casa_legislativa, periodocl,votacoes,partidos)
                ap.analise_ja_feita = True # nao quero que faça analise, pois os dados virão do bd.
                for pos_do_bd in ap_do_bd.posicoes.all():
                    ap.coordenadas[pos_do_bd.partido.nome] = (pos_do_bd.x,pos_do_bd.y)
                    ap.tamanhos_partidos[pos_do_bd.partido.nome] = (pos_do_bd.tamanho)
                    # TODO: acrescentar presença.
                self.analisadores_periodo.append(ap)
            logger.info("analise baixada do bd")
            
    def _faz_analises(self):
        """ Método da classe AnalisadorTemporal que cria os objetos AnalisadorPeriodo e faz as análises."""
        for periodo in self.periodos:
            logger.info("Analisando periodo %s a %s." % (str(periodo.ini),str(periodo.fim)) )
            if len(self.votacoes) == 0: # FUNFA?
                votacoes = None
            else:
                votacoes = self.votacoes
            if len(self.partidos) == 0: # FUNFA?
                partidos = None
            else:
                partidos = self.partidos
            x = AnalisadorPeriodo(self.casa_legislativa, periodo, votacoes, partidos)
            if x.votacoes:
                logger.info("O periodo possui %d votações." % len(x.votacoes))
                x.partidos_2d()
                self.analisadores_periodo.append(x)
            else:
                logger.info("O periodo não possui nenhuma votação.")
            logger.info("Soma dos Tamanhos dos Partidos %f" % x.soma_dos_tamanhos_dos_partidos)

        # Rotacionar as análises, e determinar área máxima:
        maior = self.analisadores_periodo[0].soma_dos_tamanhos_dos_partidos
        for i in range(1,len(self.analisadores_periodo)): # a partir da segunda analise
            # Rotacionar/espelhar a análise baseado na análise anterior
            self.analisadores_periodo[i].espelha_ou_roda(self.analisadores_periodo[i-1].coordenadas)
            # Área Máxima:
            candidato = self.analisadores_periodo[i].soma_dos_tamanhos_dos_partidos
            if candidato > maior:
                maior = candidato
        self.area_total = maior
       
    def _cria_json(self,constante_escala_tamanho=45):
        """Uma vez que a análise temporal está feita, este método cria o json. """

        self.json = '{"geral":{"CasaLegislativa":{'
        self.json += '"nome":"' + self.casa_legislativa.nome + '",'
        self.json += '"nome_curto":"' + self.casa_legislativa.nome_curto + '",'
        self.json += '"esfera":"' + self.casa_legislativa.esfera + '",'
        self.json += '"local":"' + self.casa_legislativa.local + '",'
        self.json += '"atualizacao":"' + unicode(self.casa_legislativa.atualizacao) + '"'
        self.json += "}," # fecha casa legislativa
        escala = constante_escala_tamanho**2 / max(1,self.area_total)
        escala_20px = 20**2 * (1/escala) # numero de parlamentares representado
                                         # por um circulo de raio 20 pixels.
        self.json += '"escala_tamanho":' + str(round(escala_20px,1)) + ','
        self.json += '"filtro_partidos":null,'
        self.json += '"filtro_votacoes":null},' # fecha bloco "geral"
        self.json += '"periodos":['
        for ap in self.analisadores_periodo:
            self.json += '{' # abre periodo
            self.json += '"nvotacoes":' + str(ap.periodo.quantidade_votacoes) + ','
            self.json += '"nome":"' + ap.periodo.string + '",'
            var_explicada = round((ap.pca_partido.eigen[0] + ap.pca_partido.eigen[1])/ap.pca_partido.eigen.sum() * 100,1)
            self.json += '"var_explicada":' + str(var_explicada) + ","
            self.json += '"cp1":{"theta":' + str(round(ap.theta,0)%180) + ','
            var_explicada = round(ap.pca_partido.eigen[0]/ap.pca_partido.eigen.sum() * 100,1)
            self.json += '"var_explicada":' + str(var_explicada) + ","
            self.json += '"composicao":' + str([round(el,2) for el in 100*ap.pca_partido.Vt[0,:]**2]) + "}," # fecha cp1
            self.json += '"cp2":{"theta":' + str(round(ap.theta,0)%180 + 90) + ','
            var_explicada = str(round(ap.pca_partido.eigen[1]/ap.pca_partido.eigen.sum() * 100,1))
            self.json += '"var_explicada":' + str(var_explicada) + ","
            self.json += '"composicao":' + str([round(el,2) for el in 100*ap.pca_partido.Vt[1,:]**2]) + "}," # fecha cp2
            self.json += '"votacoes":' # deve trazer a lista de votacoes do periodo
                                       # na mesma ordem apresentada nos vetores
                                       # composicao das componentes principais.
            lista_votacoes = []
            for votacao in ap.votacoes:
                lista_votacoes.append({"id":unicode(votacao).replace('"',"'")})
            self.json += json.dumps(lista_votacoes)
            self.json += ' },' # fecha lista de votações e fecha período
        self.json = self.json[0:-1] # apaga última vírgula
        self.json += '],' # fecha lista de períodos
        self.json += '"partidos":['
        parts = []
        for partido in self.casa_legislativa.partidos():
            dict_partido = {"nome":partido.nome ,"numero":partido.numero,"cor":grafico.CorPartido.cor(partido)}
            dict_partido["t"] =  []
            dict_partido["r"] =  []
            dict_partido["x"] =  []
            dict_partido["y"] =  []
            dict_partido["p"] =  []
            for ap in self.analisadores_periodo:
                scaler = grafico.GraphScaler()
                mapa = scaler.scale(ap.coordenadas)
                dict_partido["x"].append(round(mapa[partido.nome][0],2))
                dict_partido["y"].append(round(mapa[partido.nome][1],2))
                t = ap.tamanhos_partidos[partido.nome]
                dict_partido["t"].append(t)
                r = numpy.sqrt(t*escala)
                dict_partido["r"].append(round(r,1))
                p = ap.presencas_partidos[partido.nome] * 100
                dict_partido["p"].append(round(p,1))
                dict_partido["parlamentares"]=None
            self.json += json.dumps(dict_partido) + ','
        self.json = self.json[0:-1] # apaga última vírgula
        self.json += '] }' # fecha lista de partidos e fecha json


    def _salvar_json_no_bd(self):
        """Salva o resultado de um AnalisadorTemporal no banco de dados como json.

        Este método poderá ser excluído quando o json antigo não for mais usado."""
        json_bd = JsonAnaliseTemporal()
        json_bd.hash_id = self._calcula_hash()
        json_bd.casa_legislativa = self.casa_legislativa
        json_bd.periodicidade = self.periodicidade
        json_bd.data_inicio = self.ini
        json_bd.data_fim = self.fim
        json_bd.votacoes = self.votacoes
        json_bd.partidos = self.partidos
        json_bd.json = self.json
        json_bd.save()

    #deprecated (serve para o json antigo funcionar)
    def salvar_no_bd(self):
        """Salva uma instância de AnalisadorTemporal no banco de dados.

        Este método poderá ser excluído quando o json antigo não for mais usado."""
        # 'modat' é o modelo análise temporal que vou salvar.
        modat = AnaliseTemporal()
        modat.casa_legislativa = self.casa_legislativa
        modat.periodicidade = self.periodicidade
        modat.data_inicio = self.ini
        modat.data_fim = self.fim
        modat.votacoes = self.votacoes
        modat.partidos = self.partidos
        modat.area_total = self.area_total
        # Criar um hash para servir de primary key desta análise temporal:
        modat.hash_id = self._calcula_hash()
        # Salvar no bd, ainda sem as análises
        modat.save()
        # Salvar as análises por período no bd:
        for ap in self.analisadores_periodo:
            modap = AnalisePeriodo()
            modap.casa_legislativa = ap.casa_legislativa
            modap.data_inicio = ap.ini.strftime('%Y-%m-%d')
            modap.data_fim = ap.fim.strftime('%Y-%m-%d')
            #votacoes = self.votacoes
            #partidos = self.partidos
            modap.analiseTemporal = modat
            posicoes = []
            for part, coord in ap.coordenadas.items():
                posicao = PosicaoPartido() # Cria PosicaoPartido no bd
                posicao.x = coord[0]
                posicao.y = coord[1]
                posicao.partido = models.Partido.objects.filter(nome=part)[0]
                posicao.tamanho = ap.tamanhos_partidos.get(part,0)
                posicao.presenca = 0 # TODO: incluir presença aqui.
                posicao.save() # Salva PosicaoPartido no bd
                posicoes.append(posicao)
            modap.save()
            modap.posicoes = posicoes
            modap.save() # Salva a análise do período no bd, associada a uma AnalisadorTemporal





