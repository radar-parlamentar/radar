# !/usr/bin/python
# coding=utf8

# Copyright (C) 2013, Arthur Del Esposte, David Carlos de Araujo Silva,
# Luciano Endo, Diego Rabatone
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

from modelagem import models
from xml.etree.ElementTree import Element, ElementTree
import sys
import os

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))


def serialize_casa_legislativa(nome_curto):

    # Identificando Casa
    casa = models.CasaLegislativa.objects.filter(nome_curto=nome_curto)
    if len(casa) <= 0:
        raise ValueError('Casa Legislativa não encontrada\n')

    reload(sys)
    sys.setdefaultencoding("utf-8")

    print "\nExportando dados de %s\n" % casa[0].nome

    root = Element('CasaLegislativa', nome=casa[0].nome, nome_curto=casa[
                   0].nome_curto, esfera=casa[0].esfera, local=casa[0].local,
                   atualizacao=str(casa[0].atualizacao))

    # Identificando a proposição
    proposicao = models.Proposicao.objects.filter(
        casa_legislativa_id__nome_curto=nome_curto)

    for e in proposicao:
        print "Exportando todas as votações e votos da Proposicao com id: "
        print str(e.id_prop) + ", numero: " + str(e.numero)
        proposicao_xml = Element(
            'Proposicao', id_prop=str(e.id_prop),
            sigla=e.sigla, numero=str(e.numero), ano=str(e.ano),
            ementa=e.ementa, descricao=e.descricao,
            indexacao=str(e.indexacao),
            data_apresentacao=str(e.data_apresentacao), situacao=e.situacao)

        votacao = models.Votacao.objects.filter(proposicao_id=e)
        for v in votacao:
            votacao_xml = Element('Votacao', id_vot=str(
                v.id_vot), descricao=v.descricao, data=str(v.data),
                resultado=v.resultado)

            # =--------------Voto----------=#
            votos = models.Voto.objects.filter(votacao_id=v)
            for voto in votos:

                legislatura = voto.legislatura
                parlamentar = legislatura.parlamentar
                partido = legislatura.partido

                voto_xml = Element(
                    'Voto', nome=parlamentar.nome, id_parlamentar=str(
                        parlamentar.id_parlamentar), genero=parlamentar.genero,
                    partido=partido.nome, inicio=str(legislatura.inicio),
                    fim=str(legislatura.fim), numero=str(partido.numero),
                    opcao=voto.opcao)

                votacao_xml.append(voto_xml)

            proposicao_xml.append(votacao_xml)

        root.append(proposicao_xml)

    filepath = os.path.join(MODULE_DIR, 'dados/' + nome_curto + '.xml')
    out = open(filepath, "w")
    ElementTree(root).write(out)
    out.close()

    print "Exportação realizada com sucesso"
