#!/usr/bin/python
# -*- coding: utf-8 -*-
import svgwrite
import re

class Grafico:

    def __init__(self):
        self.svg = svgwrite.Drawing(filename="resultados/grafico.svg", size = ("1000px", "1000px"))

    def add_partido(self, nome, center, raio=40):

        # TODO desafio: o que fazer com os partidos que ficam com o nome escondido?

        # preparação das coordenadas para uma melhor distribuição visual
        center = (center[0]*100 + 300, center[1]*100 + 300)
        self.svg.add(self.svg.circle(center=center, r=raio, fill='white', stroke='black', stroke_width='1'))
        text = self.svg.text(nome, insert=center, text_anchor='middle', font_family='LMMono10', alignment_baseline='middle')
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

if __name__ == "__main__":

    partidos = parse_from_file()

    # TODO
    # preparação semântica das coordenadas:
    # deixar esquerda/direita (ideologia) no eixo horizontal
    # deixar situação pra cima e oposição pra baixo

    # desenha o gráfico
    grafico = Grafico()
    for part, coord in partidos.items():
        grafico.add_partido(part, (coord[0], coord[1]))



