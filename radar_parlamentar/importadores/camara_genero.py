# !/usr/bin/python
# coding=utf8

# Copyright (C) 2013, Diego Rabatone
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

"""módulo que cuida da importação dos dados da Câmara dos Deputados"""

from __future__ import unicode_literals
import json
import csv

HEADERS = [
    "codProposicao", "txtProposicao", "txtTipoProposicao", "txtSigla",
    "numNumero", "numAno", "datApresentacao", "codTipoProposicao",
    "codOrgaoOrigem", "txtEmenta", "txtExplicacaoEmenta", "txtIndexacao",
    "codRegime", "txtRegime", "codApreciacao", "txtApreciacao",
    "txtOrgaoOrigem", "txtNomeOrgaoOrigem", "indGenero", "txtNomeAutor",
    "txtSiglaUF", "txtSiglaPartido", "codPartido", "qtdAutores",
    "datDespacho", "txtDespacho", "codEstadoProposicao",
    "txtEstadoProposicao", "codOrgaoEstado", "txtSiglaOrgaoEstado",
    "qtdOrgaosComEstado", "codProposicaoPrincipal", "txtProposicaoPrincipal",
    "ideCadastro", "nomeProposicaoOrigem"]

PARTIDOS = {}
DIC_TERMOS = {}
PALAVRAS_MAIS_MAIS = []
DESCARTADAS = ['de', 'do', 'da', 'dos', 'das', 'e', 'para', 'com', 'a', 'A']
FILTRADAS = [
    'lei', 'normas', 'obrigatoriedade', 'cria\u00e7\u00e3o', 'nacional',
    'prazo', 'fixa\u00e7\u00e3o', 'proibi\u00e7\u00e3o',
    'especial', 'pessoa', 'utiliza\u00e7\u00e3o', 'atividade', 'valor',
    'institui\u00e7\u00e3o', 'civil', 'estabelecimento', 'registro']
LISTA_BASE_PARTIDOS = [
    'PCB', 'PSD', 'UDN', 'SEM PARTIDO', 'PP', 'PR', 'PTB', 'PRE', 'PRF', 'PST',
    'UPF', 'AL', 'FUG', 'PSN', 'PSP', 'PRP', 'PTN', 'PDC', 'PNI', 'PL', 'PPR',
    'ARENA', 'PTR', 'PSB', 'PRR', 'PSC', 'PRD', 'LASP', 'PRM', 'PRT', 'PPS',
    'PSR', 'PS', 'PDS', 'MTR', 'MDB', 'PMDB', 'PSDB', 'PFL', 'PT', 'PTdoB',
    'PDT', 'PJ', 'PCdoB', 'PC', 'PV', 'PRN', 'PPB', 'PSDC', 'PRONA', 'DEM',
    'PSOL', 'PMN', 'PSL', 'PRS', 'PRB', 'PE', 'PRC', 'PRL', 'UDB', 'PLC',
    'LEC', 'PD', 'ED', 'PRPa', 'PED', 'PNS', 'PPA', 'PNA', 'PSTU', 'PTC',
    'PAN', 'PHS', 'PRTB']

matrix = {}


def converte_csv_para_json(nome_arquivo_entrada):
    sep = b";"
    file = open(nome_arquivo_entrada + '.csv', 'r')
    reader = csv.DictReader(file, delimiter=sep, fieldnames=HEADERS)
    out = json.loads(json.dumps([row for row in reader], indent=4))
    return out


def _null_to_none(proposicao):
    for atributo in proposicao.keys():
        if proposicao[atributo] == "NULL":
            proposicao[atributo] = None
    return proposicao


def multiple_null_remove(lista_proposicoes):
    nova_lista = []
    for proposicao in lista_proposicoes:
        nova_lista.append(_null_to_none(proposicao))
    return nova_lista


def proposicoes_indexadas(lista_proposicoes):
    indexados = []
    for proposicao in lista_proposicoes:
        if proposicao['txtIndexacao'] and proposicao['txtSiglaPartido']:
            if proposicao['txtSiglaPartido'].strip() in LISTA_BASE_PARTIDOS:
                indexados.append(proposicao)
    return indexados


def parseia_indexacoes(indexacao):
    indexacao1 = [termo.strip()
                  for termo in indexacao.replace('\n', '').replace('.', '').replace('_', '').split(',')]
    indexacao2 = []
    for termo in indexacao1:
        termo = termo.split(' ')
        for termo2 in termo:
            if not termo2 == "":
                indexacao2.append(termo2.lower())
    return indexacao2


def parsear_indexacoes_de_proposicoes(lista_proposicoes):
    nova_lista_proposicoes = []
    for proposicao in lista_proposicoes:
        proposicao['txtIndexacao'] = parseia_indexacoes(
            proposicao['txtIndexacao'])
        nova_lista_proposicoes.append(proposicao)
        if proposicao['txtSiglaPartido']:
            soma_palavras_no_partido(
                proposicao['txtSiglaPartido'], proposicao['txtIndexacao'])
    return nova_lista_proposicoes


def partidos_das_proposicoes(lista_proposicoes):
    for proposicao in lista_proposicoes:
        if proposicao['txtSiglaPartido']:
            partido = proposicao['txtSiglaPartido'].strip()
            if partido not in PARTIDOS:
                PARTIDOS[partido] = {}


def contabiliza_termos_geral(lista_indexadas):
    for proposicao in lista_indexadas:
        for termo in proposicao['txtIndexacao']:
            if termo not in DESCARTADAS:
                if termo in DIC_TERMOS:
                    DIC_TERMOS[termo] += 1
                else:
                    DIC_TERMOS[termo] = 1


def pega_maiores_palavras(dic_palavras):
    palavras = sorted(dic_palavras, key=lambda k: -dic_palavras[k])
    export_json(palavras, "lista_50_mais")
    global PALAVRAS_MAIS_MAIS
    PALAVRAS_MAIS_MAIS = palavras[0:50]
    for termo in FILTRADAS:
        PALAVRAS_MAIS_MAIS.remove(termo)


def ordena_palavras_partido():
    for partido in PARTIDOS:
        palavras_partido = PARTIDOS[partido]
        palavras = sorted(palavras_partido, key=lambda k: -palavras_partido[k])
        PARTIDOS[partido] = {}
        for termo in palavras:
            PARTIDOS[partido][termo] = palavras_partido[termo]


def soma_palavras_no_partido(partido, lista_palavras):
    for palavra in lista_palavras:
        if palavra not in PARTIDOS[partido.strip()]:
            PARTIDOS[partido.strip()][palavra] = 1
        else:
            PARTIDOS[partido.strip()][palavra] += 1


def export_json(data, filename):
    with open(filename, 'w') as outFile:
        outFile.write(json.dumps(data, indent=4))


def jsonMatrix_gera_partidos():
    i = 0
    lista_partidos = []
    for partido in PARTIDOS:
        lista_partidos.append({'name': partido, 'group': 1, 'id': i})
        i += 1
    global matrix
    matrix['partidos'] = lista_partidos


def jsonMatrix_gera_termos_mais_mais():
    i = 0
    lista_termos = []
    global matrix
    matrix['termos'] = []
    for termo in PALAVRAS_MAIS_MAIS:
        print(termo, i)
        lista_termos.append({'name': termo, 'group': 1, 'id': i})
        i += 1
    matrix['termos'] = lista_termos
    print(matrix['termos'])


def jsonMatrix_gera_links_partidos_termos():
    global matrix
    matrix['links'] = []
    for p in range(len(matrix['partidos'])):
        partidoNome = matrix['partidos'][p]['name']
        for t in range(len(matrix['termos'])):
            termoNome = matrix['termos'][t]['name']
            if termoNome in PARTIDOS[partidoNome]:
                matrix['links'].append(
                    {'source': t, 'target': p, 'value': PARTIDOS[
                     partidoNome][termoNome]})


def principal(fonte=None):
    if not fonte:
        fonte = 'pl'
    lista_proposicoes = converte_csv_para_json(fonte)
    lista_proposicoes = multiple_null_remove(lista_proposicoes)
    lista_proposicoes = proposicoes_indexadas(lista_proposicoes)
    partidos_das_proposicoes(lista_proposicoes)
    lista_proposicoes = parsear_indexacoes_de_proposicoes(lista_proposicoes)
    contabiliza_termos_geral(lista_proposicoes)
    pega_maiores_palavras(DIC_TERMOS)
    # ordena_palavras_partido()
    jsonMatrix_gera_partidos()
    jsonMatrix_gera_termos_mais_mais()
    print(matrix['termos'])
    jsonMatrix_gera_links_partidos_termos()
    with open('matrix.json', 'w') as arqMatrix:
        arqMatrix.write(json.dumps(matrix, indent=4))

    retorno = {'partidos': PARTIDOS, 'dic_termos':
               DIC_TERMOS, 'lista_proposicoes': lista_proposicoes}

    #export_json(PARTIDOS, 'partidospropositores.json')
    #export_json(lista_proposicoes, 'lista_proposicoes.json')
    export_json(DIC_TERMOS, 'dic_termos.json')

    return retorno
