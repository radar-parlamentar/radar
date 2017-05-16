# !/usr/bin/python
# coding=utf8


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

        self.salvar_chefe_executivo(chefe)


    def salvar_chefe_executivo(self, chefe):

        chefe_atual = self.get_chefe_executivo_do_banco(chefe) #chefe_atual é recebido para adicionarmos relacão com outra casa

        #Adiciona novo chefe ou adiciona casa a um chefe ja existente ou ignora chefe ja existente de acordo com chefe_existe
        if (chefe_atual):
            if self.verifica_casa_existe_no_chefe(chefe_atual):
                logger.warn('Chefe %s já existe' % chefe.nome)
            else:
                chefe_atual.casas_legislativas.add(self.casa)
                logger.info('Adicionando chefe %s em outra casa' % chefe_atual.nome)
        else:
            chefe.save()
            chefe.casas_legislativas.add(self.casa)
            logger.info('Adicionando chefe %s' % chefe.nome)


    def get_chefe_executivo_do_banco(self, chefe):
        chefe_banco = models.ChefeExecutivo.objects.filter(
            nome=chefe.nome,
            mandato_ano_inicio=chefe.mandato_ano_inicio,
            mandato_ano_fim=chefe.mandato_ano_fim)

        if chefe_banco and chefe_banco[0].partido.pk == chefe.partido.pk:
            return chefe_banco[0]
        else:
            return None


    def verifica_casa_existe_no_chefe(self, chefe_atual):

        for index in range(len(chefe_atual.casas_legislativas.all())):
            if(chefe_atual.casas_legislativas.all()[index] == self.casa): #Quer dizer que o chefe ja tem a casa atual
                return True
                break
        return False
