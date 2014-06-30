# -*- coding:UTF-8 -*-

from os import listdir
from xml.dom.minidom import parseString
import json
import logging
logger = logging.getLogger("radar")


arqs = listdir("bios")

generos = {}
historia = {}
lista_partidos = []

cont = 0
for arq in arqs:
    if arq[0] != ".":
        ponteiro = open("bios/" + arq)
        data = ponteiro.read()
        dom = parseString(data)
        records = dom.getElementsByTagName('DATA_RECORD')

        for record in records:
            legis = record.getElementsByTagName(
                'MANDATOSCD')[0].firstChild.data
            if legis.find("Deputada") != -1:
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

            legis = legis.split(";")
            partidos = []
            for leg in legis:
                termos = leg.split(",")
                data = termos[1].strip()
                try:
                    partido = termos[-1].strip().partition(".")[0]
                except:
                    partido = "SEM PARTIDO"
                if not len(partido):
                    partido = "SEM PARTIDO"
                if partido == "S":
                    partido = "SEM PARTIDO"

                if partido not in lista_partidos:
                    lista_partidos.append(partido)

                partidos.append(partido)

            for i in range(len(anos2)):
                legislatura = anos2[i].strip()
                partido = partidos[i]
                legis_partidos = historia.get(partido)
                if not legis_partidos:
                    legis_partidos = {}
                    historia[partido] = legis_partidos
                nums = legis_partidos.get(legislatura, {})
                if not nums:
                    nums = {"M": 0, "F": 0}
                    legis_partidos[legislatura] = nums
                nums[genero] = nums.get(genero, 0) + 1

                ano1, e, ano2 = legislatura.partition("-")
                nums["ano"] = int(ano1)
                nums["duracao"] = 4
                nums["legis"] = legislatura


            #ordenada = []
            # for a in legis_partidos.keys():
            #    ordenada.append(a)
            # ordenada.sort()

            #prox = None
            # for l in ordenada:
            #    try:
            #        prox_data = ordenada[ordenada.index(i)+1]
            #        prox = prox_data.partition("-")[0]
            #    except ValueError, error :
            #        logger.error("ValueError: %s" % error)


            #    ano1, e, ano2 = i.partition("-")
            #    duracao = int(ano2)-int(ano1)+1
            #    if ano2 == prox:
            #        duracao -= 1

            #    nums["duracao"] = duracao


print(cont)
ordenada = []
for a in historia.keys():
    ordenada.append(a)
ordenada.sort()

print(lista_partidos)

arq = open("genero_historia_partidos.json", "w")
json.dump(historia, arq)
