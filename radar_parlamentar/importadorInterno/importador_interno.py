#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Guilherme Januário, Diego Rabatone
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
	try:
		filepath = os.path.join(MODULE_DIR, 'dados/partido.xml')
		out = open(filepath, "r")
	except IOError as e:
		print "I/O erro, não há nenhum arquivo de Partido para ser importado".format(e.errno, e.strerror)
		return

	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()

def deserialize_casa_legislativa():
	try:
		filepath = os.path.join(MODULE_DIR, 'dados/casa_legislativa.xml')
		out = open(filepath, "r")
	except IOError as e:
		print "I/O erro, não há nenhum arquivo de CasaLegislativa para ser importado".format(e.errno, e.strerror)
		return

	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()

def deserialize_parlamentar():
	try:
		filepath = os.path.join(MODULE_DIR, 'dados/parlamentar.xml')
		out = open(filepath, "r")
	except IOError as e:
		print "I/O erro, não há nenhum arquivo de Parlamentar para ser importado".format(e.errno, e.strerror)
		return

	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()

def deserialize_legislatura():
	try:
		filepath = os.path.join(MODULE_DIR, 'dados/legislatura.xml')
		out = open(filepath, "r")
	except IOError as e:
		print "I/O erro, não há nenhum arquivo de Legislatura para ser importado".format(e.errno, e.strerror)
		return	
	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()


def deserialize_proposicao():
	try:
		filepath = os.path.join(MODULE_DIR, 'dados/proposicao.xml')
		out = open(filepath, "r")
	except IOError as e:
		print "I/O erro, não há nenhum arquivo de Proposição para ser importado".format(e.errno, e.strerror)
		return

	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()


def deserialize_votacao():
	try:
		filepath = os.path.join(MODULE_DIR, 'dados/votacao.xml')
		out = open(filepath, "r")
	except IOError as e:
		print "I/O erro, não há nenhum arquivo de Votacação para ser importado".format(e.errno, e.strerror)
		return
			
	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()


def deserialize_voto():
	try:
		filepath = os.path.join(MODULE_DIR, 'dados/voto.xml')
		out = open(filepath, "r")
	except IOError as e:
		print "I/O erro, não há nenhum arquivo de Voto para ser importado".format(e.errno, e.strerror)
		return

	data = serializers.deserialize("xml", out)
	for deserialized_object in data:
    		deserialized_object.save()






	
