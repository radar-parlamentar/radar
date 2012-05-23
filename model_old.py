# -*- coding: utf-8 -*-

# Copyright (C) 2012, Leonardo Leite
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

"""Módulo model -- modelagem do domínio, baseado nos XMLs dos web services da câmara

Classes:
Partido -- modela um partido
Proposicao -- modela uma proposição parlamentar
Votacao -- modela uma votação pertencente à uma proposição parlamentar
Deputado -- modela o voto de um deputado numa votação
VotoPartido -- representa um conjunto de votos de um partido
VotoUF -- representa um conjunto de votos de uma UF (estado ou distrito federal)
""" 

from __future__ import unicode_literals
import xml.etree.ElementTree as etree
import io
import re
import sqlite3 as lite

SIM = 'Sim'
NAO = 'Não'
ABSTENCAO = 'Abstenção'
OBSTRUCAO = 'Obstrução' # interpretada como Abstenção

class Partido:
    """Modela um partido político
    Atributos:
    nome -- ex: 'PT' [string] 
    numero -- ex: '13' [string]
    """
#    Atributos a serem implementados no futuro:
#    tamanho [int], partido do governo (executivo)?[booleano], 
#    cargos_indicados (quantidade de cargos de indicação do executivo que esse partido possui - ministros/secretários)
#    Obs: como tamanho, partido do governo etc são características variáveis do partido, 
#    talvez seja melhor elas pertencerem a uma classe SituacaoPartido, que teria como atributos partido, periodo e as citadas

    def __init__(self, nome='', numero=''):
        self.nome = nome
        self.numero = numero

class Proposicao:
    """Modela uma proposição parlamentar
    Atributos:
    id, sigla, numero, ano, ementa, explicacao, situacao -- strings
    votacaoes -- lista de objetos do tipo Votacao
    """

    def __init__(self):
        self.id = ''
        self.sigla = ''
        self.numero = ''
        self.ano = ''
        self.ementa = ''
        self.explicacao = ''
        self.situacao = ''
        self.votacoes = []
    
    @staticmethod
    def fromxml(xml):
        """Transforma um texto XML em uma proposição
        Argumentos:
        xml -- string contendo o XML retornado do web service que retorna votações de uma proposição

        Retorna:
        Um objeto do tipo Proposicao
        """  
        tree = etree.fromstring(xml)
        prop = Proposicao()
        prop.sigla = tree.find('Sigla').text
        prop.numero = tree.find('Numero').text
        prop.ano = tree.find('Ano').text
        for child in tree.find('Votacoes'):
          vot = Votacao.fromtree(child)
          prop.votacoes.append(vot)
        return prop

    @staticmethod
    def fromxmlid(xml):
        """Transforma um texto XML do ObterProposicaoPorID em um string do tipo "sigla numero/ano"
        Argumentos:
        xml -- string contendo o XML retornado do web service que retorna proposição por id

        Retorna:
        string do tipo "sigla numero/ano", por exemplo fromxmlid(513512) retorna "MPV 540/2011"
        """  
        tree = etree.fromstring(xml)
        nome = tree.find('nomeProposicao').text
        return nome


    def __unicode__(self):
        return "[%s %s/%s]: %s \nEmenta: %s \nSituação: %s" % (self.sigla, self.numero, self.ano, self.explicacao, self.ementa, self.situacao) 

    def __str__(self):
        return unicode(self).encode('utf-8')

    def nome(self):
        return "%s %s/%s" % (self.sigla, self.numero, self.ano)

class Votacao:
    """Modela uma votação pertencente à uma proposição parlamentar
    Atributos:
    resumo, data, hora -- strings
    deputados -- lista de objetos do tipo Deputado
    """
    def __init__(self): 
        self.resumo = ''
        self.data = ''
        self.hora = ''
        self.deputados = []

    @staticmethod
    def fromtree(tree):
        """Transforma um XML em uma votação
        Argumentos:
        tree -- objeto do tipo xml.etree.ElementTree representando o XML que descreve uma votação

        Retorna:
        Um objeto do tipo Votacao
        """
        vot = Votacao() 
        vot.resumo = tree.attrib['Resumo']
        vot.data = tree.attrib['Data']
        vot.hora = tree.attrib['Hora']
        for child in tree:
          dep = Deputado.fromtree(child)
          vot.deputados.append(dep)
        return vot

    def por_partido(self):
        """Retorna votos agregados por partido
        Retorna:
        Um dicionário cuja chave é o nome do partido (string) e o valor é um VotoPartido
        """
        dic = {}
        for dep in self.deputados:
          part = dep.partido
          if not part in dic:
            dic[part] = VotoPartido(part)
          voto = dic[part]
          voto.add(dep.voto)
        return dic  
  
    def por_uf(self):
        """Retorna votos agregados por UF
        Retorna:
        Um dicionário cuja chave é o nome da UF (string) e o valor é um VotoUF
        """
        dic = {}
        for dep in self.deputados:
          uf = dep.uf
          if not uf in dic:
            dic[uf] = VotoUF(uf)
          voto = dic[uf]
          voto.add(dep.voto)
        return dic  

    def __unicode__(self):
        return "[%s, %s] %s" % (self.data, self.hora, self.resumo)

    def __str__(self):
        return unicode(self).encode('utf-8')

class Deputado:
    """Modela o voto de um deputado numa votação
    Atributos:
    nome, partido, uf -- strings que caracterizam o deputado
    voto -- voto dado pelo deputado \in {SIM, NAO, ABSTENCAO, OBSTRUCAO}

    Métodos estáticos: (O bd fica em 'resultados/camara.db')
    fromtree(tree) -- Transforma um XML em um objeto tipo Deputado.
    inicializar_dicpartidos() -- Copia tabela PARTIDOS do bd na variável Deputado.dicpartidos. Também usa informações do arquivo 'listapartidos.txt'.
    inicializar_diclistadeps() -- Copia tabela PARLAMENTARES do bd na variável Deputado.diclistadeps.
    idPartido(siglapartido) -- Retorna inteiro que identifica o partido segundo a tabela PARTIDOS do bd.
    idUF(siglauf) -- Retorna inteiro que identifica uma UF. Usar maiúsculas. Joga StandardError se UF não existir.
    idDep(nome,partido,uf) -- Retorna inteiro chamado idDep que identifica univocamente a tupla (nome,partido,uf) de acordo com a tabela PARLAMENTARES do bd.
    """
    listauf = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
    dicpartidos = dict() # chave é a sigla, valor é o idPartido, número que ele ganhou (que não é o número eleitoral, que não estamos usando porque está sujeito a mudar com o tempo)
    dicpartidos_inicializado = False
    diclistadeps = {}
    diclistadeps_inicializado = False

    def __init__(self):
        self.nome = ''
        self.partido = ''
        self.uf = ''
        self.voto = ''

    @staticmethod
    def fromtree(tree):
        """Transforma um XML no voto de um deputado
        Argumentos:
        tree -- objeto do tipo xml.etree.ElementTree representando o XML que descreve o voto de um deputado

        Retorna:
        Um objeto do tipo Deputado
        """
        dep = Deputado()
        dep.nome = tree.attrib['Nome']
        dep.partido = tree.attrib['Partido']
        dep.uf = tree.attrib['UF']
        dep.voto = tree.attrib['Voto']
        return dep

    def __unicode__(self):
        ufstr = ''
        if self.uf:
            ufstr = '-%s' % self.uf
        return "%s (%s%s) votou %s" % (self.nome, self.partido, ufstr, self.voto)

    def __str__(self):
        return unicode(self).encode('utf-8')

    @staticmethod
    def inicializar_dicpartidos(bd='resultados/camara.db'):
        """Lê no banco de dados 'resultados/camaraws.db' a tabela PARTIDOS, se presente, para inicializar a variável Deputado.dicpartidos com os partidos que ali constarem. Deputado.dicpartidos é um dicionário que tem como chave as siglas dos partidos e como valor o idPartido (identificador interno único, não necessariamente igual ao número eleitoral).

        Lê em seguida o arquivo listapartidos.txt que contém linhas do tipo 'PV 88' onde a sigla é a sigla de um partido e o número é um idPartido preferencial que pode ser escolhido pelo usuário, editando o arquivo manualmente. Se um partido de 'listapartidos.txt' já tiver sido encontrado no banco de dados com um idPartido diferente, prevalesce o do banco de dados, o do arquivo é ignorado, com emissão de uma mensagem de warning.

        Isso permite ao usuário escolher o idPartido que quer dar para cada partido, por exemplo fazendo-o coincidir com o número eleitoral. Permite também que bancos de dados criados em momentos diferentes acabem atribuindos idPartidos diferentes, o que não deveria ser um problema se os programas forem consistentes, mas poderia dificultar a localização de algum bug.

        Retorna 0 se a leitura for executada com sucesso, 1 se o arquivo listapartidos.txt não existir (ou não tiver permissão de leitura).
        """
        con = lite.connect(bd)
        if len(con.execute("select * from sqlite_master where type='table' and name='PARTIDOS'").fetchall()) != 0: # se tabela existe
            partsdb = con.execute('SELECT * FROM PARTIDOS').fetchall()
#            print partsdb
            for p in partsdb:
                Deputado.dicpartidos[p[1]] = p[0]
        file_listapartidos = 'listapartidos.txt'
        try:
            prop_file = open(file_listapartidos,'r')
        except IOError:
            return 1
        # ex: "PV 88"
        regexp = '([A-z_-]*)\s*(\d*)'
        for line in prop_file:
#            print line
            res = re.search(regexp,line)
            if res:
                siglawannabe = res.group(1)
                idwannabe = res.group(2)
                # verificar se ja tem, se sim warning, se nao acrescenta no bd e no dicpartidos
                if idwannabe in Deputado.dicpartidos.values():
                    if not Deputado.dicpartidos[siglawannabe] == idwannabe:
                        print "WARNING: listapartidos.txt associa o %s ao idPartido %s" % (siglawannabe,idwannabe)
                        print "mas no banco de dados este id ja esta associado ao %s." % (Deputado.dicpartidos[idwannabe])
                        print "Foi mantido o valor do banco de dados, e ignorado o de listapartidos.txt."
                elif siglawannabe in Deputado.dicpartidos:
                    if not Deputado.dicpartidos[siglawannabe] == idwannabe:
                        print "WARNING: listapartidos.txt associa o %s ao idPartido %s" % (siglawannabe,idwannabe)
                        print "mas no banco de dados o %s ja esta associado ao id %s." % (siglawannabe,Deputado.dicpartidos[siglawannabe])
                        print "Foi mantido o valor do banco de dados, e ignorado o de listapartidos.txt."
                else:
                    Deputado.dicpartidos[res.group(1)] = int(res.group(2))
                    con.execute("insert into PARTIDOS values(?,?)",(idwannabe,siglawannabe))
                    con.commit()
        con.close()
        return 0
    
    @staticmethod
    def inicializar_diclistadeps():
        """Lê no banco de dados 'resultados/camara.db' a tabela PARLAMENTARES, se presente, para inicializar a variável Deputado.diclistadeps com os deputados que ali constarem. Deputado.diclistadeps é um dicionário que tem como chave um inteiro de até cinco dígitos chamado idPartUF que identifica um par partido-UF, e como valor uma lista de deputados que pertencem a este partido-UF.
        """
        con = lite.connect('resultados/camara.db')
        if len(con.execute("select * from sqlite_master where type='table' and name='PARLAMENTARES'").fetchall()) != 0: # Se a tabela existe
            depsdb = con.execute('SELECT * FROM PARLAMENTARES').fetchall()
            con.close()
            for d in depsdb:
                iddep = d[0]
                idpartuf = int(iddep/1000)
                Deputado.diclistadeps[idpartuf] = [d[1]]
        return

    @staticmethod
    def idPartido(siglapartido, bd='resultados/camara.db'):
        """Retorna um inteiro que identifica o partido de acordo com a tabela PARTIDOS do bd.
        Se o partido não estiver na tabela, recebe um identificador novo, e é inserido na tabela.
        """
        if siglapartido in Deputado.dicpartidos:
            return Deputado.dicpartidos[siglapartido]
        else:
            if not Deputado.dicpartidos_inicializado:
                Deputado.inicializar_dicpartidos(bd)
                Deputado.dicpartidos_inicializado = True
                if siglapartido in Deputado.dicpartidos:
                    return Deputado.dicpartidos[siglapartido]
            # se chegou aqui, encontrou partido novo.
            idpartido = max(Deputado.dicpartidos.values()+[0]) + 1
            Deputado.dicpartidos[siglapartido] = idpartido
            print "Novo partido '%s' encontrado. Atribuido idPartido %d" % (siglapartido,idpartido)
            # colocar no banco de dados
            con = lite.connect(bd)
            con.execute('INSERT INTO PARTIDOS VALUES(?,?)',(idpartido,siglapartido))
            con.commit()
            con.close()
        return idpartido

    @staticmethod
    def idUF(siglauf):
        """Dada a sigla de uma unidade da federação (duas maiúsculas), retorna um inteiro entre 1 e 27 que a identifica univocamente, ou None se a sigla não for válida
        """
        try:
            iduf = Deputado.listauf.index(siglauf) + 1
            return iduf
        except:
            raise StandardError('UF %s nao existe. Obs: usar maiusculas.' % siglauf)

    @staticmethod
    def idDep(nome,partido,uf,bd='resultados/camara.db'):
        """Dado nome, partido e uf de um deputado, retorna um inteiro, chamado idDep, que o identifica univocamente, segundo a tabela PARLAMENTARES do bd.

        Deputados com mesmo nome mas filiação diferente são tratados como deputados distintos (pode acontecer no caso de mudança de partido).
        O idDep é construido de forma a ser suficiente para determinar partido e uf apenas olhando o número, pois tem a sintaxe: PPPEENNN, onde PPP é o idPartido, EE é o idUF e NNN é um número único para cada nome de deputado dentro de um partido-uf.
        Se o deputado não estiver ainda na tabela PARLAMENTARES do bd, ele ganha uma nova idDep, é inserido na tabela, e retorna-se o idDep recém atribuído.
        """
#        print Deputado.dicpartidos_inicializado
        if not Deputado.diclistadeps_inicializado:
            Deputado.inicializar_diclistadeps()
            Deputado.diclistadeps_inicializado = True

        iduf = '99' # usado quando UF não faz sentido (ex: câmara municipal)
        if uf:
            iduf = Deputado.idUF(uf)
        idPartUF = '%s%s' % (Deputado.idPartido(partido, bd), iduf)
        idPartUF = int(idPartUF)
        if idPartUF in Deputado.diclistadeps:
            if nome in Deputado.diclistadeps[idPartUF]:
                iddep = idPartUF*1000 + Deputado.diclistadeps[idPartUF].index(nome) + 1
                return iddep
            else:
                Deputado.diclistadeps[idPartUF].append(nome)
                iddep = idPartUF*1000 + Deputado.diclistadeps[idPartUF].index(nome) + 1
        else:
            Deputado.diclistadeps[idPartUF] = [nome]
            iddep = idPartUF*1000 + 1
        con = lite.connect(bd)
        con.execute('INSERT INTO PARLAMENTARES VALUES(?,?,?,?)',(iddep,nome,partido,uf))
        con.commit()
        con.close()
        return iddep



class VotosAgregados:
    """Representa um conjunto de votos
    Atributos:
    sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto
    """

    def add(self, voto):
        """Adiciona um voto ao conjunto de votos
        Argumentos:
        voto -- string \in {SIM, NAO, ABSTENCAO, OBSTRUCAO}
        OBSTRUCAO conta como um voto NAO
        """
        if (voto == SIM):
          self.sim += 1
        if (voto == NAO):
          self.nao += 1
        if (voto == OBSTRUCAO):
          self.nao += 1
        if (voto == ABSTENCAO):
          self.abstencao += 1

    def __init__(self):
        self.sim = 0
        self.nao = 0
        self.abstencao = 0

    def __unicode__(self):
        return '(%s, %s, %s)' % (self.sim, self.nao, self.abstencao)

    def __str__(self):
        return unicode(self).encode('utf-8')

class VotoPartido(VotosAgregados):
    """Representa um conjunto de votos de um partido
    Atributos:
    sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto
    partido -- string
    """
    def __init__(self, partido):
        VotosAgregados.__init__(self)
        self.partido = partido

class VotoUF(VotosAgregados):
    """Representa um conjunto de votos de uma UF (estado ou distrito federal)
    Atributos:
    sim, nao, abstencao -- inteiros que representam a quantidade de votos no conjunto
    uf -- string
    """
    def __init__(self, uf):
        VotosAgregados.__init__(self)
        self.uf = uf


