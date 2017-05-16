# !/usr/bin/python
# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Diego Rabatone, Saulo Trento,
# Carolina Ramalho, Brenddon Gontijo Furtado
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

"""módulo que cuida da importação dos dados da Câmara dos Deputados"""


from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist
from .chefes_executivos import ImportadorChefesExecutivos
from modelagem import models
from datetime import datetime
import re
import os
import xml.etree.ElementTree as etree
import urllib.request, urllib.error, urllib.parse
import logging
import threading
import math
import sys

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_FOLDER = os.path.join(MODULE_DIR, 'dados/cdep/')

ANO_MIN = 1991
# só serão buscadas votações a partir de ANO_MIN

logger = logging.getLogger("radar")

XML_FILE = 'dados/chefe_executivo/chefe_executivo_congresso.xml'
NOME_CURTO = 'cdep'


class Url(object):

    """Classe que abre urls"""

    def toXml(self, url):
        try:
            xml = self.read(url)
            tree = etree.fromstring(xml)
        except etree.ParseError as error:
            logger.error("etree.ParseError: %s" % error)
            return None
        return tree

    def read(self, url):
        text = ''
        try:
            request = urllib.request.Request(url)
            text = urllib.request.urlopen(request).read()
        except urllib.error.URLError as error:
            logger.error("%s ao acessar %s" % (error, url))
        except urllib.error.HTTPError:
            logger.error("%s ao acessar %s" % (error, url))
        return text


class Camaraws:

    """Acesso aos Web Services da Câmara dos Deputados"""
    URL_PROPOSICAO = 'http://www.camara.gov.br/sitcamaraws/' + \
        'Proposicoes.asmx/ObterProposicaoPorID?'
    URL_VOTACOES = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx' + \
        '/ObterVotacaoProposicao?'
    URL_LISTAR_PROPOSICOES = 'http://www.camara.gov.br/SitCamaraWS/' + \
        'Proposicoes.asmx/ListarProposicoes?'
    URL_PLENARIO = 'http://www.camara.gov.br/SitCamaraWS/' + \
        'Proposicoes.asmx/ListarProposicoesVotadasEmPlenario?'

    def __init__(self, url=Url()):
        self.url = url

    def _montar_url_consulta_camara(self, base_url, url_params, **kwargs):
        built_url = base_url

        for par in list(kwargs.keys()):
            if type(par) == str:
                kwargs[par] = kwargs[par].lower()

        for par in url_params:
            if par in list(kwargs.keys()):
                built_url += str(par) + "=" + str(kwargs[par]) + "&"
            else:
                built_url += str(par) + "=&"

        built_url = built_url.rstrip("&")
        return built_url

    def obter_proposicao_por_id(self, id_prop):
        """Obtém detalhes de uma proposição

        Argumentos:
        id_prop

        Retorna:
        Um objeto ElementTree correspondente ao XML retornado pelo web service
        Exemplo:
        http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=17338

        Exceções:
            ValueError -- quando proposição não existe
        """
        parametros_de_consulta = ["idprop"]
        args = {'idprop': id_prop}
        url = self._montar_url_consulta_camara(
            Camaraws.URL_PROPOSICAO, parametros_de_consulta, **args)
        tree = self.url.toXml(url)
        if tree is None or tree.tag == 'erro':
            raise ValueError('Proposicao %s nao encontrada' % id_prop)
        return tree

    def obter_votacoes(self, sigla, num, ano, **kwargs):
        """Obtém votacões de uma proposição

        Argumentos:
        sigla, num, ano -- strings que caracterizam a proposicão

        Retorna:
        Um objeto ElementTree correspondente ao XML retornado pelo web service
        Exemplo:
        http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterVotacaoProposicao?tipo=pl&numero=1876&ano=1999

        Exceções:
            ValueError -- quando proposição não existe ou não possui votações
        """
        parametros_de_consulta = ["tipo", "numero", "ano"]
        args = {'tipo': sigla, 'numero': num, 'ano': ano}
        if kwargs:
            args.update(kwargs)
        url = self._montar_url_consulta_camara(
            Camaraws.URL_VOTACOES, parametros_de_consulta, **args)
        tree = self.url.toXml(url)
        if tree is None or tree.tag == 'erro':
            raise ValueError(
                'Votacoes da proposicao %s %s/%s nao encontrada'
                % (sigla, num, ano))
        return tree

    def obter_proposicoes_votadas_plenario(self, ano):
        """Obtem as votações votadas em Plenario

        Argumentos:
        obrigatorio : ano

        Retorna:
        Um objeto ElementTree correspondente ao XML retornado pelo web service
        Exemplo:
        http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ListarProposicoesVotadasEmPlenario?ano=1991&tipo=
        """

        parametros_de_consulta = ["ano", "tipo"]
        args = {'ano': ano, 'tipo': ' '}
        url = self._montar_url_consulta_camara(
            Camaraws.URL_PLENARIO, parametros_de_consulta, **args)
        tree = self.url.toXml(url)
        if tree is None or tree.tag == 'erro':
            raise ValueError('O ano %s nao possui votacoes ainda' % ano)
        return tree

    def listar_proposicoes(self, sigla, ano, **kwargs):
        """Busca proposições de acordo com ano e sigla desejada

        Argumentos obrigatórios:
        sigla, ano -- strings que caracterizam as proposições buscadas

        Retorna:
        ElementTree correspondente ao XML retornado pelo web service
        Exemplo:
        http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoes?sigla=PL&numero=&ano=2011&datApresentacaoIni=14/11/2011&datApresentacaoFim=16/11/2011&autor=&parteNomeAutor=&siglaPartidoAutor=&siglaUFAutor=&generoAutor=&codEstado=&codOrgaoEstado=&emTramitacao=
        O retorno é uma lista de objetos Element sendo cara item da lista
        uma proposição encontrada

        Exceções:
            ValueError -- quando o web service não retorna um XML,
            que ocorre quando não há resultados para os critérios da busca
        """
        parametros_de_consulta = [
            "sigla", "numero", "ano", "datapresentacaoini",
            "datapresentacaofim", "idtipoautor", "partenomeautor",
            "siglapartidoautor", "siglaufautor", "generoautor", "codestado",
            "codorgaoestado", "emtramitacao"]
        args = {'sigla': sigla, 'ano': ano}
        if kwargs:
            args.update(kwargs)
        url = self._montar_url_consulta_camara(
            Camaraws.URL_LISTAR_PROPOSICOES, parametros_de_consulta, **args)
        tree = self.url.toXml(url)
        if tree is None or tree.tag == 'erro':
            raise ValueError(
                'Proposicoes nao encontradas para sigla=%s&ano=%s' %
                            (sigla, ano))
        return tree

    def listar_siglas(self):
        """Listar as siglas de proposições existentes; exemplo: "PL", "PEC" etc.
        O retorno é feito em uma lista de strings.
        """
        # A lista completa se encontra aqui:
        # http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ListarSiglasTipoProposicao
        # No entanto, muito dessas siglas correspondem a proposições que
        # não possuem votações
        # Por isso estamos aqui retornando um resultado mais restrito
        return ['PL', 'MPV', 'PDC', 'PEC', 'PLP',
                'PLC', 'PLN', 'PLOA', 'PLS', 'PLV']


class ProposicoesFinder:

    def find_props_disponiveis(self, ano_max=None, ano_min=ANO_MIN,
                               camaraws=Camaraws()):

        """Retorna uma lista com proposicoes que tiveram votações
        entre ano_min e ano_max.
        Cada votação é um dicionário com chaves \in {id, sigla, num, ano}.
        As chaves e valores desses dicionários são strings.

        ano_min padrão é 1991
        """
        if ano_max is None:
            ano_max = datetime.today().year
        proposicoes_votadas = []
        for ano in range(ano_max, ano_min - 1, -1):
            logger.info('Procurando em %s' % ano)
            try:
                xml = camaraws.obter_proposicoes_votadas_plenario(ano)
                proposicoes_votadas_no_ano = self._parse_xml(xml)
                proposicoes_votadas.extend(proposicoes_votadas_no_ano)
                logger.info('%d proposições encontradas' %
                            len(proposicoes_votadas_no_ano))
            except Exception as e:
                logger.error(e)
        return proposicoes_votadas

    def _parse_xml(self, xml):
        prop_votadas = []
        for child in xml:
            id_prop = child.find('codProposicao').text.strip()
            nome_prop = child.find('nomeProposicao').text.strip()
            dic_prop = self._build_dic(id_prop, nome_prop)
            prop_votadas.append(dic_prop)
        return prop_votadas

    def _build_dic(self, id_prop, nome_prop):
        sigla = nome_prop[0:nome_prop.index(" ")]
        num = nome_prop[nome_prop.index(" ") + 1: nome_prop.index("/")]
        ano = nome_prop[nome_prop.index("/") + 1: len(nome_prop)]
        return {'id': id_prop, 'sigla': sigla, 'num': num, 'ano': ano}


def _converte_data(data_str):
    """Converte string 'd/m/a' para objeto datetime.date;
    retona None se data_str é inválido
    """
    DATA_REGEX = '(\d\d?)/(\d\d?)/(\d{4})'
    dt = re.match(DATA_REGEX, data_str)
    if dt:
        new_str = '%s-%s-%s' % (
            dt.group(3), dt.group(2), dt.group(1))
        return parse_date(new_str)
    else:
        return None


class ImportadorCamara:
    """Salva os dados dos web services da
    Câmara dos Deputados no banco de dados"""

    def __init__(self, camaraws=Camaraws()):
        self.camara_dos_deputados = self._gera_casa_legislativa()
        self.parlamentares = self._init_parlamentares()
        self.proposicoes = self._init_proposicoes()
        self.votacoes = self._init_votacoes()
        self.camaraws = camaraws

    def _gera_casa_legislativa(self):
        """Gera objeto do tipo CasaLegislativa
        Câmara dos Deputados e o salva no banco de dados.
        Caso cdep já exista no banco de dados, retorna o objeto já existente.
        """
        count_cdep = models.CasaLegislativa.objects.filter(
            nome_curto='cdep').count()
        if not count_cdep:
            camara_dos_deputados = models.CasaLegislativa()
            camara_dos_deputados.nome = 'Câmara dos Deputados'
            camara_dos_deputados.nome_curto = 'cdep'
            camara_dos_deputados.esfera = models.FEDERAL
            camara_dos_deputados.save()
            return camara_dos_deputados
        else:
            return models.CasaLegislativa.objects.get(nome_curto='cdep')

    def _init_parlamentares(self):
        """(nome_parlamentar,nome_partido,localidade) -> Parlamentar"""
        parlamentares = {}
        for p in models.Parlamentar.objects.filter(
                casa_legislativa=self.camara_dos_deputados):
            parlamentares[self._key_parlamentar(p)] = p
        return parlamentares

    def _key_parlamentar(self, parlamentar):
        return (parlamentar.nome,
                parlamentar.partido.nome,
                parlamentar.localidade)

    def _init_proposicoes(self):
        """id_prop -> Proposicao"""
        proposicoes = {}
        for p in models.Proposicao.objects.filter(
                casa_legislativa=self.camara_dos_deputados):
            proposicoes[p.id_prop] = p
        return proposicoes

    def _init_votacoes(self):
        """(id_prop,descricao,data) -> Votacao"""
        votacoes = {}
        for v in models.Votacao.objects.filter(
                proposicao__casa_legislativa=self.camara_dos_deputados):
            votacoes[self._key_votacao(v)] = v
        return votacoes

    def _key_votacao(self, votacao):
        return (votacao.proposicao.id_prop, votacao.descricao, votacao.data)

    def importar(self, votadas):
        """votadas -- lista de dicionários com id/sigla/num/ano das proposições que tiveram votações
        """
        self.total_proposicoes = len(votadas)
        self.proposicoes_importadas = 0
        self.imprimir_quando_progresso = 5
        for dic in votadas:
            self._importar(dic)
            self._progresso()

    def _progresso(self):
        self.proposicoes_importadas += 1
        porcentagem = 100.0 * self.proposicoes_importadas / self.total_proposicoes
        if porcentagem > self.imprimir_quando_progresso:
            logger.info('Progresso: %.1f%%' % porcentagem)
            self.imprimir_quando_progresso += 5

    def _importar(self, dic_proposicao):
        """dic_proposicao -- dicionário com id/sigla/num/ano de uma proposição a ser importada
        """
        f = lambda dic: (dic['id'], dic['sigla'], dic['num'], dic['ano'])
        id_prop, sigla, num, ano = f(dic_proposicao)

        try:
            if id_prop in self.proposicoes:
                prop = self.proposicoes[id_prop]
            else:
                proposicao_xml = self.camaraws.obter_proposicao_por_id(id_prop)
                prop = self._prop_from_xml(proposicao_xml)

            votacoes_xml = self.camaraws.obter_votacoes(sigla, num, ano)
            for child in votacoes_xml.find('Votacoes'):
                self._votacao_from_xml(child, prop)
        except ValueError as error:
            logger.error("ValueError: %s" % error)

    def _prop_from_xml(self, prop_xml):
        """prop_xml -- tipo etree

        Retorna proposicao
        """
        id_prop = prop_xml.find('idProposicao').text.strip()
        prop = models.Proposicao()
        prop.id_prop = id_prop
        prop.sigla = prop_xml.get('tipo').strip()
        prop.numero = prop_xml.get('numero').strip()
        prop.ano = prop_xml.get('ano').strip()
        logger.info("Importando %s %s/%s" % (prop.sigla, prop.numero, prop.ano))
        prop.ementa = prop_xml.find('Ementa').text.strip()
        prop.descricao = prop_xml.find('ExplicacaoEmenta').text.strip()
        prop.indexacao = prop_xml.find('Indexacao').text.strip()
        prop.autor_principal = prop_xml.find('Autor').text.strip()
        date_str = prop_xml.find('DataApresentacao').text.strip()
        prop.data_apresentacao = _converte_data(date_str)
        prop.situacao = prop_xml.find('Situacao').text.strip()
        prop.casa_legislativa = self.camara_dos_deputados
        prop.save()
        self.proposicoes[id_prop] = prop
        return prop

    def _votacao_from_xml(self, votacao_xml, prop):
        """votacao_xml -- XML representando votação (objeto etree)
           prop -- objeto do tipo Proposicao
        """
        descricao = 'Resumo: [%s]. ObjVotacao: [%s]' % (
            votacao_xml.get('Resumo'), votacao_xml.get('ObjVotacao'))
        data_str = votacao_xml.get('Data').strip()
        data = _converte_data(data_str)

        key = (prop.id_prop, descricao, data)
        if key not in self.votacoes:
            votacao = models.Votacao()
            votacao.proposicao = prop
            votacao.descricao = descricao
            votacao.data = data
            votacao.save()
            self.votacoes[key] = votacao
            if votacao_xml.find('votos') is not None:
                for voto_xml in votacao_xml.find('votos'):
                    self._voto_from_xml(voto_xml, votacao)
            votacao.save()

    def _voto_from_xml(self, voto_xml, votacao):
        """voto_xml -- XML representando voto (objeto etree)
           votacao -- objeto do tipo Votacao
        """
        opcao_str = voto_xml.get('Voto')
        deputado = self._deputado(voto_xml)
        voto = models.Voto()
        voto.opcao = self._opcao_xml_to_model(opcao_str)
        voto.parlamentar = deputado
        voto.votacao = votacao
        voto.save()

    def _opcao_xml_to_model(self, voto):
        """Interpreta voto como tá no XML e responde em adequação a modelagem
        em models.py"""
        voto = voto.strip()
        if voto == 'Não':
            return models.NAO
        elif voto == 'Sim':
            return models.SIM
        elif voto == 'Obstrução':
            return models.OBSTRUCAO
        elif voto == 'Abstenção':
            return models.ABSTENCAO
        # presidente da casa não pode votar
        elif voto == 'Art. 17':
            return models.ABSTENCAO
        else:
            logger.warning(
                'opção de voto "%s" desconhecido! Mapeado como ABSTENCAO'
                % voto)
            return models.ABSTENCAO

    def _deputado(self, voto_xml):
        """Procura primeiro no cache e depois no banco; se não existir,
        cria novo parlamentar"""
        nome = voto_xml.get('Nome')
        nome_partido = voto_xml.get('Partido')
        partido = self._partido(nome_partido)
        localidade = voto_xml.get('UF')
        key = (nome, partido.nome, localidade)
        parlamentar = self.parlamentares.get(key)
        if not parlamentar:
            parlamentar = models.Parlamentar()
            parlamentar.id_parlamentar = voto_xml.get('ideCadastro')
            parlamentar.nome = nome
            parlamentar.partido = partido
            parlamentar.localidade = localidade
            parlamentar.casa_legislativa = self.camara_dos_deputados
            parlamentar.save()
            if partido.numero == 0:
                logger.warn('Não achou o partido %s' % nome_partido)
                logger.info('Deputado %s inserido sem partido' % nome)
            self.parlamentares[key] = parlamentar
        return parlamentar

    def _partido(self, nome_partido):
        nome_partido = nome_partido.strip()
        partido = models.Partido.from_nome(nome_partido)
        if partido is None:
            partido = models.Partido.get_sem_partido()
        return partido


class PosImportacao:

    def processar(self):
        self.remover_votacao_com_deputados_sem_partidos()

    # Issue #256
    def remover_votacao_com_deputados_sem_partidos(self):
        try:
            prop = models.Proposicao.objects.get(sigla='PL',
                                                 numero='821',
                                                 ano='1995')
            obj_votacao = 'SUBEMENDA A EMENDA N. 33'
            votacao = models.Votacao.objects.get(
                proposicao=prop, descricao__contains=obj_votacao)
            votacao.delete()
        except ObjectDoesNotExist:
            logger.warn('Votação esperada (em PL 821/1995)\
                        não foi encontrada na base de dados.')


# unesed!
# foi usado pra gerar algum dataset?
# se for o caso, melhor deixar em outro módulo.
def lista_proposicoes_de_mulheres():
    camaraws = Camaraws()
    prop_finder = ProposicoesFinder()
    importador = ImportadorCamara([''])
    importador.camara_dos_deputados = importador._gera_casa_legislativa()
    ano_min = 2012
    ano_max = 2013
    proposicoes = {}
    percentuais_fem = {}
    contagem_proposicoes = {}

    for ano in range(ano_min, ano_max + 1):
        proposicoes[ano] = {}
        contagem_proposicoes[ano] = {}
        proposicoes[ano]['F'] = []
        proposicoes[ano]['M'] = []
        contagem_proposicoes[ano]['F'] = []
        contagem_proposicoes[ano]['M'] = []
        contagem_proposicoes[ano]['somatotal'] = []

        for gen in ['F', 'M']:
            prop_ano_gen = prop_finder._parse_xml(
                camaraws.listar_proposicoes('PL', str(ano), **{
                    'generoautor': gen}))
            for prop in prop_ano_gen:
                prop_xml = camaraws.obter_proposicao_por_id(prop[0])
                proposicoes[ano][gen].append(
                    importador._prop_from_xml(prop_xml, prop[0]))

        contagem_proposicoes[ano]['mulheres'] = len(proposicoes[ano]['F'])
        contagem_proposicoes[ano]['homens'] = len(proposicoes[ano]['M'])
        contagem_proposicoes[ano]['somatotal'] = len(
            proposicoes[ano]['F']) + len(proposicoes[ano]['M'])

        percentuais_fem[ano] = 100 * float(
            contagem_proposicoes[ano]['F']) / float(contagem_proposicoes[
                                                    ano]['somatotal'])

    return {'proposicoes': proposicoes, 'contagem': contagem_proposicoes,
            'percentuais_fem': percentuais_fem}


def main():
    logger.info('IMPORTANDO DADOS DA CAMARA DOS DEPUTADOS')
    prop_finder = ProposicoesFinder()
    dic_votadas = prop_finder.find_props_disponiveis()
    importador = ImportadorCamara()
    importador.importar(dic_votadas)
    pos_importacao = PosImportacao()
    pos_importacao.processar()
    logger.info('IMPORTANDO CHEFES EXECUTIVOS DA CAMARA DOS DEPUTADOS')
    importer_chefe = ImportadorChefesExecutivos(NOME_CURTO, 'Presidentes', 'Presidente', XML_FILE)
    importer_chefe.importar_chefes()

    from importadores import cdep_genero
    cdep_genero.main()
    logger.info('IMPORTACAO DE DADOS DA CAMARA DOS DEPUTADOS FINALIZADA')
