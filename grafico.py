#!/usr/bin/python
# -*- coding: utf-8 -*-
import svgwrite
import re, math

class Grafico:

    # or parâmetros são os valores extremos obtidos no PCA
    def __init__(self, top, bottom, left, right):
        self.radius = 20
        self.factor = 100 # ajusta distância entre circunferências
        self.offset = (-left*self.factor + 2*self.radius, -bottom*self.factor + 2*self.radius) # ajusta posição (obs, se valores são positivos, offset deveria ser ZERO)
        self.width = (right - left)*self.factor + 4*self.radius
        self.height = (top - bottom)*self.factor + 4*self.radius
        self.svg = svgwrite.Drawing(filename="resultados/grafico.svg", size = ("%fpx" % self.width, "%fpx" % self.height))

    def add_partido(self, nome, center):

        # preparação das coordenadas para uma melhor distribuição visual
        x = center[0]*self.factor + self.offset[0]
        y = center[1]*self.factor + self.offset[1]
        center = (x, y)
        # a ideia é que a intensidade seja um valor entre 0 e 255, em hexadecimal
        intensidade = hex(int(abs(y) % 255))[2:]
        cor='#'
        #deve-se encontrar qual a linha divisória entre "direita e esquerda", é o valor do '620'.
        if y < 620:
            cor += intensidade
            cor += "0000"
        else:
            cor += "0000"
            cor += intensidade
        self.svg.add(self.svg.circle(center=center, r=self.radius, fill=cor, fill_opacity='0.5', stroke='black', stroke_width='1'))
        text = self.svg.text(nome, insert=center, text_anchor='middle', font_family='LMMono10', font_size='12', alignment_baseline='middle')
        self.svg.add(text)
        self.svg.save()
    


# parseia o arquivo resultados/pca.txt pra gerar o mapa partido => coordenadas do gráfico
def parse_from_file():

    mapa = {}
    name = 'resultados/pca.txt'
    vfile = open(name, 'r')
    regexp = '^([a-zA-Z]*?): (.*)'
    for line in vfile:
        res = re.search(regexp, line)
        if res:
            mapa[res.group(1)] = eval(res.group(2))
    return mapa

# preparacão semântica das coordenadas
# inverte os eixos do gráfico oriundo do PCA
# o que faz com que esquerda/direita fique no eixo orizontal
# e situacão/oposicão no eixo vertical
def muda_eixos(partidos):
    for part, coord in partidos.items():
        partidos[part] = (coord[1], coord[0])

# encontra extremos do gráfico
def extremos(partidos):
    top = bottom = left = right = 0
    for coord in partidos.values():
        if coord[0] > right:
            right = coord[0] 
        if coord[0] < left:
            left = coord[0] 
        if coord[1] > top:
            top = coord[1] 
        if coord[1] < bottom:
            bottom = coord[1] 
    return top, bottom, left, right 

if __name__ == "__main__":

    partidos = parse_from_file()
    top, bottom, left, right = extremos(partidos)

    # desenha o gráfico
    grafico = Grafico(top, bottom, left, right)
    #muda_eixos(partidos) # achei que o resultado disso ficou meio feio 
    # pois pra apresentar na web é melhor que o eixo horizontal seja o maior
    for part, coord in partidos.items():
        grafico.add_partido(part, (coord[0], coord[1]))



