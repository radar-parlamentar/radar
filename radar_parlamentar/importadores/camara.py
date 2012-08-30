#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""módulo camara (Câmara dos Deputados)

Classes:
    Camaraws -- acesso aos web services com os dados da câmara dos deputados
    ImportadorCamara -- salva os dados dos web services da Câmara dos Deputados no banco de dados
"""

from __future__ import unicode_literals
from django.utils.dateparse import parse_datetime
from modelagem import models
import re
import xml.etree.ElementTree as etree
import urllib2
import io

RESOURCES_FOLDER = 'importadores/dados/'
URL_PROPOSICAO = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=%s'
URL_VOTACOES = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=%s&numero=%s&ano=%s'

class Camaraws:
    """Requisições para os Web Services da Câmara dos Deputados
    Métodos:
        obter_proposicao(id_prop)
        obter_votacoes(tipo, num, ano)
    """

    def obter_proposicao(self, id_prop):
        """Obtém detalhes de uma proposição 

        Argumentos:
        tipo, num, ano -- strings que caracterizam a proposicão

        Retorna:
        Um objeto ElementTree correspondente ao XML retornado pelo web service
        Exemplo: http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=17338

        Exceções:
            ValueError -- quando proposição não existe
        """
        url = URL_PROPOSICAO % id_prop
        try:
            request = urllib2.Request(url)
            xml = urllib2.urlopen(request).read()
        except urllib2.URLError:
            raise ValueError('Proposição %s não encontrada' % id_prop)

        tree = etree.fromstring(xml)
        return tree

    def obter_votacoes(self, sigla, num, ano):
        """Obtém votacões de uma proposição

        Argumentos:
        sigla, num, ano -- strings que caracterizam a proposicão

        Retorna:
        Um objeto ElementTree correspondente ao XML retornado pelo web service
        Exemplo: http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=pl&numero=1876&ano=1999

        Exceções:
            ValueError -- quando proposição não existe
        """
        url  = URL_VOTACOES % (sigla, num, ano)
        try:
            request = urllib2.Request(url)
            xml = urllib2.urlopen(request).read()
        except urllib2.URLError:
            raise ValueError('Votações da proposição %s %s/%s não encontrada' % (sigla, num, ano))

        tree = etree.fromstring(xml)
        return tree


class ImportadorCamara:

    def __init__(self, verbose=False):
        """verbose (booleano) -- ativa/desativa prints na tela"""

        self.verbose = verbose
        self.camara_dos_deputados = self._gera_casa_legislativa()

    def _gera_casa_legislativa(self):
        """Gera objeto do tipo CasaLegislativa representando a Câmara dos Deputados"""

        camara_dos_deputados = models.CasaLegislativa()
        camara_dos_deputados.nome = 'Câmara Municipal de São Paulo'
        camara_dos_deputados.nome_curto = 'cmsp'
        camara_dos_deputados.esfera = models.MUNICIPAL
        camara_dos_deputados.local = 'São Paulo - SP'
        #camara_dos_deputados.save()
        return camara_dos_deputados

    def _parse_votadas(self):
        """Parse do arquivo importadores/dados/votadas.txt
        Retorna:
        Uma lista com a identificação das proposições encontradas no txt
        Cada posição da lista é um dicionário com chaves \in {id, sigla, num, ano}
        As chaves e valores desses dicionários são strings
        """
        file_name = RESOURCES_FOLDER + 'votadas.txt' 
        prop_file = open(file_name, 'r')
        # ex: "485262: MPV 501/2010"
        regexp = '^([0-9]*?): ([A-Z]*?) ([0-9]*?)/([0-9]{4})'
        proposicoes = []
        for line in prop_file:
            res = re.search(regexp, line)
            if res:
                proposicoes.append({'id':res.group(1), 'sigla':res.group(2), 'num':res.group(3), 'ano':res.group(4)})
        return proposicoes

    def _prop_from_xml(self, prop_xml, id_prop):
        """Recebe XML representando proposição (objeto etree) e devolve objeto do tipo Proposicao"""
        prop = models.Proposicao()
        prop.id_prop = id_prop
        prop.sigla = prop_xml.get('tipo').strip()
        prop.numero = prop_xml.get('numero').strip()
        prop.ano = prop_xml.get('ano').strip()

        prop.ementa = prop_xml.find('Ementa').text.strip()
        prop.descricao = prop_xml.find('ExplicacaoEmenta').text.strip()
        prop.indexacao = prop_xml.find('Indexacao').text.strip()
#        prop.autores = prop_xml.find('Autor').text.strip()
        prop.data_apresentacao = prop_xml.find('DataApresentacao').text.strip()
        prop.situacao =prop_xml.find('Situacao').text.strip()
        prop.casa_legislativa = self.camara_dos_deputados

        return prop         
    
    def importar(self):

        votadas_ids = self._parse_votadas() # id/sigla/num/ano das proposições que tiveram votações
        f = lambda dic: ( dic['id'], dic['sigla'], dic['num'], dic['ano'] ) 
        for id_prop,sigla,num,ano in [ f(dic) for dic in votadas_ids ]:
            print 'Importando %s: %s %s/%s' % (id_prop, sigla, num, ano)
            camaraws = Camaraws()
            prop_xml = camaraws.obter_proposicao(id_prop)
            prop = self._prop_from_xml(prop_xml, id_prop)
            #vots_xml = camaraws.obter_votacoes(sigla, num, ano)
            print prop
        
        

def main():

    print 'IMPORTANDO DADOS DA CÂMARA DOS DEPUTADOS'
    importer = ImportadorCamara()
    importer.importar()



