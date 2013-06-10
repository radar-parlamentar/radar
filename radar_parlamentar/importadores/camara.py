#!/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Diego Rabatone, Saulo Trento
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

"""módulo camara (Câmara dos Deputados)

Classes:
    Camaraws
    ImportadorCamara
"""

from __future__ import unicode_literals
from django.utils.dateparse import parse_datetime
from django.db.utils import DatabaseError
from modelagem import models
from datetime import datetime
import re
import sys
import os
import xml.etree.ElementTree as etree
import urllib2
import logging
import Queue
import threading
import time
import math

# data em que a lista votadas.txt foi atualizada
ULTIMA_ATUALIZACAO = parse_datetime('2012-06-01 0:0:0')

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

RESOURCES_FOLDER = os.path.join(MODULE_DIR, 'dados/cdep/')
VOTADAS_FILE_PATH = RESOURCES_FOLDER + 'votadas.txt'

INICIO_PERIODO = parse_datetime('2004-01-01 0:0:0')
FIM_PERIODO = parse_datetime('2012-07-01 0:0:0')

NUM_THREADS_NA_IMPORTACAO = 16

logger = logging.getLogger("radar")

class ThreadFindProp(threading.Thread):
    """Executa a busca pelas proposições que estão na fila 'fila_entrada' usando multiprocessamento,
    o que garante o uso de vários cores e processadores e acelera muito o processo de encontrar e
    analisar as proposições.
    Ao fim da busca, caso a proposição exista, ela é adicionada à fila para depois ser gravada
    num arquivo de texto."""

    def __init__(self, fila_ids, fila_saida):
        threading.Thread.__init__(self)
        self.fila_saida = fila_saida
        self.fila_ids = fila_ids
        self.total_itens = fila_ids.qsize()

    def run(self):
        while True:
            id_candidato = None

            #recupera id da fila de entrada
            id_candidato = self.fila_ids.get()

            #Verifica a existência da proposição
            camaraws = Camaraws()
            prop = ProposicoesFinder()
            if (id_candidato % 10000) == 0: #< 500:
                processados = self.total_itens - self.fila_ids.qsize()
                sys.stdout.write('Itens Processados: %d\n Itens encontrados: %d\n Itens a processar: %d\n' %(processados, self.fila_saida.qsize(), self.fila_ids.qsize()))
                sys.stdout.flush()
                time.sleep(10)
            try:
                prop_xml = camaraws.obter_proposicao(id_candidato)
                nome_prop = prop._nome_proposicao(prop_xml)
                #Caso exista, salva na fila de saída
                self.fila_saida.put({id_candidato: nome_prop})
                #sys.stdout.write('.')
                #sys.stdout.flush()
                #logger.info('%d: %s' %(id_candidato, nome_prop))
            except ValueError:
                sys.stdout.write('')
                sys.stdout.flush()
                #logger.info('%d: x' %(id_candidato))

            #Avisa que a tarefa foi terminada
            #logger.debug('Encontrados: %d' %(self.fila_saida.qsize()))
            self.fila_ids.task_done()


class ProposicoesFinder:

    def __init__(self, verbose=True):
        self.verbose = verbose

    def _parse_nomes_lista_proposicoes(self, xml):
        """Recebe XML (objeto etree) do web service ListarProposicoes e devolve uma lista de tuplas,
        o primeiro item da tuple é o id da proposição, e o segundo item é o nome da proposição (sigla num/ano)
        """
        ids = []
        nomes = []
        for child in xml:
            id_prop = child.find('id').text.strip()
            nome = child.find('nome').text.strip()
            ids.append(id_prop)
            nomes.append(nome)
        return zip(ids, nomes)

    def _nome_proposicao(self, prop_xml):
        sigla = prop_xml.get('tipo').strip()
        numero = prop_xml.get('numero').strip()
        ano = prop_xml.get('ano').strip()
        return '%s %s/%s' % (sigla, numero, ano)

    def find_props_que_existem(self, file_name, ano_min=1988):
        """Retorna IDs de proposições que existem na câmara dos deputados.

        Buscas são feitas por proposições apresentadas desde ano_min, que por padrão é 1988, até o presente
        Não necessariamente todos os IDs possuem votações (na verdade a grande maioria não tem!).
        Se file_name == None, lança exceção TypeError

        Resultado é salvo no arquivo file_name.
        Cada linha possui o formato "id: sigla num/ano".
        """

        if file_name == None:
            raise TypeError('file_name não pode ser None')

        today = datetime.today()
        ano_max = today.year

        f = open(file_name,'a')
        f.write('# Arquivo gerado pela classe ProposicoesFinder\n')
        f.write('# para achar os IDs existentes na camara dos deputados\n')
        f.write('# Procurando ids entre %d e %d.\n' % (ano_min, ano_max))
        f.write('# id  : proposicao\n')
        f.write('#-----------\n')

        camaraws = Camaraws()
        siglas = camaraws.listar_siglas()
        for ano in range(ano_min, ano_max+1):
            logger.info('Procurando em %s' % ano)
            for sigla in siglas:
                try:
                    xml = camaraws.listar_proposicoes(sigla, ano)
                    props = self._parse_nomes_lista_proposicoes(xml)
                    for id_prop, nome in props:
                        f.write('%s: %s\n' %(id_prop, nome))
                    logger.info('%d %ss encontrados' % (len(props), sigla))
                except urllib2.URLError, etree.ParseError:
                    logger.info('access error in %s' % sigla)
                except:
                    logger.info('XML parser error in %s' % sigla)
        f.close()

    def find_props_que_existem_brute_force(self, file_name, id_min, id_max):
        """Retorna IDs de proposições que existem na câmara dos deputados.

        Buscas serão feitas por proposições com IDs entre id_min e id_max
        Não necessariamente todos os IDs possuem votações (na verdade a grande maioria não tem!).
        Se file_name == None, lança exceção TypeError

        Resultado é salvo no arquivo file_name.
        Cada linha possui o formato "id: sigla num/ano".
        """
        if file_name == None:
            raise TypeError('file_name não pode ser None')

        f = open(file_name,'w') # o arquivo aqui é aberto com 'w' pois ignorar-se-á o que havia anteriormente.
        f.write('# Arquivo gerado pela classe ProposicoesFinder\n')
        f.write('# para achar os IDs existentes na camara dos deputados\n')
        f.write('# Procurando ids entre %d e %d.\n' % (id_min, id_max))
        f.write('# id  : proposicao\n')
        f.write('#-----------\n')
        f.close()

        if self.verbose:
            print '"." id valido; "x" id invalido'

        # Na variável encontradas serão armazenadas as informações das proposições encontradas.
        # A variável é um dicionário que terá como chaves os id's das proposições encontradas e como valor o nome da proposição.
        # Ao final as informações desta variável serão gravadas no arquivo de texto acima.
        encontradas = Queue.Queue()
        fila_ids = Queue.Queue()

        #populando a fila com ids
        for id_candidato in range(id_min, id_max+1):
            fila_ids.put(id_candidato)

        #criando uma série de threads para tratarem as filas
        for i in range(1000):
            t = ThreadFindProp(fila_ids, encontradas)
            t.setDaemon(True)
            t.start()

            #aguarda até que a fila seja toda processada
        fila_ids.join()

        f = open(file_name,'a')
        while not encontradas.empty():
            encontrada = encontradas.get()
        f.write('%d: %s\n' %(encontrada.keys()[0],encontrada.values()[0]))
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
        with open(file_name, 'r') as f:
            for line in f:
                res = re.search(regexp, line)
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
                camaraws.obter_votacoes(prop['sigla'], prop['num'], prop['ano'])
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

    URL_PROPOSICAO = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=%s'
    URL_VOTACOES = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=%s&numero=%s&ano=%s'
    URL_LISTAR_PROPOSICOES = 'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoes?sigla=%s&numero=&ano=%s&datApresentacaoIni=&datApresentacaoFim=&autor=&parteNomeAutor=&siglaPartidoAutor=&siglaUFAutor=&generoAutor=&codEstado=&codOrgaoEstado=&emTramitacao='

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
        url = Camaraws.URL_PROPOSICAO % id_prop
        try:
            request = urllib2.Request(url)
            xml = urllib2.urlopen(request).read()
        except urllib2.URLError:
            raise ValueError('Proposicao %s nao encontrada' % id_prop)

        try:
            tree = etree.fromstring(xml)
        except etree.ParseError:
            raise ValueError('Proposicao %s nao encontrada' % id_prop)

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

        url  = Camaraws.URL_VOTACOES % (sigla, num, ano)
        try:
            request = urllib2.Request(url)
            xml = urllib2.urlopen(request).read()
        except urllib2.URLError:
            raise ValueError('Votacoes da proposicao %s %s/%s nao encontrada' % (sigla, num, ano))

        try:
            tree = etree.fromstring(xml)
        except etree.ParseError:
            raise ValueError('Votacoes da proposcaão %s %s/%s nao encontrada' % (sigla, num, ano))

        return tree

    def listar_proposicoes(self, sigla, ano):
        """Busca proposições de acordo com ano e sigla desejada

        Argumentos:
        sigla, ano -- strings que caracterizam as proposições buscadas

        Retorna:
        ElementTree correspondente ao XML retornado pelo web service
        Exemplo: http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoes?sigla=PL&numero=&ano=2011&datApresentacaoIni=14/11/2011&datApresentacaoFim=16/11/2011&autor=&parteNomeAutor=&siglaPartidoAutor=&siglaUFAutor=&generoAutor=&codEstado=&codOrgaoEstado=&emTramitacao=
        O retorno é uma lista de objetos Element sendo cara item da lista uma proposição encontrada

        Exceções:
            ValueError -- quando o web service não retorna um XML,
            que ocorre quando não há resultados para os critérios da busca
        """
        url = Camaraws.URL_LISTAR_PROPOSICOES % (sigla, ano)
        try:
            request = urllib2.Request(url)
            xml = urllib2.urlopen(request).read()
        except urllib2.URLError:
            raise ValueError('Proposicoes nao encontradas para sigla=%s&ano=%s' % (sigla, ano))

        try:
            tree = etree.fromstring(xml)
        except etree.ParseError:
            raise ValueError('Proposicoes nao encontradas para sigla=%s&ano=%s' % (sigla, ano))

        return tree

    def listar_siglas(self):
        """Listar as siglas de proposições existentes; exemplo: "PL", "PEC" etc
        O retorno é feito em uma lista de strings
        """
        # A lista completa se encontra aqui:
        # http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarSiglasTipoProposicao
        # No entanto, muito dessas siglas correspondem a proposições que não possuem votações
        # Por isso estamos aqui retornando um resultado mais restrito
        return ['PL', 'MPV', 'PDC', 'PEC', 'PLP', 'PLC', 'PLN', 'PLOA', 'PLS', 'PLV']


class VotadasParser:
    
    def __init__(self, votadas_file_path):
        self.votadas_file_path = votadas_file_path
    
    def parse_votadas(self):
        """Parse do arquivo self.votadas_file_path
        Retorna:
        Uma lista com a identificação das proposições encontradas no txt
        Cada posição da lista é um dicionário com chaves \in {id, sigla, num, ano}
        As chaves e valores desses dicionários são strings
        """
        # ex: "485262: MPV 501/2010"
        regexp = '^([0-9]*?): ([A-Z]*?) ([0-9]*?)/([0-9]{4})'
        proposicoes = []
        with open(self.votadas_file_path, 'r') as prop_file:
            for line in prop_file:
                res = re.search(regexp, line)
                if res:
                    proposicoes.append({'id':res.group(1), 'sigla':res.group(2), 'num':res.group(3), 'ano':res.group(4)})
        return proposicoes


LOCK_TO_CREATE_CASA = threading.Lock()

class ImportadorCamara:
    """Salva os dados dos web services da Câmara dos Deputados no banco de dados"""

    def __init__(self, votadas, verbose=False):
        """verbose (booleano) -- ativa/desativa prints na tela"""

        self.verbose = verbose
        self.votadas = votadas # id/sigla/num/ano das proposições que tiveram votações
        self.total = len(self.votadas)
        self.importadas = 0 # serve para indicar progresso
        self.partidos = {} # cache de partidos (chave é nome, e valor é objeto Partido)
        self.parlamentares = {} # cache de parlamentares (chave é 'nome-partido', e valor é objeto Parlamentar)

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
        """Gera objeto do tipo CasaLegislativa representando a Câmara dos Deputados e o salva no banco de dados.

            Caso cdep já exista no banco de dados, retorna o objeto já existente.
        """
        LOCK_TO_CREATE_CASA.acquire()
        if (models.CasaLegislativa.objects.filter(nome_curto='cdep').count() == 0):
            camara_dos_deputados = models.CasaLegislativa()
            camara_dos_deputados.nome = 'Câmara dos Deputados'
            camara_dos_deputados.nome_curto = 'cdep'
            camara_dos_deputados.esfera = models.FEDERAL
            camara_dos_deputados.atualizacao = ULTIMA_ATUALIZACAO
            camara_dos_deputados.save()
            LOCK_TO_CREATE_CASA.release()
            return camara_dos_deputados
        else:
            LOCK_TO_CREATE_CASA.release()
            return models.CasaLegislativa.objects.get(nome_curto='cdep')

    def _prop_from_xml(self, prop_xml, id_prop):
        """Recebe XML representando proposição (objeto etree)
        e devolve objeto do tipo Proposicao, que é salvo no banco de dados.
        Caso proposição já exista no banco, é retornada a proposição que já estava no banco.
        """
        try:
            query = models.Proposicao.objects.filter(id_prop=id_prop, casa_legislativa=self.camara_dos_deputados)
        except DatabaseError:
            # try again
            time.sleep(1)
            query = models.Proposicao.objects.filter(id_prop=id_prop, casa_legislativa=self.camara_dos_deputados)
            
        if query:
            prop = query[0]
        else:
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

    def _votacao_from_xml(self, votacao_xml, prop):
        """Salva votação no banco de dados.

        Atributos:
            votacao_xml -- XML representando votação (objeto etree)
            prop -- objeto do tipo Proposicao

        Retorna:
            objeto do tipo Votacao
        """
        descricao = 'Resumo: [%s]. ObjVotacao: [%s]' % (votacao_xml.get('Resumo'), votacao_xml.get('ObjVotacao'))
        data_str = votacao_xml.get('Data').strip()
        hora_str = votacao_xml.get('Hora').strip()
        date_time = self._converte_data(data_str, hora_str)

        query = models.Votacao.objects.filter(descricao=descricao, data=date_time, proposicao__casa_legislativa=self.camara_dos_deputados)
        if query:
            votacao = query[0]
        else:
            logger.info('Importando votação ocorrida em %s' % data_str)
            votacao = models.Votacao()
            votacao.descricao = descricao
            votacao.data = date_time
            votacao.proposicao = prop
            votacao.save()
            for voto_xml in votacao_xml.find('votos'):
                self._voto_from_xml(voto_xml, votacao)
            votacao.save()

        return votacao

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
            logger.warning('tipo de voto (%s) desconhecido! Mapeado como ABSTENCAO' % voto)
            return models.ABSTENCAO

    def _legislatura(self, voto_xml):
        """Salva legislatura no banco de dados.

        Atributos:
            voto_xml -- XML representando voto (objeto etree)

        Retorna:
            objeto do tipo Legislatura
        """
        partido = self._partido(voto_xml.get('Partido'))
        votante = self._votante(voto_xml.get('Nome'), partido.nome)

        # TODO filtrar tb por inicio e fim
        legs = models.Legislatura.objects.filter(parlamentar=votante,partido=partido,casa_legislativa=self.camara_dos_deputados)

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
        """Procura primeiro no cache e depois no banco; se não existir, cria novo partido"""
        nome_partido = nome_partido.strip()
        partido = self.partidos.get(nome_partido)
        if not partido:
            partido = models.Partido.from_nome(nome_partido)
            if partido == None:
                logger.warning('Não achou o partido %s; Usando "sem partido"' % nome_partido)
                partido = models.Partido.get_sem_partido()
            else:
                partido.save()
                self.partidos[nome_partido] = partido
                #logger.debug('Partido %s salvo' % partido)

        return partido

    def _votante(self, nome_dep, nome_partido):
        """Procura primeiro no cache e depois no banco; se não existir, cria novo parlamentar"""
        key = '%s-%s' % (nome_dep, nome_partido)
        parlamentar = self.parlamentares.get(key)
        if not parlamentar:
            parlamentares = models.Parlamentar.objects.filter(nome=nome_dep)
            if parlamentares:
                parlamentar = parlamentares[0]
                self.parlamentares[key] = parlamentar

        if not parlamentar:
            parlamentar = models.Parlamentar()
            parlamentar.nome = nome_dep
            #votante.id_parlamentar =
            #votante.genero =
            parlamentar.save()
            self.parlamentares[key] = parlamentar
            #logger.debug('Deputado %s salvo' % parlamentar)
        return parlamentar

    def _progresso(self):
        """Indica progresso na tela"""
        porctg = (int) (1.0*self.importadas / self.total * 100)
        logger.info('Progresso: %d / %d proposições (%d%%)' % (self.importadas, self.total, porctg))


    def importar(self):

        self.camara_dos_deputados = self._gera_casa_legislativa()

        f = lambda dic: ( dic['id'], dic['sigla'], dic['num'], dic['ano'] )
        for id_prop,sigla,num,ano in [ f(dic) for dic in self.votadas ]:

            logger.info('#################################################################')
            logger.info('Importando votações da PROPOSIÇÃO %s: %s %s/%s' % (id_prop, sigla, num, ano))

            camaraws = Camaraws()
            try:
                prop_xml = camaraws.obter_proposicao(id_prop)
                prop = self._prop_from_xml(prop_xml, id_prop)
                vots_xml = camaraws.obter_votacoes(sigla, num, ano)
    
                for child in vots_xml.find('Votacoes'):
                    self._votacao_from_xml(child, prop)
    
                self.importadas += 1
                self._progresso()
            except ValueError as e:
                logger.error('%s' % e)
        
        logger.info('### Fim da Importação das Votações das Proposições da Câmara dos Deputados.')


class SeparadorDeLista:
    
    def __init__(self, numero_de_listas):
        self.numero_de_listas = numero_de_listas
    
    def separa_lista_em_varias_listas(self, lista):
        lista_de_listas = []
        start = 0;
        chunk_size = (int) ( math.ceil( 1.0 * len(lista) / self.numero_de_listas ) ) 
        while start<len(lista):
            end = start+chunk_size
            if (end > len(lista)):
                end = len(lista)
            lista_de_listas.append(lista[start:end])
            start += chunk_size
        return lista_de_listas

class ImportadorCamaraThread(threading.Thread):

    def __init__(self, importer):
        threading.Thread.__init__(self)
        self.importer = importer
        
    def run(self):
        self.importer.importar()
        
def wait_threads(threads):
    for t in threads:
        t.join()    

def main():

    logger.info('IMPORTANDO DADOS DA CAMARA DOS DEPUTADOS')
    votadasParser = VotadasParser(VOTADAS_FILE_PATH)
    votadas = votadasParser.parse_votadas()
    separador = SeparadorDeLista(NUM_THREADS_NA_IMPORTACAO)
    listas_votadas = separador.separa_lista_em_varias_listas(votadas)
    threads = []
    for lista_votadas in listas_votadas:
        importer = ImportadorCamara(lista_votadas)
        thread = ImportadorCamaraThread(importer)
        threads.append(thread)
        thread.start()
    wait_threads(threads)
    logger.info('IMPORTACAO DE DADOS DA CAMARA DOS DEPUTADOS FINALIZADA')
    
    
    
