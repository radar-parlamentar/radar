#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Diego Rabatone, Saulo Trento
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
    Camaraws
    ImportadorCamara
"""

from __future__ import unicode_literals
from django.utils.dateparse import parse_datetime
from modelagem import models
import re
import sys
import xml.etree.ElementTree as etree
import urllib2

# data em que a lista votadas.txt foi atualizada
ULTIMA_ATUALIZACAO = parse_datetime('2012-06-01 0:0:0')

RESOURCES_FOLDER = 'importadores/dados/'
VOTADAS_FILE_PATH = RESOURCES_FOLDER + 'votadas.txt'

URL_PROPOSICAO = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=%s'
URL_VOTACOES = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=%s&numero=%s&ano=%s'

INICIO_PERIODO = parse_datetime('2004-01-01 0:0:0')
FIM_PERIODO = parse_datetime('2012-07-01 0:0:0')

class ProposicoesFinder:

    def __init__(self, verbose=True):
        self.verbose = verbose

    def _nome_proposicao(self, prop_xml):
        sigla = prop_xml.get('tipo').strip()
        numero = prop_xml.get('numero').strip()
        ano = prop_xml.get('ano').strip()
        return '%s %s/%s' % (sigla, numero, ano)

    def find_props_que_existem(self, file_name, id_min, id_max):
        """Retorna IDs de proposições que existem na câmara dos deputados.

        Buscas serão feitas por proposições com IDs entre id_min e id_max
        Não necessariamente todos os IDs possuem votações (na verdade a grande maioria não tem!).
        Se file_name == None, lança exceção TypeError
        """

        if file_name == None:
            raise TypeError('file_name não pode ser None')

        f = open(file_name,'a')
        f.write('# Arquivo gerado pela classe ProposicoesFinder\n')
        f.write('# para achar os IDs existentes na camara dos deputados\n')
        f.write('# Procurando ids entre %d e %d.\n' % (id_min, id_max))
        f.write('# id  : proposicao\n')
        f.write('#-----------\n')
        if self.verbose:
            print '"." id valido; "x" id invalido'

        camaraws = Camaraws()
        for id_candidato in range(id_min, id_max+1):
            if (id_candidato % 1000) == 0:
                print '\nJá procurei ateh o ID %d' % id_candidato # A cada 1000: diz onde está
            try:
                prop_xml = camaraws.obter_proposicao(id_candidato)
                nome_prop = self._nome_proposicao(prop_xml)
                f.write('%d: %s\n' %(id_candidato, nome_prop))
                if self.verbose:
                    sys.stdout.write('.')
                    sys.stdout.flush()
            except ValueError:
                if self.verbose:
                    sys.stdout.write('x')
                    sys.stdout.flush()
        f.close()

    def parse_ids_que_existem(self, file_name):
        """Lê o arquivo criado por find_props_que_existem.

        Retorna:
            Uma lista com a identificação das proposições encontradas no txt
            Cada posição da lista é um dicionário com chaves \in {id, sigla, num, ano}
            As chaves e valores desses dicionários são strings
        """
        # ex: "485262: MPV 501/2010"
        regexp = '^([0-9]*?): ([A-Z]*?) ([0-9]*?)/([0-9]{4})'
        proposicoes = []
        with open(file_name, 'r') as prop_file:
            res = re.search(regexp, prop_file.readline())
            if res:
                proposicoes.append({'id':res.group(1), 'sigla':res.group(2), 'num':res.group(3), 'ano':res.group(4)})
        return proposicoes

    def find_props_com_votacoes(self, ids_file, output, verbose=True):
        """Procura pelo web servcie da Câmara quais IDs correspondem a proposições com pelo menos uma votação.

        Argumentos:
            ids_file -- string com a localização de arquivo no formato do arquivo gerado por find_props_que_existem,
                        ou seja, cada linha possui uma entrada 'ID: SIGLA NUM/ANO'
            output -- arquivo onde vai ser gravada a saída (equivalente ao retorno do método)
            verbose -- True ou False, True é defaultf

        Retorna:
            Uma lista com a identificação das proposições que possuem votações
            Cada posição da lista é um dicionário com chaves \in {id, sigla, num, ano}
            As chaves e valores desses dicionários são strings
        """
        
        f = open(output,'a')
        f.write('# Arquivo gerado pela classe ProposicoesFinder\n')
        f.write('# para achar os IDs existentes na camara dos deputados\n')
        f.write('# que possuem votacoes.\n')
        f.write('# id  : proposicao\n')
        f.write('#-----------\n')
        if self.verbose:
            print '"." id valido; "x" id invalido'

        props = self.parse_ids_que_existem(ids_file)
        votadas = []
        camaraws = Camaraws()
        count = 0
        for prop in props:
            if count % 1000 == 0 and verbose:
                print '\nProcurando votações da proposição de ID ', prop['id']
            count += 1
            try:
                votacoes_xml = camaraws.obter_votacoes(prop['sigla'], prop['num'], prop['ano'])
                nome_prop = '%s %s/%s' % (prop['sigla'], prop['num'], prop['ano'])
                f.write('%s: %s\n' %(prop['id'], nome_prop))
                votadas.append(prop)
                if self.verbose:
                    sys.stdout.write('.')
                    sys.stdout.flush()
            except ValueError:
                if self.verbose:
                    sys.stdout.write('x')
                    sys.stdout.flush()
        f.close()
        return votadas
        

class Camaraws:
    """Acesso aos Web Services da Câmara dos Deputados
    Métodos:
        obter_proposicao(id_prop)
        obter_votacoes(sigla, num, ano)
    """

    def obter_proposicao(self, id_prop):
        """Obtém detalhes de uma proposição

        Argumentos:
        id_prop

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

        try:
            tree = etree.fromstring(xml)
        except etree.ParseError:
            raise ValueError('Proposição %s não encontrada' % id_prop)

        return tree

    def obter_votacoes(self, sigla, num, ano):
        """Obtém votacões de uma proposição

        Argumentos:
        sigla, num, ano -- strings que caracterizam a proposicão

        Retorna:
        Um objeto ElementTree correspondente ao XML retornado pelo web service
        Exemplo: http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=pl&numero=1876&ano=1999

        Exceções:
            ValueError -- quando proposição não existe ou não possui votações
        """
        
        url  = URL_VOTACOES % (sigla, num, ano)
        try:
            request = urllib2.Request(url)
            xml = urllib2.urlopen(request).read()
        except urllib2.URLError:
            raise ValueError('Votações da proposição %s %s/%s não encontrada' % (sigla, num, ano))

        try:
            tree = etree.fromstring(xml)
        except etree.ParseError:
            raise ValueError('Votações da proposição %s %s/%s não encontrada' % (sigla, num, ano))
        
        return tree


class ImportadorCamara:
    """Salva os dados dos web services da Câmara dos Deputados no banco de dados"""

    def __init__(self, verbose=False):
        """verbose (booleano) -- ativa/desativa prints na tela"""

        self.verbose = verbose
        self.votadas_ids = self._parse_votadas() # id/sigla/num/ano das proposições que tiveram votações
        self.partidos = {}

    def _converte_data(self, data_str, hora_str='00:00'):
        """Converte string 'd/m/a' para objeto datetime; retona None se data_str é inválido
        Pode também receber horário: hora_str como 'h:m'
        """
        DATA_REGEX = '(\d\d?)/(\d\d?)/(\d{4})'
        HORA_REGEX = '(\d\d?):(\d\d?)'
        dt = re.match(DATA_REGEX, data_str)
        hr = re.match(HORA_REGEX, hora_str)
        if dt and hr:
            new_str = '%s-%s-%s %s:%s:0' % (dt.group(3), dt.group(2), dt.group(1), hr.group(1), hr.group(2))
            return parse_datetime(new_str)
        else:
            return None

    def _gera_casa_legislativa(self):
        """Gera objeto do tipo CasaLegislativa representando a Câmara dos Deputados"""

        camara_dos_deputados = models.CasaLegislativa()
        camara_dos_deputados.nome = 'Câmara dos Deputados'
        camara_dos_deputados.nome_curto = 'cdep'
        camara_dos_deputados.esfera = models.FEDERAL
        camara_dos_deputados.atualizacao = ULTIMA_ATUALIZACAO
        camara_dos_deputados.save()
        return camara_dos_deputados

    def _parse_votadas(self):
        """Parse do arquivo importadores/dados/votadas.txt
        Retorna:
        Uma lista com a identificação das proposições encontradas no txt
        Cada posição da lista é um dicionário com chaves \in {id, sigla, num, ano}
        As chaves e valores desses dicionários são strings
        """
        # ex: "485262: MPV 501/2010"
        regexp = '^([0-9]*?): ([A-Z]*?) ([0-9]*?)/([0-9]{4})'
        proposicoes = []
        prop_file = open(VOTADAS_FILE_PATH, 'r') 
        for line in prop_file:
            res = re.search(regexp, line)
            if res:
                proposicoes.append({'id':res.group(1), 'sigla':res.group(2), 'num':res.group(3), 'ano':res.group(4)})
        return proposicoes

    def _prop_from_xml(self, prop_xml, id_prop):
        """Recebe XML representando proposição (objeto etree)
        e devolve objeto do tipo Proposicao, que é salvo no banco de dados.
        """
        prop = models.Proposicao()
        prop.id_prop = id_prop
        prop.sigla = prop_xml.get('tipo').strip()
        prop.numero = prop_xml.get('numero').strip()
        prop.ano = prop_xml.get('ano').strip()

        prop.ementa = prop_xml.find('Ementa').text.strip()
        prop.descricao = prop_xml.find('ExplicacaoEmenta').text.strip()
        prop.indexacao = prop_xml.find('Indexacao').text.strip()
        #prop.autores = prop_xml.find('Autor').text.strip()
        date_str = prop_xml.find('DataApresentacao').text.strip()
        prop.data_apresentacao = self._converte_data(date_str)
        prop.situacao =prop_xml.find('Situacao').text.strip()
        prop.casa_legislativa = self.camara_dos_deputados

        prop.save()
        return prop

    def _votacao_from_xml(self, vot_xml, prop):
        """Salva votação no banco de dados.

        Atributos:
            vot_xml -- XML representando votação (objeto etree)
            prop -- objeto do tipo Proposicao

        Retorna:
            objeto do tipo Votacao
        """
        votacao = models.Votacao()

        votacao.descricao = 'Resumo: [%s]. ObjVotacao: [%s]' % (vot_xml.get('Resumo'), vot_xml.get('ObjVotacao'))
        data_str = vot_xml.get('Data').strip()
        hora_str = vot_xml.get('Hora').strip()
        datetime = self._converte_data(data_str, hora_str)
        votacao.data = datetime
        votacao.proposicao = prop
        votacao.save()

        for voto_xml in vot_xml:
            self._voto_from_xml(voto_xml, votacao)

        votacao.save()
        self.progresso()
        return votacao

    def progresso(self):
        """Indica progresso na tela"""
        sys.stdout.write('x')
        sys.stdout.flush()

    def _voto_from_xml(self, voto_xml, votacao):
        """Salva voto no banco de dados.

        Atributos:
            voto_xml -- XML representando voto (objeto etree)
            votacao -- objeto do tipo Votacao

        Retorna:
            objeto do tipo Voto
        """
        voto = models.Voto()

        opcao_str = voto_xml.get('Voto')
        voto.opcao = self._opcao_xml_to_model(opcao_str)
        leg = self._legislatura(voto_xml)
        voto.legislatura = leg
        voto.votacao = votacao
        voto.save()

        return voto

    def _opcao_xml_to_model(self, voto):
        """Interpreta voto como tá no XML e responde em adequação a modelagem em models.py"""

        if voto == 'Não':
            return models.NAO
        elif voto == 'Sim':
            return models.SIM
        elif voto == 'Obstrução':
            return models.OBSTRUCAO
        elif voto == 'Abstenção':
            return models.ABSTENCAO
        else:
            print 'tipo de voto (%s) não mapeado!' % voto
            return models.ABSTENCAO

    def _legislatura(self, voto_xml):
        """Salva legislatura no banco de dados.

        Atributos:
            voto_xml -- XML representando voto (objeto etree)

        Retorna:
            objeto do tipo Legislatura
        """
        partido = self._partido(voto_xml.get('Partido'))
        votante = self._votante(voto_xml.get('Nome'))

        legs = models.Legislatura.objects.filter(parlamentar=votante,partido=partido,casa_legislativa=self.camara_dos_deputados)
        # TODO acima filtrar tb por inicio e fim
        if legs:
            leg = legs[0]
        else:
            leg = models.Legislatura()
            leg.parlamentar = votante
            leg.partido = partido
            leg.localidade = voto_xml.get('UF')
            leg.casa_legislativa = self.camara_dos_deputados
            leg.inicio = INICIO_PERIODO # TODO refinar
            leg.fim = FIM_PERIODO # TODO refinar
            leg.save()

        return leg

    def _partido(self, nome_partido):
        nome_partido = nome_partido.strip()
        partido = models.Partido.from_nome(nome_partido)
        if partido == None:
            print 'Não achou o partido %s' % nome_partido
            partido = models.Partido.get_sem_partido()
        else:
            partido.save()
            if self.verbose:
                print 'Partido %s salvo' % partido
        return partido

    def _votante(self, nome_dep):
        votantes = models.Parlamentar.objects.filter(nome=nome_dep)
        if votantes:
            votante = votantes[0]
        else:
            votante = models.Parlamentar()
            votante.save()
            #votante.id_parlamentar =
            votante.nome = nome_dep
            #votante.genero =
            votante.save()
            if self.verbose:
                print 'Deputado %s salvo' % votante
        return votante

    def importar(self):

        self.camara_dos_deputados = self._gera_casa_legislativa()

        f = lambda dic: ( dic['id'], dic['sigla'], dic['num'], dic['ano'] )
        for id_prop,sigla,num,ano in [ f(dic) for dic in self.votadas_ids ]:
            if self.verbose:
                print 'Importando %s: %s %s/%s' % (id_prop, sigla, num, ano)
            camaraws = Camaraws()
            prop_xml = camaraws.obter_proposicao(id_prop)
            prop = self._prop_from_xml(prop_xml, id_prop)
            vots_xml = camaraws.obter_votacoes(sigla, num, ano)
            for child in vots_xml.find('Votacoes'):
                self._votacao_from_xml(child, prop)


def main():

    print 'IMPORTANDO DADOS DA CÂMARA DOS DEPUTADOS'
    importer = ImportadorCamara()
    importer.importar()



