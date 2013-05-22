#!/usr/bin/python
# coding=utf8

from django.core import serializers
from modelagem import models
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


def serialize_partido():
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
	out = open(filepath, "w")
	xml_serializer.serialize(models.Partido.objects.all(), stream=out)
	data = xml_serializer.getvalue()

def serialize_casa_legislativa():
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	out = open(os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml'), "w")
	xml_serializer.serialize(models.CasaLegislativa.objects.all(), stream=out)
	data = xml_serializer.getvalue()
	
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
	

	





	


	

