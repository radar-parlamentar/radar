# -*- coding: utf-8 -*-
# Copyright (C) 2015,
# Diego Rabatone Oliveira, Matheus Fonseca, Brenddon Gontijo Furtado
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

"""Módulo responsável por importar dados de gênero da CDEP"""


from io import StringIO
from modelagem import models

import xml.etree.ElementTree as etree
import zipfile
import urllib.request, urllib.error, urllib.parse
import logging

logger = logging.getLogger("radar")


def abrir_xml_zipado(url=None):
    xml = None
    try:
        xml_zip_text = _faz_download_arquivo_zipado(url)

        xml_zip_file = StringIO()
        xml_zip_file.write(xml_zip_text)

        xml_zip = zipfile.ZipFile(xml_zip_file)
        xml_file_name = xml_zip.namelist()[0]  # pega só o primeiro arquivo
        xml_text = xml_zip.read(xml_file_name)

        xml = etree.fromstring(xml_text)
    except (etree.ParseError, zipfile.BadZipfile) as e:
        logger.info('%s: %s' % (e.__class__.__name__, e))

    return xml


def _faz_download_arquivo_zipado(url):
    text = ''
    try:
        text = urllib.request.urlopen(url).read()
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        logger.info('%s: %s' % (e.__class__.__name__, e))

    return text


def insere_genero_parlamentares_camara():
    URL_DADOS_CDEP = 'http://www.camara.leg.br/internet/deputado/'
    ARQ_DADOS_CDEP = 'DeputadosXML_52a55.zip'
    xml = abrir_xml_zipado(url=URL_DADOS_CDEP + ARQ_DADOS_CDEP)

    lista_parlamentares_xml = xml[0]

    for parlamentar_xml in lista_parlamentares_xml:
        # Buscando conteúdos das tags nomeParlamentar e SEXO.
        nome_parlamentar_xml = parlamentar_xml.find('nomeParlamentar').text
        sexo_parlamentar_xml = parlamentar_xml.find('SEXO').text

        # Transformando nome do parlamentar no formato title do Python.
        nome_parlamentar_xml = str(
            nome_parlamentar_xml).title().encode('utf-8')

        lista_parlamentar_banco = models.Parlamentar.objects.filter(
            nome=nome_parlamentar_xml)

        for parlamentar_banco in lista_parlamentar_banco:
            if parlamentar_banco.genero == '' or \
                    parlamentar_banco.genero is None:
                parlamentar_banco.genero = sexo_parlamentar_xml
                parlamentar_banco.save()

                string_log = 'Genero de {0} \
                    alterado com sucesso!'.decode().encode('utf-8')
                string_log = string_log.format(nome_parlamentar_xml)
                logger.debug(string_log)


def main():
    insere_genero_parlamentares_camara()
    logger.info('Generos dos parlamentares da Camara alterados com sucesso!')
