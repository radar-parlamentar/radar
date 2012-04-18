#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, Leonardo Leite, Saulo Trento
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

"""Script cria_bd -- Cria um banco de dados sqlite3 em 'resultados/camara.db' a partir de requisições ao webservice da câmara pelas proposições elencadas no arquivo 'resultados/ids_que_existem.txt' (este último pode ser criado com o módulo ids_que_existem)
"""

import proposicoes
import camaraws
import partidos
import sys
import re
import os
import model
import ids_que_existem
import sqlite3 as lite


if __name__ == "__main__":

    os.system('rm resultados/camara.db.backup') # Apagar backup anterior.
    os.system('mv resultados/camara.db resultados/camara.db.backup') # Faz backup do bd antigo.
    os.system('rm resultados/camara.db') # Apagar bd antigo para fazer um novo em folha.

    print 'resultados/camara.db renomeado para resultados/camara.db.backup'
    print 'Backup anterior, se havia, foi apagado.'
    print 'Entre parenteses, (id da proposicao,numero de votacoes).'
    print 'Proposicoes sem votacoes aparecem como um ponto.'

    proposicoes = [] # lista de objetos da classe model.Proposicao.
    numero_votacoes = [] # lista de ints que informa quantas votacoes cada proposicao da lista acima tem.

    lista_proposicoes = ids_que_existem.parse_txt('resultados/ids_que_existem.txt')
    con = lite.connect('resultados/camara.db') # abrir conexão com bd.
    with con:
        cur = con.cursor()
        # Para criar tabela só se já não existir: create table if not exists TableName
        # Para testar se tabela existe: SELECT name FROM sqlite_master WHERE type='table' AND name='table_name';
        cur.execute("CREATE TABLE if not exists  PROPOSICOES(idProp INT, tipo TEXT, num TEXT, ano TEXT, ementa TEXT, explicacao TEXT, situacao TEXT, num_votacoes INT)")
        cur.execute("CREATE TABLE if not exists DEPUTADOS(idDep INT, deputado TEXT, partido TEXT, uf TEXT)")
        cur.execute("CREATE TABLE if not exists VOTACOES(idProp INT, idVot INT, resumo TEXT, data TEXT, hora TEXT, sim TEXT, nao TEXT, abstencao TEXT, obstrucao TEXT)")
        cur.execute("CREATE TABLE if not exists PARTIDOS(idPart INT, partido TEXT)")
    con.close()

    for iprop in lista_proposicoes:
        #print 'AVALIANDO %s %s %s' % (iprop['tipo'],iprop['num'],iprop['ano'])
        p = camaraws.obter_votacao(iprop['tipo'], iprop['num'],iprop['ano']) # Obtém proposição e suas votações do web service
        if p != None:
            proposicoes.append(p)
            numero_votacoes.append(len(p.votacoes))
            #print 'Houveram votacoes. Votacoes encontradas: %d' % (len(p.votacoes))
            sys.stdout.write('(%s,%d),'%(iprop['id'],len(p.votacoes)))
            sys.stdout.flush()
            #adicionar proposicao na tabela PROPOSICOES
            con = lite.connect('resultados/camara.db')
            con.execute("INSERT INTO PROPOSICOES VALUES(?,?,?,?,?,?,?,?)",(p.id,p.sigla,p.numero,p.ano,p.ementa,p.explicacao,p.situacao,len(p.votacoes)))
            con.commit()
            con.close()
            for v in p.votacoes:
                sim = []
                nao = []
                abstencao = []
                obstrucao = []
                for d in v.deputados:
                    idDep = model.Deputado.idDep(d.nome,d.partido,d.uf)
                    if d.voto[0] == 'S':
                        sim.append(idDep)
                    if d.voto[0] == 'N':
                        nao.append(idDep)
                    if d.voto[0] == 'A':
                        abstencao.append(idDep)
                    if d.voto[0] == 'O':
                        obstrucao.append(idDep)
                pid = p.id
                votid = p.votacoes.index(v) + 1
                resum = v.resumo
                data = v.data
                hora = v.hora
                ssim = str(sim)
                snao = str(nao)
                sabs = str(abstencao)
                sobs = str(obstrucao)
                con = lite.connect('resultados/camara.db')
                con.execute("INSERT INTO VOTACOES VALUES(?,?,?,?,?,?,?,?,?)",(pid, votid, resum, data, hora, ssim, snao, sabs, sobs))
                con.commit()
                con.close()
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
