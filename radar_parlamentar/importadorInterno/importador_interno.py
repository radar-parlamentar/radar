from django.core import serializers
from modelagem import models
import re
import sys
import os


MODULE_DIR = os.getcwd() + '/exportadores/'

def main():
	deserialize_partido()
	deserialize_casa_legislativa()
	deserialize_parlamentar()
	deserialize_legislatura()
	deserialize_proposicao()
	deserialize_votacao()
	deserialize_voto()

def deserialize_partido():
	filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
	out = open(filepath, "r")
	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()

def deserialize_casa_legislativa():
	filepath = os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml')
	out = open(filepath, "r")
	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()

def deserialize_parlamentar():
	filepath = os.path.join(MODULE_DIR, 'dados/parlamentar.xml')
	out = open(filepath, "r")
	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()

def deserialize_legislatura():
	filepath = os.path.join(MODULE_DIR, 'dados/legislatura.xml')
	out = open(filepath, "r")
	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()


def deserialize_proposicao():
	filepath = os.path.join(MODULE_DIR, 'dados/proposicao.xml')
	out = open(filepath, "r")
	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()


def deserialize_votacao():
	filepath = os.path.join(MODULE_DIR, 'dados/votacao.xml')
	out = open(filepath, "r")
	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()


def deserialize_voto():
	filepath = os.path.join(MODULE_DIR, 'dados/voto.xml')
	out = open(filepath, "r")
	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()






	
