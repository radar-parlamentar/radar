# -*- coding:UTF-8 -*-

from os import listdir
from xml.dom.minidom import parseString
import logging
logger = logging.getLogger("radar")


arqs = listdir("bios")
saida = open("saida.csv", "w")

generos = {}
historia = {}

cont = 0
for arq in arqs:
    if arq[0] != ".":
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
            legis_anos = record.getElementsByTagName(
                'LEGISLATURAS')[0].firstChild.data
            generos[nome] = genero

            anos = legis_anos.split(",")
            anos2 = []
            for ano in anos:
                if ano.find("e") == -1:
                    anos2.append(ano)
                else:
                    ano1, e, ano2 = ano.partition("e")
                    anos2.append(ano1.strip())
                    anos2.append(ano2.strip()[:-1])
            for ano in anos2:
                ano = ano.strip()

                historia[ano] = historia.get(ano, []) + [nome]

print(cont)
ordenada = []
for a in historia.keys():
    ordenada.append(a)
ordenada.sort()


saida.write("Ano,Feminino,Masculino,Total,Duracao,Legislatura\n")
for i in ordenada:
    femi = 0
    masc = 0
    total = len(historia[i])
    for pessoa in historia[i]:
        gen = generos[pessoa]
        if gen == "F":
            femi += 1
        else:
            masc += 1

    try:
        prox_data = ordenada[ordenada.index(i) + 1]
    except ValueError, error:
        logger.error("ValueError: %s" % error)

    prox = prox_data.partition("-")[0]

    ano1, e, ano2 = i.partition("-")
    duracao = int(ano2) - int(ano1) + 1
    if ano2 == prox:
        duracao -= 1

    saida.write("%s,%s,%s,%s,%s,%s\n" % (ano1, femi, masc, total, duracao, i))
