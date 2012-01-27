#!/usr/bin/python
import svgwrite


class Grafico:

    def __init__(self):
        self.svg = svgwrite.Drawing(filename="resultados/grafico.svg", size = ("800px", "600px"))

    def add_partido(self, nome, center, raio=40):
        self.svg.add(self.svg.circle(center=center, r=raio, fill='white', stroke='black', stroke_width='1'))
        text = self.svg.text(nome, insert=center, text_anchor='middle', font_family='LMMono10', alignment_baseline='middle')
        self.svg.add(text)
        self.svg.save()
    




if __name__ == "__main__":
    grafico = Grafico()
    grafico.add_partido('PCdoB', (500, 300))
