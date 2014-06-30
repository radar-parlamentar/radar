# !/usr/bin/python
# coding=utf8

# Copyright (C) 2013, David Carlos de Araujo Silva
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
# along with Radar Parlamentar.  If not, see
# <http://www.gnu.org/licenses/>.from __future__ import unicode_literals
import xml.etree.ElementTree as etree
import os
from modelagem import models

import logging
logger = logging.getLogger("radar")

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_FOLDER = os.path.join(MODULE_DIR, '../exportadores/dados/')


class importador_interno:

    def __init__(self):
        self.verifica_voto = False
        self.verifica_votacao = False

    def carrega_xml(self, nome_curto):
        diretorio = RESOURCES_FOLDER + nome_curto + '.xml'
        try:
            tree = etree.parse(diretorio)
            root = tree.getroot()
        except Exception:
            logger.error("Arquivo não encontrado: %s.xml" % nome_curto)
            print "Xml não encontrado"
            return None

        models.CasaLegislativa.deleta_casa(nome_curto)
        print "Voltei"

        casaLegislativa = models.CasaLegislativa()
        casaLegislativa.nome_curto = root.attrib.get("nome_curto")
        casaLegislativa.nome = root.attrib.get("nome")
        casaLegislativa.esfera = root.attrib.get("esfera")
        casaLegislativa.local = root.attrib.get("local")
        casaLegislativa.atualizacao = root.attrib.get("atualizacao")
        casaLegislativa.save()

        for child_proposicao in root.iter("Proposicao"):

            proposicao = models.Proposicao()
            proposicao.casa_legislativa = casaLegislativa
            proposicao.id_prop = child_proposicao.attrib.get("id_prop")
            proposicao.sigla = child_proposicao.attrib.get("sigla")
            proposicao.numero = child_proposicao.attrib.get("numero")
            proposicao.ano = child_proposicao.attrib.get("ano")
            proposicao.ementa = child_proposicao.attrib.get("ementa")
            proposicao.descricao = child_proposicao.attrib.get("descricao")
            proposicao.indexacao = child_proposicao.attrib.get("indexacao")
            if(child_proposicao.attrib.get("data_apresentacao") == "None"):
                # Valor default caso a data venha em branco
                proposicao.data_apresentacao = "1900-01-01"
                proposicao.save()
            else:
                proposicao.data_apresentacao = child_proposicao.attrib.get(
                    "data_apresentacao")
                proposicao.save()

            # Pega a filha da subarvore que está sendo percorrida.
            for child_votacao in child_proposicao.findall("Votacao"):

                votacao = models.Votacao()
                votacao.proposicao = proposicao
                votacao.id_votacao = child_votacao.attrib.get("id_votacao")
                votacao.id_vot = child_votacao.attrib.get("id_vot")
                votacao.descricao = child_votacao.attrib.get("descricao")
                votacao.data = child_votacao.attrib.get("data")
                votacao.resultado = child_votacao.attrib.get("resultado")
                votacao.save()

                for child_voto in child_votacao.findall("Voto"):

                    partido = models.Partido()
                    partido.numero = child_voto.attrib.get("numero")
                    partido.nome = child_voto.attrib.get("partido")
                    partido_existente = models.Partido.objects.filter(
                        numero=partido.numero, nome=partido.nome)
                    if len(partido_existente) > 0:
                        partido = partido_existente[0]
                    else:
                        partido.save()

                    parlamentar = models.Parlamentar()
                    parlamentar.nome = child_voto.attrib.get("nome")
                    parlamentar.id_parlamentar = child_voto.attrib.get(
                        "id_parlamentar")
                    parlamentar.genero = child_voto.attrib.get("genero")
                    parlamentar_existente = models.Parlamentar.objects.filter(
                        nome=parlamentar.nome,
                        id_parlamentar=parlamentar.id_parlamentar,
                        genero=parlamentar.genero)
                    if len(parlamentar_existente) > 0:
                        parlamentar = parlamentar_existente[0]
                    else:
                        parlamentar.save()

                    legislatura = models.Legislatura()
                    legislatura.partido = partido
                    legislatura.parlamentar = parlamentar
                    legislatura.casa_legislativa = casaLegislativa
                    legislatura.inicio = child_voto.attrib.get("inicio")
                    legislatura.fim = child_voto.attrib.get("fim")
                    legislatura.localidade = child_voto.attrib.get(
                        "localidade")
                    if legislatura.localidade is None:
                        legislatura.localidade = ""
                    else:
                        legislatura.localidade = "" + legislatura.localidade
                    legislatura_existente = models.Legislatura.objects.filter(
                        partido=legislatura.partido,
                        parlamentar=legislatura.parlamentar,
                        casa_legislativa=legislatura.casa_legislativa,
                        inicio=legislatura.inicio, fim=legislatura.fim)
                    if len(legislatura_existente) > 0:
                        legislatura = legislatura_existente[0]
                    else:
                        legislatura.save()

                    voto = models.Voto()
                    voto.votacao = votacao
                    voto.legislatura = legislatura
                    voto.opcao = child_voto.attrib.get("opcao")
                    voto.save()


def main(nome_curto):
    x = importador_interno()
    x.carrega_xml(nome_curto)
