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
from importadores import convencao
from datetime import date
import models
import pdb

class ModelsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        importer = convencao.ImportadorConvencao()
        importer.importar()

    def test_partido(self):
        pt = models.Partido.from_nome('PT')
        self.assertEquals(pt.numero, 13)
        psdb = models.Partido.from_numero(45)
        self.assertEquals(psdb.nome, 'PSDB')
        
    def test_partido_from_nome_None(self):
        nome = None
        partido = models.Partido.from_nome(nome)
        self.assertIsNone(partido)

    def test_casa_legislativa_partidos(self):
        conv = models.CasaLegislativa.objects.get(nome_curto='conv')
        partidos = conv.partidos()
        self.assertEquals(len(partidos), 3)
        nomes = [ p.nome for p in partidos ]
        self.assertTrue(convencao.JACOBINOS in nomes)
        self.assertTrue(convencao.GIRONDINOS in nomes)
        self.assertTrue(convencao.MONARQUISTAS in nomes)

    def test_casa_legislativa_periodos(self):
        conv = models.CasaLegislativa.objects.get(nome_curto='conv')
        periodos = conv.periodos(models.ANO)
        self.assertEquals(len(periodos), 1)
        self.assertEqual(periodos[0].string, '1989')
        self.assertEqual(periodos[0].quantidade_votacoes,8)
        periodos = conv.periodos(models.MES)
        self.assertEquals(len(periodos), 9)
        self.assertEqual(periodos[0].string, '1989 Fev')
        self.assertEqual(periodos[0].quantidade_votacoes,4)
        self.assertEqual(periodos[1].string, '1989 Mar')
        self.assertEqual(periodos[1].quantidade_votacoes,0)
        periodos = conv.periodos(models.SEMESTRE)
        self.assertEquals(len(periodos), 2)
        d = periodos[0].ini
        self.assertEqual(1989, d.year)
        self.assertEqual(1, d.month)
        d = periodos[0].fim
        self.assertEqual(1989, d.year)
        self.assertEqual(6, d.month)
        d = periodos[1].ini
        self.assertEqual(1989, d.year)
        self.assertEqual(7, d.month)
        d = periodos[1].fim
        self.assertEqual(1989, d.year)
        self.assertEqual(12, d.month)
        self.assertEqual(periodos[0].string, '1989 1o Semestre')
        self.assertEqual(periodos[1].string, '1989 2o Semestre')
        periodos = conv.periodos(models.MES,numero_minimo_de_votacoes=1)
        self.assertEqual(len(periodos),2)
        
    def test_sould_find_legislatura(self):
        dt = date(1989, 07, 14)
        try:
            leg = models.Legislatura.find(dt, 'Pierre')
            self.assertTrue(leg != None)
        except ValueError:
            self.fail('Legislatura não encontrada')
            
    def test_sould_not_find_legislatura(self):
        dt = date(1900, 07, 14)
        try:
            models.Legislatura.find(dt, 'Pierre')
            self.fail('Legislatura não deveria ter sido encontrada')
        except:
            self.assertTrue(True)

    def test_deleta_casa(self):

    	partidoTest1 = models.Partido()
    	partidoTest1.nome = 'PA'
    	partidoTest1.numero = '01'
        partidoTest1.save()
        partidoTest2 = models.Partido()
    	partidoTest2.nome = 'PB'
    	partidoTest2.numero = '02'
        partidoTest2.save()
         
        parlamentarTest1 = models.Parlamentar()
    	parlamentarTest1.id_parlamentar = ''
    	parlamentarTest1.nome ='Pierre'
    	parlamentarTest1.genero = ''
        parlamentarTest1.save()
        parlamentarTest2 = models.Parlamentar()
    	parlamentarTest2.id_parlamentar = ''
    	parlamentarTest2.nome = 'Napoleao'
    	parlamentarTest2.genero = ''
        parlamentarTest2.save()
    	
        casa_legislativaTest1 = models.CasaLegislativa()
    	casa_legislativaTest1.nome= 'Casa1'
    	casa_legislativaTest1.nome_curto = 'cs1'
    	casa_legislativaTest1.esfera = 'FEDERAL'
        casa_legislativaTest1.local = ''
    	casa_legislativaTest1.atualizacao = '2012-06-01'
    	casa_legislativaTest1.save()
        casa_legislativaTest2 = models.CasaLegislativa()
    	casa_legislativaTest2.nome='Casa2'
    	casa_legislativaTest2.nome_curto='cs2'
    	casa_legislativaTest2.esfera = 'MUNICIPAL'
        casa_legislativaTest2.local = 'local2'
    	casa_legislativaTest2.atualizacao = '2012-12-31'
        casa_legislativaTest2.save()

    	legislaturaTest1 = models.Legislatura()
    	legislaturaTest1.parlamentar=parlamentarTest1
    	legislaturaTest1.casa_legislativa = casa_legislativaTest1
    	legislaturaTest1.inicio='2013-01-01'
    	legislaturaTest1.fim='2013-02-01'
    	legislaturaTest1.partido=partidoTest1
    	legislaturaTest1.localidade='PB'
    	legislaturaTest1.save()
    	legislaturaTest2 = models.Legislatura()
    	legislaturaTest2.parlamentar=parlamentarTest2
    	legislaturaTest2.casa_legislativa = casa_legislativaTest2
    	legislaturaTest2.inicio='2013-01-02'
    	legislaturaTest2.fim='2013-02-02'
    	legislaturaTest2.partido=partidoTest2
    	legislaturaTest2.localidade='PR'
    	legislaturaTest2.save()

    	proposicaoTest1= models.Proposicao()
    	proposicaoTest1.id_prop ='0001'
        proposicaoTest1.sigla = 'PR1'
        proposicaoTest1.numero = '0001'
        proposicaoTest1.ano = '2013'
        proposicaoTest1.data_apresentacao = '2013-01-02'
        proposicaoTest1.casa_legislativa = casa_legislativaTest1
    	proposicaoTest1.save()
    	proposicaoTest2= models.Proposicao()
    	proposicaoTest2.id_prop ='0002'
        proposicaoTest2.sigla = 'PR2'
        proposicaoTest2.numero = '0002'
        proposicaoTest2.ano = '2013'
        proposicaoTest2.data_apresentacao = '2013-02-02'
        proposicaoTest2.casa_legislativa = casa_legislativaTest2
    	proposicaoTest2.save()

    	votacaoTest1 = models.Votacao(id_vot = ' 12345',descricao = 'Teste da votacao',data = '1900-12-05',resultado = 'Teste',proposicao = 		proposicaoTest1)
    	votacaoTest1.save()		
      
      	votoTest1 = models.Voto(votacao = votacaoTest1,legislatura = legislaturaTest1,opcao = 'TESTE' )
      	votoTest1.save()
    	
    	antes_objetos_partido=models.Partido.objects.all()
    	antes_objetos_parlamentar=models.Parlamentar.objects.all()
    	antes_objetos_casa=models.CasaLegislativa.objects.all()
    	antes_objetos_legislatura=models.Legislatura.objects.all()
    	antes_objetos_proposicao=models.Proposicao.objects.all()
    	antes_objetos_voto=models.Voto.objects.all()
    	antes_objetos_votacao=models.Votacao.objects.all()

        nomes_partido = [p.nome for p in antes_objetos_partido]
        self.assertTrue('PA' in nomes_partido)
        self.assertTrue('PB' in nomes_partido)

        nomes_parlamentar = [pl.nome for pl in antes_objetos_parlamentar]
        self.assertTrue('Pierre' in nomes_parlamentar)
        self.assertTrue('Napoleao' in nomes_parlamentar)

    	nomes_casa = [c.nome for c in antes_objetos_casa]
        self.assertTrue('Casa1' in nomes_casa)
        self.assertTrue('Casa2' in nomes_casa)

    	nomes_legislatura = [l.localidade for l in antes_objetos_legislatura]
        self.assertTrue('PB' in nomes_legislatura)
        self.assertTrue('PR' in nomes_legislatura)

    	nomes_proposicao = [lg.sigla for lg in antes_objetos_proposicao]
        self.assertTrue('PR1' in nomes_proposicao)
        self.assertTrue('PR2' in nomes_proposicao)

    	nomes_voto = [v.votacao for v in antes_objetos_voto]
        self.assertTrue(votacaoTest1 in nomes_voto)

    	nomes_votacao = [vt.id_vot for vt in antes_objetos_votacao]
        self.assertTrue(' 12345' in nomes_votacao)

        
        models.CasaLegislativa.deleta_casa('casa_qualquer')#Tentando excluir uma casa que não existe
        models.CasaLegislativa.deleta_casa('cs1')
    	
        

        depois_objetos_partido=models.Partido.objects.all()
    	depois_objetos_parlamentar=models.Parlamentar.objects.all()
    	depois_objetos_casa=models.CasaLegislativa.objects.all()
    	depois_objetos_legislatura=models.Legislatura.objects.all()
    	depois_objetos_proposicao=models.Proposicao.objects.all()
    	depois_objetos_voto=models.Voto.objects.all()
    	depois_objetos_votacao=models.Votacao.objects.all()

    	nomes_partido = [p.nome for p in depois_objetos_partido]
        self.assertTrue('PA' in nomes_partido)
        self.assertTrue('PB' in nomes_partido)

    	nomes_parlamentar = [pl.nome for pl in depois_objetos_parlamentar]
        self.assertTrue('Pierre' in nomes_parlamentar)
        self.assertTrue('Napoleao' in nomes_parlamentar)

        nomes_casa = [c.nome for c in depois_objetos_casa]
        self.assertFalse('Casa1' in nomes_casa)
        self.assertTrue('Casa2' in nomes_casa)

    	nomes_legislatura = [l.localidade for l in depois_objetos_legislatura]
        self.assertFalse('PB' in nomes_legislatura)
        self.assertTrue('PR' in nomes_legislatura)

    	nomes_proposicao = [lg.sigla for lg in depois_objetos_proposicao]
        self.assertFalse('PR1' in nomes_proposicao)
        self.assertTrue('PR2' in nomes_proposicao)

    	nomes_voto = [v.votacao for v in depois_objetos_voto]
        self.assertFalse(votacaoTest1 in nomes_voto)

    	nomes_votacao = [vt.id_vot for vt in depois_objetos_votacao]
        self.assertFalse(' 12345' in nomes_votacao)


