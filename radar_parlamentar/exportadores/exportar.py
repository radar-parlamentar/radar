# !/usr/bin/python
# coding=utf8

# Copyright (C) 2013, Arthur Del Esposte, David Carlos de Araujo Silva
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

from django.core import serializers
from modelagem import models
import os

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))


def main():
    serialize_partido()
    serialize_casa_legislativa()
    serialize_parlamentar()
    serialize_legislatura()
    serialize_proposicao()
    serialize_votacao()
    serialize_voto()


def serialize_partido():
    XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()
    filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
    out = open(filepath, "w")
    xml_serializer.serialize(models.Partido.objects.all(), stream=out)


def serialize_casa_legislativa():
    XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()
    out = open(os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml'), "w")
    xml_serializer.serialize(models.CasaLegislativa.objects.all(), stream=out)


def serialize_parlamentar():
    XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()
    out = open(os.path.join(MODULE_DIR, 'dados/parlamentar.xml'), "w")
    xml_serializer.serialize(models.Parlamentar.objects.all(), stream=out)


def serialize_legislatura():
    XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()
    out = open(os.path.join(MODULE_DIR, 'dados/legislatura.xml'), "w")
    xml_serializer.serialize(models.Legislatura.objects.all(), stream=out)


def serialize_proposicao():
    XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()
    out = open(os.path.join(MODULE_DIR, 'dados/proposicao.xml'), "w")
    xml_serializer.serialize(models.Proposicao.objects.all(), stream=out)


def serialize_votacao():
    XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()
    out = open(os.path.join(MODULE_DIR, 'dados/votacao.xml'), "w")
    xml_serializer.serialize(models.Votacao.objects.all(), stream=out)


def serialize_voto():
    XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()
    out = open(os.path.join(MODULE_DIR, 'dados/voto.xml'), "w")
    voto = models.Voto.objects.all()
    for e in voto:
        e.id = None
    xml_serializer.serialize(voto, stream=out)
