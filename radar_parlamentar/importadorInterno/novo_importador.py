#!/usr/bin/python
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
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.from __future__ import unicode_literals
from django.core import serializers
import xml.etree.ElementTree as etree
import urllib2
import os
from modelagem import models

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_FOLDER = os.path.join(MODULE_DIR, '../exportadores/dados/EXEMPLO.xml')



class importador_interno:

	def __init__(self):
		self.lista_proposicao = []
		self.lista_votacao = []


	
	def carrega_xml(self):
		diretorio = RESOURCES_FOLDER	
		tree = etree.parse(diretorio)
		root = tree.getroot()
		
		#dicionario = dict(root)
		casaLegislativa = models.CasaLegislativa()
		casaLegislativa.nome_curto = root.attrib.get("nome_curto")
		casaLegislativa.nome = root.attrib.get("nome")
		casaLegislativa.esfera = root.attrib.get("esfera")
		casaLegislativa.local = root.attrib.get("local")
		casaLegislativa.atualizacao = root.attrib.get("atualizacao")
		casaLegislativa.save()
		
		for child in root.iter("Proposicao"):
			proposicao = models.Proposicao()
			proposicao.casa_legislativa = models.CasaLegislativa.objects.get(nome_curto = casaLegislativa.nome_curto)
			proposicao.id_prop = child.attrib.get("id_prop")
			proposicao.sigla = child.attrib.get("sigla")
			proposicao.numero = child.attrib.get("numero")
			proposicao.ano = child.attrib.get("ano")
			proposicao.ementa = child.attrib.get("ementa")
			proposicao.descricao = child.attrib.get("descricao")
			proposicao.indexacao = child.attrib.get("indexacao")
			if(child.attrib.get("data_apresentacao") == ""):
				#Valor default caso a data venha em branco
				proposicao.data_apresentacao = "1900-01-01"
				proposicao.save()
			else:	
				proposicao.data_apresentacao = child.attrib.get("data_apresentacao")	
				proposicao.save()	
	
			for child in root.iter("Votacao"):
				votacao = models.Votacao()
				votacao.proposicao = models.Proposicao.objects.get(id_prop = proposicao.id_prop)
				votacao.id_vot = child.attrib.get("id_vot")
				votacao.descricao = child.attrib.get("descricao")
			   	votacao.data = child.attrib.get("data")
				votacao.resultado = child.attrib.get("resultado")
				votacao.save()

				for child in root.iter("Voto"):
					partido = models.Partido()
					partido.numero = child.attrib.get("numero")
					partido.nome = child.attrib.get("partido")
					partido.save()
					
					parlamentar = models.Parlamentar()
					parlamentar.nome = child.attrib.get("nome")
					parlamentar.id_parlamentar = child.attrib.get("id_parlamentar")
					parlamentar.genero = child.attrib.get("genero")
					parlamentar.save()
				
					legislatura = models.Legislatura()
					legislatura.partido = models.Partido.objects.get(chave = partido.chave)
					legislatura.parlamentar = models.Parlamentar.objects.get(chave = parlamentar.chave)
					legislatura.casa_legislativa = models.CasaLegislativa(nome_curto= casaLegislativa.nome_curto)
					legislatura.inicio = child.attrib.get("inicio")
					legislatura.fim = child.attrib.get("fim")
					legislatura.localidade = "vazio"
					legislatura.save()

					
					voto = models.Voto()
					voto.votacao = models.Votacao.objects.get(id_votacao = votacao.id_votacao)
					voto.legislatura = models.Legislatura.objects.get(chave = legislatura.chave)
					voto.opcao = child.attrib.get("opcao")
					voto.save()

			return;	

				#self.lista_votacao.append(votacao)	
				
		

def main():
	x = importador_interno()
	x.carrega_xml()










