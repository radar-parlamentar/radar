# !/usr/bin/python
# coding=utf8

from __future__ import unicode_literals
from modelagem import models
import os
import xml.etree.ElementTree as etree
import logging

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger("radar")

class ImportadorChefesExecutivos:

    def __init__(self, nome_curto_casa, tag_cargo, tag_titulo, xml_file):
        self.casa = models.CasaLegislativa.objects.get(nome_curto=nome_curto_casa)
        self.tag_cargo = tag_cargo
        self.tag_titulo = tag_titulo
        self.xml_file = xml_file


    def importar_chefes(self):
        tree = self.abrir_xml()
        presidentes_tree = tree.find(self.tag_cargo)
        self.presidente_from_tree(presidentes_tree)


    def abrir_xml(self):
        xml_chefes = os.path.join(MODULE_DIR, self.xml_file)
        file = open(xml_chefes, 'r')
        xml = file.read()
        file.close()
        return etree.fromstring(xml)


    def presidente_from_tree(self, presidentes_tree):
        for presidente in presidentes_tree.getchildren():
            if presidente.tag == self.tag_titulo:
                nome = presidente.get('Nome')
                partido = presidente.get('Partido')
                ano_inicio = presidente.get('AnoInicio')
                ano_fim = presidente.get('AnoFinal')
                genero = presidente.get('Genero')
                self.criar_chefe_executivo(nome, partido, int(ano_inicio), int(ano_fim), genero)


    def criar_chefe_executivo(self, nome, sigla_partido, ano_inicio, ano_fim, genero):
        partido = models.Partido()
        partido = partido.from_nome(sigla_partido)

        chefe = models.ChefeExecutivo(nome=nome, partido=partido, mandato_ano_inicio=ano_inicio,
                                      mandato_ano_fim=ano_fim, genero=genero)

        chefe_existe = self.verificar_chefe_existe(chefe)
        if not chefe_existe:
            chefe.save()
            chefe.casas_legislativas.add(self.casa)
            logger.info('Adicionando chefe %s' % nome)
        else:
            logger.warn('Chefe %s já existe' % nome)


    def verificar_chefe_existe(self, chefe):
        chefes = models.ChefeExecutivo.objects.all()

        if chefes:
            for chefe_atual in chefes:
                nome_igual = chefe_atual.nome == chefe.nome
                partido_igual = chefe_atual.partido.pk == chefe.partido.pk
                ano_inicio_igual = chefe_atual.mandato_ano_inicio == chefe.mandato_ano_inicio
                ano_fim_igual = chefe_atual.mandato_ano_fim == chefe.mandato_ano_fim

                if (nome_igual and partido_igual and ano_inicio_igual and ano_fim_igual):
                    chefe_existe = True
                    break
            else:
                chefe_existe = False
        else:
            chefe_existe = False

        return chefe_existe