#!/usr/bin/python
# coding=utf8

# Copyright (C) 2013, Arthur Del Esposte, David Carlos de Araujo Silva, Luciano Endo 
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
from xml.dom.minidom import parseString
import re
import sys
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

def serialize_casa_legislativa(nome_curto):
	casa = models.CasaLegislativa.objects.filter(nome_curto = nome_curto)
	if len(casa) <= 0:
		raise ValueError('Casa Legislativa não encontrada\n')

	casa_xml = '<CasaLegislativa nome="' + casa[0].nome + '" nome_curto="' + casa[0].nome_curto + '" esfera="' + casa[0].esfera + '" local="' + casa[0].local + '" atualizacao="' + str(casa[0].atualizacao) + '">'

	print casa_xml

	'''
	doc = parseString("""<CasaLegislativa""")

	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	out = open(os.path.join(MODULE_DIR, 'dados/'+nome_curto+'.xml'), "w")

	xml_serializer.serialize(models.CasaLegislativa.objects.filter(), stream=out)
	data = xml_serializer.getvalue()
	'''

def serialize_partido():
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
	out = open(filepath, "w")
	xml_serializer.serialize(models.Partido.objects.all(), stream=out)
	data = xml_serializer.getvalue()
'''
def serialize_casa_legislativa():
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	out = open(os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml'), "w")
	xml_serializer.serialize(models.CasaLegislativa.objects.all(), stream=out)
	data = xml_serializer.getvalue()
'''	
def serialize_parlamentar():
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	out = open(os.path.join(MODULE_DIR, 'dados/parlamentar.xml'), "w")
	xml_serializer.serialize(models.Parlamentar.objects.all(), stream=out)
	data = xml_serializer.getvalue()
		
def serialize_legislatura():
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	out = open(os.path.join(MODULE_DIR, 'dados/legislatura.xml'), "w")
	xml_serializer.serialize(models.Legislatura.objects.all(), stream=out)
	data = xml_serializer.getvalue()
	
def serialize_proposicao():
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	out = open(os.path.join(MODULE_DIR, 'dados/proposicao.xml'), "w")
	xml_serializer.serialize(models.Proposicao.objects.all(), stream=out)
	data = xml_serializer.getvalue()
	
def serialize_votacao():
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	out = open(os.path.join(MODULE_DIR, 'dados/votacao.xml'), "w")
	xml_serializer.serialize(models.Votacao.objects.all(), stream=out)
	data = xml_serializer.getvalue()
	
def serialize_voto():
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	out = open(os.path.join(MODULE_DIR, 'dados/voto.xml'), "w")
	xml_serializer.serialize(models.Voto.objects.all(), stream=out)
	data = xml_serializer.getvalue()
	

	





	


	

