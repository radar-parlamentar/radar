# -*- coding:UTF-8 -*-

from os import listdir
from xml.dom.minidom import parseString
import json


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
                legis_partidos = historia.get(legislatura)
                if not legis_partidos:
                    legis_partidos = {}
                    historia[legislatura] = legis_partidos
                nums = legis_partidos.get(partido, {})
                if not nums:
                    nums = {"M": 0, "F": 0}
                    legis_partidos[partido] = nums
                nums[genero] = nums.get(genero, 0) + 1


print(cont)

print(historia.keys())

arq = open("genero_comparativo_partidos.json", "w")
json.dump(historia, arq)
