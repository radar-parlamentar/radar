# -*- coding:UTF-8 -*-

from os import listdir
from xml.dom.minidom import parseString


arqs = listdir("bios")
saida = open("saida.csv", "w")

cont = 0
for arq in arqs:
        ponteiro = open("bios/" + arq)
        data = ponteiro.read()
        dom = parseString(data)
        records = dom.getElementsByTagName('DATA_RECORD')

        for record in records:
            dep = record.getElementsByTagName('MANDATOSCD')[0].firstChild.data
            if dep.find("Deputada") != -1:
                genero = "F"
                cont += 1
            else:
                genero = "M"
            nome = record.getElementsByTagName('TXTNOME')[0].firstChild.data
            legis = record.getElementsByTagName(
                'MANDATOSCD')[0].firstChild.data
            legis = legis.split(";")
            saida_legis = ""
            for leg in legis:
                dados = leg.split(",")
                ano = dados[1]
                saida_legis += "%s/" % ano
                try:
                    estado = dados[2]
                    saida_legis += "%s/" % estado
                    partido = dados[3].partition(".")[0]
                    saida_legis += "%s/" % partido
                    saida_legis += " , "
                except:
                    print(dados)
                    saida_legis += " , "
            saida.write('%s|%s|%s\n' % (nome, genero, saida_legis))

print(cont)
