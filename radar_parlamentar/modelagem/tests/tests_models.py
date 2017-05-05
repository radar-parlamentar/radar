# coding=utf8

# Copyright (C) 2012, Leonardo Leite, Eduardo Hideo, Diego Rabatone
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

from __future__ import unicode_literals
from django.test import TestCase
from importadores import conv
import datetime
import modelagem.models
import modelagem.utils
from util_test import flush_db
from django.utils.dateparse import parse_datetime
from modelagem.models import MUNICIPAL, FEDERAL, ESTADUAL, BIENIO
import logging
import datetime

logger = logging.getLogger("radar")

class ModelsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        importer = conv.ImportadorConvencao()
        importer.importar()

    @classmethod
    def tearDownClass(cls):
        flush_db(cls)


    ########################
    #### Classe Partido ####
    ########################

    def test_partido(self):
        pt = modelagem.models.Partido.from_nome('PT')
        self.assertEquals(pt.numero, 13)
        self.assertEquals(pt.cor, '#FF0000')
        psdb = modelagem.models.Partido.from_numero(45)
        self.assertEquals(psdb.nome, 'PSDB')
        self.assertEquals(psdb.cor, '#0059AB')
        pcdob = modelagem.models.Partido.from_nome('PC DO B')
        self.assertEquals(pcdob.numero, 65)
        dem = modelagem.models.Partido.from_nome('DEMOCRATAS')
        self.assertEquals(dem.nome, 'DEM')
        self.assertEquals(dem.numero, 25)

    def cria_chefes_executivo(self):
        pt = modelagem.models.Partido.from_nome('PT')
        chefe_masculino = modelagem.models.ChefeExecutivo(nome="Luiz Inacio Pierre da Silva", genero="M", partido = pt,
                                    mandato_ano_inicio = 1989, mandato_ano_fim = 1990)
        chefe_masculino.save()
        chefe_feminino = modelagem.models.ChefeExecutivo(nome="Dilmé Rouseffé", genero="F", partido = pt,
                                    mandato_ano_inicio = 1989, mandato_ano_fim = 1990)
        chefe_feminino.save()
        chefes = [chefe_masculino, chefe_feminino]
        return chefes

    def test_chefe_executivo_prefeito(self):
        chefes = self.cria_chefes_executivo()
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        casa.esfera = modelagem.models.MUNICIPAL
        casa.save()
        chefes[0].casas_legislativas.add(casa)
        expected =  "Prefeito: Luiz Inacio Pierre da Silva - PT"
        self.assertEquals(unicode(chefes[0]), expected)

    def test_chefe_executivo_presidenta(self):
        chefes = self.cria_chefes_executivo()
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        chefes[1].casas_legislativas.add(casa)
        expected = "Presidenta: Dilmé Rouseffé - PT"
        self.assertEquals(unicode(chefes[1]), expected)

    def test_chefe_executivo_prefeita(self):
        chefes = self.cria_chefes_executivo()
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        casa.esfera = modelagem.models.MUNICIPAL
        casa.save()
        chefes[1].casas_legislativas.add(casa)
        expected =  "Prefeita: Dilmé Rouseffé - PT"
        self.assertEquals(unicode(chefes[1]), expected)

    def test_chefe_executivo_presidente(self):
        chefes = self.cria_chefes_executivo()
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        chefes[0].casas_legislativas.add(casa)
        expected =  "Presidente: Luiz Inacio Pierre da Silva - PT"
        self.assertEquals(unicode(chefes[0]), expected)

    def test_partido_from_nome_None(self):
        nome_partido = None
        partido = modelagem.models.Partido.from_nome(nome_partido)
        self.assertIsNone(partido)

    def test_partido_from_nome(self):
        nome_partido = 'PT'
        partido = modelagem.models.Partido.from_nome(nome_partido)
        self.assertEquals(partido.nome, 'PT' )

    def test_partido_from_numero_None(self):
        numero_partido = None
        partido = modelagem.models.Partido.from_numero(numero_partido)
        self.assertIsNone(partido)

    def test_partido_from_numero(self):
        numero = 13
        partido = modelagem.models.Partido.from_numero(numero)
        self.assertEquals(partido.numero, 13)

    def test_get_sem_partido(self):
        partido = modelagem.models.Partido.get_sem_partido()
        self.assertEquals(partido.nome, 'Sem partido')
        self.assertEquals(partido.numero, 0)
        self.assertEquals(partido.cor, '#000000')


    #################################
    #### Classe Casa Legislativa ####
    #################################

    def test_partidos(self):
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        partidos = casa.partidos()
        self.assertEquals(len(partidos), 3)
        nomes = [p.nome for p in partidos]
        self.assertTrue(conv.JACOBINOS in nomes)
        self.assertTrue(conv.GIRONDINOS in nomes)
        self.assertTrue(conv.MONARQUISTAS in nomes)

    def test_parlamentares(self):
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        parlamentares = casa.parlamentares()
        self.assertEquals(len(parlamentares), 9)
        nomes = [p.nome for p in parlamentares]
        self.assertTrue('Pierre' in nomes)

    def test_num_votacao(self):
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        votacoes = casa.num_votacao(data_inicial='1990-01-01', data_final='1990-01-01')
        self.assertEquals(votacoes, 1)

    def test_num_votos(self):
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        votos = casa.num_votos(data_inicio='1990-01-01', data_fim='1990-01-01')
        self.assertEquals(votos, 9)
        
    def test_deleta_casa(self):

        partidoTest1 = modelagem.models.Partido()
        partidoTest1.nome = 'PA'
        partidoTest1.numero = '01'
        partidoTest1.cor = '#FFFAAA'
        partidoTest1.save()
        partidoTest2 = modelagem.models.Partido()
        partidoTest2.nome = 'PB'
        partidoTest2.numero = '02'
        partidoTest1.cor = '#FFFFFF'
        partidoTest2.save()

        casa_legislativaTest1 = modelagem.models.CasaLegislativa()
        casa_legislativaTest1.nome = 'Casa1'
        casa_legislativaTest1.nome_curto = 'cs1'
        casa_legislativaTest1.esfera = 'FEDERAL'
        casa_legislativaTest1.local = ''
        casa_legislativaTest1.save()
        casa_legislativaTest2 = modelagem.models.CasaLegislativa()
        casa_legislativaTest2.nome = 'Casa2'
        casa_legislativaTest2.nome_curto = 'cs2'
        casa_legislativaTest2.esfera = 'MUNICIPAL'
        casa_legislativaTest2.local = 'local2'
        casa_legislativaTest2.save()

        parlamentarTest1 = modelagem.models.Parlamentar()
        parlamentarTest1.id_parlamentar = ''
        parlamentarTest1.nome = 'Pierre'
        parlamentarTest1.genero = ''
        parlamentarTest1.casa_legislativa = casa_legislativaTest1
        parlamentarTest1.partido = partidoTest1
        parlamentarTest1.localidade = 'PB'
        parlamentarTest1.save()
        parlamentarTest2 = modelagem.models.Parlamentar()
        parlamentarTest2.id_parlamentar = ''
        parlamentarTest2.nome = 'Napoleao'
        parlamentarTest2.genero = ''
        parlamentarTest2.casa_legislativa = casa_legislativaTest2
        parlamentarTest2.partido = partidoTest2
        parlamentarTest2.localidade = 'PR'
        parlamentarTest2.save()

        proposicaoTest1 = modelagem.models.Proposicao()
        proposicaoTest1.id_prop = '0001'
        proposicaoTest1.sigla = 'PR1'
        proposicaoTest1.numero = '0001'
        proposicaoTest1.ano = '2013'
        proposicaoTest1.data_apresentacao = '2013-01-02'
        proposicaoTest1.casa_legislativa = casa_legislativaTest1
        proposicaoTest1.save()
        proposicaoTest2 = modelagem.models.Proposicao()
        proposicaoTest2.id_prop = '0002'
        proposicaoTest2.sigla = 'PR2'
        proposicaoTest2.numero = '0002'
        proposicaoTest2.ano = '2013'
        proposicaoTest2.data_apresentacao = '2013-02-02'
        proposicaoTest2.casa_legislativa = casa_legislativaTest2
        proposicaoTest2.save()

        votacaoTest1 = modelagem.models.Votacao(
            id_vot=' 12345', descricao='Teste da votacao',
            data='1900-12-05', resultado='Teste', proposicao=proposicaoTest1)
        votacaoTest1.save()

        votoTest1 = modelagem.models.Voto(
            votacao=votacaoTest1, parlamentar=parlamentarTest1, opcao='TESTE')
        votoTest1.save()

        antes_objetos_partido = modelagem.models.Partido.objects.all()
        antes_objetos_casa = modelagem.models.CasaLegislativa.objects.all()
        antes_objetos_parlamentar = modelagem.models.Parlamentar.objects.all()
        antes_objetos_proposicao = modelagem.models.Proposicao.objects.all()
        antes_objetos_voto = modelagem.models.Voto.objects.all()
        antes_objetos_votacao = modelagem.models.Votacao.objects.all()

        nomes_partido = [p.nome for p in antes_objetos_partido]
        self.assertTrue('PA' in nomes_partido)
        self.assertTrue('PB' in nomes_partido)

        nomes_parlamentar = [pl.nome for pl in antes_objetos_parlamentar]
        self.assertTrue('Pierre' in nomes_parlamentar)
        self.assertTrue('Napoleao' in nomes_parlamentar)

        nomes_casa = [c.nome for c in antes_objetos_casa]
        self.assertTrue('Casa1' in nomes_casa)
        self.assertTrue('Casa2' in nomes_casa)

        localidades = [p.localidade for p in antes_objetos_parlamentar]
        self.assertTrue('PB' in localidades)
        self.assertTrue('PR' in localidades)

        nomes_proposicao = [lg.sigla for lg in antes_objetos_proposicao]
        self.assertTrue('PR1' in nomes_proposicao)
        self.assertTrue('PR2' in nomes_proposicao)

        nomes_voto = [v.votacao for v in antes_objetos_voto]
        self.assertTrue(votacaoTest1 in nomes_voto)

        nomes_votacao = [vt.id_vot for vt in antes_objetos_votacao]
        self.assertTrue(' 12345' in nomes_votacao)

        # Tentando excluir uma casa que não existe
        modelagem.models.CasaLegislativa.deleta_casa('casa_qualquer')
        modelagem.models.CasaLegislativa.deleta_casa('cs1')

        depois_objetos_partido = modelagem.models.Partido.objects.all()
        depois_objetos_casa = modelagem.models.CasaLegislativa.objects.all()
        depois_objetos_parlamentar = modelagem.models.Parlamentar.objects.all()
        depois_objetos_proposicao = modelagem.models.Proposicao.objects.all()
        depois_objetos_voto = modelagem.models.Voto.objects.all()
        depois_objetos_votacao = modelagem.models.Votacao.objects.all()

        nomes_partido = [p.nome for p in depois_objetos_partido]
        self.assertTrue('PA' in nomes_partido)
        self.assertTrue('PB' in nomes_partido)

        nomes_parlamentar = [pl.nome for pl in depois_objetos_parlamentar]
        self.assertTrue('Pierre' in nomes_parlamentar)
        self.assertTrue('Napoleao' in nomes_parlamentar)

        nomes_casa = [c.nome for c in depois_objetos_casa]
        self.assertFalse('Casa1' in nomes_casa)
        self.assertTrue('Casa2' in nomes_casa)

        localidades = [p.localidade for p in depois_objetos_parlamentar]
        self.assertFalse('PB' in localidades)
        self.assertTrue('PR' in localidades)

        nomes_proposicao = [lg.sigla for lg in depois_objetos_proposicao]
        self.assertFalse('PR1' in nomes_proposicao)
        self.assertTrue('PR2' in nomes_proposicao)

        nomes_voto = [v.votacao for v in depois_objetos_voto]
        self.assertFalse(votacaoTest1 in nomes_voto)

        nomes_votacao = [vt.id_vot for vt in depois_objetos_votacao]
        self.assertFalse(' 12345' in nomes_votacao)


    ########################
    #### Classe Votacao ####
    ########################

    def test_uma_votacao_por_casa_legislativa(self):
        casa_legislativa = modelagem.models.CasaLegislativa.objects.get(
            nome_curto='conv')
        data_inicio = '1990-01-01'
        data_fim = '1990-01-01'
        votacoes = modelagem.models.Votacao.por_casa_legislativa(
            casa_legislativa, data_inicio, data_fim)
        self.assertEquals(1, len(votacoes))

    def test_nenhuma_votacao_por_casa_legislativa(self):
        casa_legislativa = modelagem.models.CasaLegislativa.objects.get(
            nome_curto='conv')
        data_inicio = '2010-01-01'
        data_fim = '2010-01-01'
        votacoes = modelagem.models.Votacao.por_casa_legislativa(
            casa_legislativa, data_inicio, data_fim)
        self.assertEquals(0, len(votacoes))  

    def test_votos(self):
        votacao = modelagem.models.Votacao.objects.get(descricao='Institui o Dia de Carlos Magno')
        votos = modelagem.models.Votacao.votos(votacao)
        self.assertEquals(len(votos), 9)
        votos_dos_parlamentares = [voto for voto in votos]
        #print votos_dos_parlamentares
       # self.assertFalse(models.SIM in votos_dos_parlamentares)
        #self.assertTrue(models.NAO in votos_dos_parlamentares)

    def test_por_casa_legislativa_e_periodo_com_datas_none(self):
        casa_legislativa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        data_inicial = None
        data_final = None
        resultado = modelagem.models.ChefeExecutivo.por_casa_legislativa_e_periodo(casa_legislativa, data_inicial, data_final)
        self.assertEquals(list(resultado), []) 

    #def test_por_casa_legislativa_e_periodo_com_datas(self):
        #casa_legislativa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        #chefes_executivo = modelagem.models.ChefeExecutivo.objects.filter(
        #data_inicio = datetime.date(1989, 1, 1)
        #data_fim = datetime.date(1990, 1, 1)
        #resultado = modelagem.models.ChefeExecutivo.por_casa_legislativa_e_periodo(casa_legislativa, data_inicio, data_fim)
        #print len(resultado)
        #self.assertEquals(list(resultado), []) 

    def test_get_chefe_anual(self):
        ano = 1989
        pt = modelagem.models.Partido.from_nome('PT')
        chefe_masculino = modelagem.models.ChefeExecutivo(nome="Luiz Inacio Pierre da Silva", genero="M", partido = pt,
                                    mandato_ano_inicio = 1989, mandato_ano_fim = 1990)
        chefe_masculino.save()
        chefe_feminino = modelagem.models.ChefeExecutivo(nome="Dilmé Rouseffé", genero="F", partido = pt,
                                    mandato_ano_inicio = 1991, mandato_ano_fim = 1992)
        chefe_feminino.save()
        chefes = [chefe_masculino, chefe_feminino]
        resultado = modelagem.models.ChefeExecutivo.get_chefe_anual(ano, chefes)
        self.assertEquals(len(resultado), 1)
        self.assertEquals(chefes[0].nome, "Luiz Inacio Pierre da Silva")        

    def test_get_chefe_periodo(self):
        ano_inicio = 1990
        ano_fim = 1992
        pt = modelagem.models.Partido.from_nome('PT')

        #teste ano_inicio_valido
        chefe1 = modelagem.models.ChefeExecutivo(nome="Luiz Inacio Pierre da Silva", genero="M", partido = pt,
                                    mandato_ano_inicio = 1989, mandato_ano_fim = 1991)
        chefe1.save()
        #teste ano_fim_valido
        chefe2 = modelagem.models.ChefeExecutivo(nome="Dilmé Rouseffé", genero="F", partido = pt,
                                    mandato_ano_inicio = 1991, mandato_ano_fim = 1992)
        chefe2.save()
        #teste mandato_ano_inicio_valido
        chefe3 = modelagem.models.ChefeExecutivo(nome="Jose Genuino", genero="M", partido = pt,
                                    mandato_ano_inicio = 1991, mandato_ano_fim = 1992)
        chefe3.save()
        #teste mandato_ano_fim_valido
        chefe4 = modelagem.models.ChefeExecutivo(nome="Joseh Gennuinno", genero="M", partido = pt,
                                    mandato_ano_inicio = 1990, mandato_ano_fim = 1991)
        chefe4.save()
        #teste falha
        chefe5 = modelagem.models.ChefeExecutivo(nome="Carlos Andrades", genero="M", partido = pt,
                                    mandato_ano_inicio = 1993, mandato_ano_fim = 1996)
        chefe5.save()
        chefes = [chefe1, chefe2, chefe3, chefe4, chefe5]
        resultado = modelagem.models.ChefeExecutivo.get_chefe_periodo(ano_inicio, ano_fim, chefes)
        self.assertEquals(len(resultado), 4)
        self.assertEquals(chefes[0].nome, "Luiz Inacio Pierre da Silva") 
        self.assertEquals(chefes[1].nome, "Dilmé Rouseffé") 
        self.assertEquals(chefes[2].nome, "Jose Genuino") 
        self.assertEquals(chefes[3].nome, "Joseh Gennuinno") 

    def test_get_titulo_chefe_masculino_municipal(self):
        pt = modelagem.models.Partido.from_nome('PT')
        chefe = modelagem.models.ChefeExecutivo(nome="Carlos Andrades", genero=modelagem.models.M, partido = pt,
                                    mandato_ano_inicio = 1993, mandato_ano_fim = 1996)
        chefe.save()
        chefes = [chefe]
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        casa.esfera = modelagem.models.MUNICIPAL
        casa.save()
        chefes[0].casas_legislativas.add(casa)
        titulo = chefes[0].get_titulo_chefe()
        self.assertEquals(titulo, "Prefeito")

    def test_get_titulo_chefe_feminino_federal(self):
        pt = modelagem.models.Partido.from_nome('PT')
        chefe = modelagem.models.ChefeExecutivo(nome="Dilmé Rouseffé", genero=modelagem.models.F, partido = pt,
                                    mandato_ano_inicio = 1993, mandato_ano_fim = 1996)
        chefe.save()
        chefes = [chefe]
        casa = modelagem.models.CasaLegislativa.objects.get(nome_curto='conv')
        casa.esfera = modelagem.models.FEDERAL
        casa.save()
        chefes[0].casas_legislativas.add(casa)
        titulo = chefes[0].get_titulo_chefe()
        self.assertEquals(titulo, "Presidenta")


    ###########################
    #### Classe Proposicao ####
    ###########################

    def test_nome(self):
        proposicao = modelagem.models.Proposicao.objects.get(id=1)
        proposicao.ano = "1990"
        resultado = proposicao.nome()
        self.assertEquals(resultado, "PL 1/1990")

    def test__unicode__proposicao(self):
        proposicao = modelagem.models.Proposicao.objects.get(id=1)
        resultado = proposicao.__unicode__()
        self.assertEquals(resultado, "[PL 1/] Reforma agrária")


    ###############################
    #### Classe VotosAgregados ####
    ###############################

    def test_add_sim(self):
        voto_agregado = modelagem.models.VotosAgregados()
        voto_agregado.add('SIM')
        voto_agregado.add('SIM')
        self.assertEquals(voto_agregado.sim, 2)

    def test_add_nao(self):
        voto_agregado = modelagem.models.VotosAgregados()
        voto_agregado.add('NAO')
        self.assertEquals(voto_agregado.nao, 1)

    def test_add_abstencao(self):
        voto_agregado = modelagem.models.VotosAgregados()
        voto_agregado.add('ABSTENCAO')
        voto_agregado.add('ABSTENCAO')
        voto_agregado.add('ABSTENCAO')
        self.assertEquals(voto_agregado.abstencao, 3)

    def test_add_obstrucao(self):
        voto_agregado = modelagem.models.VotosAgregados()
        voto_agregado.add('OBSTRUCAO')
        voto_agregado.add('ABSTENCAO')
        self.assertEquals(voto_agregado.abstencao, 2)

    def test_total(self):
        voto_agregado = modelagem.models.VotosAgregados()
        voto_agregado.add('OBSTRUCAO')
        voto_agregado.add('ABSTENCAO')
        voto_agregado.add('NAO')
        voto_agregado.add('SIM')
        total = voto_agregado.total()
        self.assertEquals(total, 4)

    def test_voto_medio_com_votos_sim_nao(self):
        voto_agregado = modelagem.models.VotosAgregados()
        voto_agregado.add('SIM')
        voto_agregado.add('NAO')
        voto_agregado.add('NAO')
        voto_agregado.add('SIM')
        total = voto_agregado.total()
        voto_medio = voto_agregado.voto_medio()
        self.assertEquals(voto_medio, 0.0)

    def test_voto_medio_votos_nulos(self):
        voto_agregado = modelagem.models.VotosAgregados()
        total = voto_agregado.total()
        voto_medio = voto_agregado.voto_medio()
        self.assertEquals(voto_medio, 0)
