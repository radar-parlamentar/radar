#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, Saulo Trento, Leonardo Leite
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

"""módulo cria_bd 

Classes:
GeradorBD -- Cria um banco de dados sqlite3 a partir de proposições fornecidas (lista de objetos do tipo Proposicao) 

Funções:
cria_bd_camara_deputados -- Cria o banco de dados da câmara dos deputados em 'resultados/camara.db' a partir de requisições ao webservice da câmara pelas proposições elencadas no arquivo 'resultados/ids_que_existem.txt' (este último pode ser criado com o módulo ids_que_existem)

cira_bc_cmsp -- Cria o banco de dados da Câmara Municipal do Município de São Paulo a partir dos XMLs em resultados/cmsp[ano].xml
"""

from __future__ import unicode_literals
import cmsp
import proposicoes
import camaraws
import partidos
import sys
import re
import os
import model
import ids_que_existem
import sqlite3 as lite

class GeradorBD:
    """Cria um banco de dados sqlite3 a partir de proposições fornecidas (lista de objetos do tipo Proposicao)"""

    def __init__(self, proposicoes = [], db = "resultados/votos.db"):
        """ Argumentos:
        proposicoes - lista de objetos do tipo Proposicao
        db - string com a localização do banco de dados a ser gerado (default = "resultados/votos.db")
        """
        self.proposicoes = proposicoes
        self.db = db

    def arrumar_datas(self):
        con = lite.connect(self.db)
        with con:
            #cur = con.cursor()
            datas = con.execute("select idProp,idVot,data from VOTACOES;").fetchall()
            for v in datas:
                r = re.search('(\d*)/(\d*)/(\d*)',v[2])
                formato_sql = r.group(3).zfill(4) + '-' + r.group(2).zfill(2) + '-' + r.group(1).zfill(2)
                con.execute("update VOTACOES set data=? where idProp=?",(formato_sql,v[0]))
        con.close()
        return
            
    def _prepara_backup(self):
        os.system('rm %s.backup' % self.db) # Apagar backup anterior.
        os.system('mv %s %s.backup' % (self.db, self.db)) # Faz backup do bd antigo.
        os.system('rm %s' % self.db) # Apagar bd antigo para fazer um novo em folha.
        print 'resultados/camara.db renomeado para resultados/camara.db.backup'
        print 'Backup anterior, se havia, foi apagado.'

    def gera_bd(self):

        self._prepara_backup()

        print 'Entre parenteses, (id da proposicao,numero de votacoes).'
        print 'Proposicoes sem votacoes aparecem como um ponto.'

        numero_votacoes = [] # lista de ints que informa quantas votacoes cada proposicao da lista acima tem.

        con = lite.connect(self.db) # abrir conexão com bd.
        with con:
            cur = con.cursor()
            # Para criar tabela só se já não existir: create table if not exists TableName
            # Para testar se tabela existe: SELECT name FROM sqlite_master WHERE type='table' AND name='table_name';
            cur.execute("CREATE TABLE if not exists  PROPOSICOES(idProp INT, tipo TEXT, num TEXT, ano TEXT, ementa TEXT, explicacao TEXT, situacao TEXT, num_votacoes INT)")
            cur.execute("CREATE TABLE if not exists PARLAMENTARES(id INT, nome TEXT, partido TEXT, uf TEXT)")
            cur.execute("CREATE TABLE if not exists VOTACOES(idProp INT, idVot INT, resumo TEXT, data TEXT, hora TEXT, sim TEXT, nao TEXT, abstencao TEXT, obstrucao TEXT)")
            cur.execute("CREATE TABLE if not exists PARTIDOS(numero INT, nome TEXT)")
        con.close()

        for prop in self.proposicoes:
            numero_votacoes.append(len(prop.votacoes))
            sys.stdout.write('(%s,%d),'%(prop.id, len(prop.votacoes)))
            sys.stdout.flush()
            #adicionar proposicao na tabela PROPOSICOES
            con = lite.connect(self.db)
            con.execute("INSERT INTO PROPOSICOES VALUES(?,?,?,?,?,?,?,?)",(prop.id, prop.sigla, prop.numero, prop.ano, prop.ementa, prop.explicacao, prop.situacao, len(prop.votacoes)))
            con.commit()
            con.close()
            for v in prop.votacoes:
                print 'analisando votação %s' % v
                sim = []
                nao = []
                abstencao = []
                obstrucao = []
                for d in v.deputados:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    idDep = model.Deputado.idDep(d.nome, d.partido, d.uf, self.db)
                    if d.voto == model.SIM: 
                        sim.append(idDep)
                    if d.voto == model.NAO:
                        nao.append(idDep)
                    if d.voto == model.ABSTENCAO:
                        abstencao.append(idDep)
                    if d.voto == model.OBSTRUCAO:
                        obstrucao.append(idDep)
                print ' '
                pid = prop.id
                votid = prop.votacoes.index(v) + 1
                resum = v.resumo
                data = v.data
                hora = v.hora
                ssim = str(sim)
                snao = str(nao)
                sabs = str(abstencao)
                sobs = str(obstrucao)
                con = lite.connect(self.db)
                con.execute("INSERT INTO VOTACOES VALUES(?,?,?,?,?,?,?,?,?)",(pid, votid, resum, data, hora, ssim, snao, sabs, sobs))
                con.commit()
                con.close()

        self.arrumar_datas()

IDS_QUE_EXISTEM = 'resultados/ids_que_existem.txt'
IDS_VOTADAS = 'resultados/votadas.txt'
def cria_bd_camara_deputados(arquivo_ids=IDS_VOTADAS):
    """Cria o banco de dados da câmara dos deputados em 'resultados/camara.db'
        Argumentos:
        arquivo_ids -- arquivo com a listagem de "id: tipo num/ano" (uma entrada por linha, suportando comentários com #)
                        a função utilizará esses ids para realizar chamadas ao web service da câmara e obter as votações
                        o valor defualt é o arquivo IDS_VOTADAS; 
                        outro arquivo útil é o IDS_QUE_EXISTEM (que pode ser criado com o módulo ids_que_existem)
    """

    props = []
    lista_proposicoes = ids_que_existem.parse_txt(arquivo_ids)
    for iprop in lista_proposicoes:
        print 'AVALIANDO %s %s %s' % (iprop['tipo'],iprop['num'],iprop['ano'])
        p = camaraws.obter_votacao(iprop['tipo'], iprop['num'],iprop['ano']) # Obtém proposição e suas votações do web service
        if p != None:
            props.append(p)

    print 'Agora sim gerando o banco'
    gerador = GeradorBD(props, 'resultados/camara.db')
    gerador.gera_bd()

def cria_bd_cmsp():
    """Cria o banco de dados da câmara municipal de são paulo em 'resultados/cmsp.db' """

    props = cmsp.from_xml(cmsp.XML2010)   
    props += cmsp.from_xml(cmsp.XML2011)
    props += cmsp.from_xml(cmsp.XML2012)

    gerador = GeradorBD(props, 'resultados/cmsp.db')
    gerador.gera_bd()

if __name__ == "__main__":
    cria_bd_cmsp()    

