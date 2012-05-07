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

# TODO: Transformar este script em uma função
#       Investigar se é possível escolher a cor das bolhas.

import numpy
import analise
import sys

############################# 
## PARAMETROS MODIFICÁVEIS ##
############################# 

# Partidos a serem incluídos nas análises:
parts = [u'PMDB', u'PTB', u'PDT', u'PT', u'DEM', u'PCdoB', u'PSB', u'PSDB', u'PSC', u'PMN', u'PPS', u'PV', u'PTdoB', u'PP', u'PHS', u'PRB', u'PSOL', u'PR', u'PSD']

ano_inicial = 2002
ano_final = 2011

arquivo_de_saida = 'colar_num_html.txt'


############################# 
##  Programa em si:        ##
############################# 

anuais = [] # lista de objetos do tipo Analise (que serão análises anuais)

anos = range(ano_inicial,ano_final+1)

# Fazer as PCAs:
for ano in anos:
    anuais.append(analise.Analise(str(ano)+'-01-01', str(ano)+'-12-31', [], parts))

dados = []
print "Fazendo PCAs:"
print '-'*(len(anuais)-1)+'v'
for a in anuais:
    dados.append( a.partidos_2d('/dev/null') )
    sys.stdout.write('.')
    sys.stdout.flush()



# Funções auxiliares:
def quantidade_movimento(i,graus=0,espelho=0):
    """Calcula quantidade de movimento entre o instante i (corresponde ao ano anos[i]) e o instante i+1.
    No cálculo o instante i tem os eixos rotacionados (valor graus, entre 0 e 360), e o primeiro eixo multiplicado por -1 se espelho=0.
    """
    qm = 0
    antes = dados[i]
    depois = dados[i+1]
    if espelho:
        antes = numpy.dot( antes,numpy.array( [[-1.,0.],[0.,1.]] ) )
    if graus != 0:
        antes = numpy.dot( antes,matrot(graus) )
    for j in range(len(parts)):
        qm += numpy.sqrt( numpy.dot( antes[j,:] - depois[j,:],  antes[j,:] - depois[j,:] ) ) * anuais[i+1].tamanho_partido[j]
    return qm

def matrot(graus):
   """ Retorna matriz de rotação 2x2 que roda os eixos em graus (0 a 360) no sentido anti-horário (como se os pontos girassem no sentido horário em torno de eixos fixos).
   """ 
   graus = float(graus)
   rad = numpy.pi * graus/180.
   c = numpy.cos(rad)
   s = numpy.sin(rad)
   return numpy.array([[c,-s],[s,c]])


print ' '
print 'Espelhando e rotacionando...'
# Rodar e espelhar eixos conforme a necessidade:
# O sentido dos eixos que resultam na PCA é arbitrário, e se não dermos tanta importância ao significado do eixo x e do eixo y, mas sim principalmente à distância entre os partidos dois a dois que se reflete no plano, a rotação dos eixos é também arbitrária. Ao relacionar análises feitas em períodos de tempo diferentes (no caso, anos), os eixos de uma análise não têm relação com os da análise seguinte (pois foram baseados em votações distintas), então se fixarmos os eixos do ano i mais recente, o ano i-1 pode ter o eixo x espelhado ou não, e pode sofrer uma rotação de ângulo qualquer.
# Gostaríamos que estas transformações fossem tais que minimizasse o movimento dos partidos: por exemplo se no ano i o partido A resultou no lado esquerdo do gráfico, e o partido B no lado direito, mas no ano i-1 o posicionamento resultou inverso, seria desejável espelhar o eixo x, ou então rodar os eixos de 180 graus.
# Isso é alcançado através do algoritmo abaixo, de minimização da 'quantidade de movimento' total com a variação da rotação dos eixos e espelhamento do eixo x. Entre dois anos, esta quantidade de movimento é definida pela soma das distâncias euclidianas caminhadas pelos partidos ponderadas pelo tamanho do partido [no ano mais recente].
for i in range(len(anos)-2,-1,-1): # indices dos anos, de tras pra frente
    print anos[i]
    qm_min = 1000000 # quero minimizar as quantidades de movimento
    campeao = (0,0) # (espelhar, graus)
    for espelhar in [0,1]:
        for graus in [0,45,90,135,180,225,270,315]:
            qm_agora = quantidade_movimento(i,graus,espelhar)
            #print '%d, %d, %f' % (espelhar,graus,qm_agora )
            if qm_agora < qm_min:
                campeao = (espelhar, graus)
                qm_min = qm_agora
    print campeao
    if campeao[0] == 1: # espelhar
        dados[i] = numpy.dot( dados[i], numpy.array([[-1.,0.],[0.,1.]]) )
    if campeao[1] != 0: # rotacionar
        dados[i] = numpy.dot( dados[i], matrot(campeao[1]) )

print 'Fim'

# Escrever arquivo:
f = open(arquivo_de_saida,'w')
f.write("""  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript">
    google.load('visualization', '1', {packages: ['motionchart']});

    function drawVisualization() {

""")
f.write('var data = new google.visualization.DataTable();\n')
f.write("data.addColumn('string', 'Partido');\n")
f.write("data.addColumn('date', 'Data');\n")
f.write("data.addColumn('number', 'Eixo1');\n")
f.write("data.addColumn('number', 'Eixo2');\n")
f.write("data.addColumn('number', 'Tamanho');\n")
f.write("data.addRows([\n")
for ia in range(len(anuais)): # datas
    a = anuais[ia]
    d_ano = int(a.data_final[0:4])
    d_mes = int(a.data_final[5:7])-1 # em js meses sao de 0 a 11
    d_dia = int(a.data_final[8:10])
    for ip in range(len(parts)): # partidos
        linha = "  ['%s',new Date(%d,%d,%d), %f,%f,%d],\n" % (parts[ip],d_ano,d_mes,d_dia,dados[ia][ip,0],dados[ia][ip,1],a.tamanho_partido[ip])
        f.write(linha)
f.seek(-2,1)
f.write("\n]);")
f.write("""     
      var motionchart = new google.visualization.MotionChart(
          document.getElementById('visualization'));

      var options = {};
      options['state'] = '{"yAxisOption":"3","xLambda":1,"colorOption":"_UNIQUE_COLOR","playDuration":40000,"showTrails":false,"iconKeySettings":[],"xAxisOption":"2","nonSelectedAlpha":0.4,"uniColorForNonSelected":false,"xZoomedDataMax":0.815577,"sizeOption":"4","orderedByY":false,"iconType":"BUBBLE","dimensions":{"iconDimensions":["dim0"]},"yZoomedDataMax":0.907421,"orderedByX":false,"xZoomedIn":false,"xZoomedDataMin":-0.510363,"time":"2002-12-31","duration":{"timeUnit":"D","multiplier":1},"yLambda":1,"yZoomedIn":false,"yZoomedDataMin":-0.558064}'
      options['width'] = 800;
      options['height'] = 500;

      motionchart.draw(data, options);

    }
    

    google.setOnLoadCallback(drawVisualization);
  </script>

<div id="visualization" style="width: 800px; height: 400px;"></div>
""")
f.close()

