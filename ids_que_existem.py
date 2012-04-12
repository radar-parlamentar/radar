#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, Leonardo Leite, Diego Rabatone, Saulo Trento
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

"""Módulo ids_que_existem -- requisições para os Web Services da câmara, afim de determinar quais são as proposições que existem. Para fazer isso, a idéia é requisitar as proposições por id, tentando todos os ids de 0 até um número máximo (por exemplo 600000), e ver quais retornam proposições válidas. Isso é um pouco demorado mas só precisa ser rodado uma vez sempre que se desejar uma lista atualizada das proposições.

Funcões:
obter_votacao_porid -- dado o id, retorna o nome da proposição (tipo, num e ano), ou None se não houver dados.
"""

from model import Proposicao
import urllib2
import xml.etree.ElementTree as etree
import io

OBTER_INFOS_PORID = 'http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=%s'

def obter_votacao_porid(idprop):
    """Obtém nome da proposição dado o id.
    Por exemplo: obter_votacao_porid(513512) retorna o string "MPV 540/2011"

    Argumentos:
    idprop -- inteiro usado como identificador único de uma proposição no webservice

    Retorna:
    Uma string com tipo, número e ano da proposição, por exemplo "MPV 540/2011".
    Caso a proposição não seja encontrada, retorna None.
    Obs: Mesmo que a proposição seja encontrada, poderá ainda assim não possuir votações.
    """
    url = OBTER_INFOS_PORID % (idprop)
    try:
        request = urllib2.Request(url)
        xml = urllib2.urlopen(request).read()
    except urllib2.URLError:
        return None

    try:
        nomeprop = Proposicao.fromxmlid(xml)
    except:
        return None

    return nomeprop


if __name__ == "__main__":
    import sys
    if (len(sys.argv)<=1):

        xmin = 513100 # Valores default
        xmax = 513200

        print '# Usando valores default para id minimo e maximo'
        print '# a saber, entre %d e %d.' % (xmin,xmax)
        print '# Para outros valores, chame com argumentos,'
        print '# por exemplo entre 1 e 100999 usaria-se: $ ./listarid.py 1 100999'
    else:
        try:
            xmin = int(sys.argv[1])
            xmax = int(sys.argv[2])
            print '# Procurando ids entre %d e %d.' % (xmin,xmax)
        except:
            print 'ERRO de input: use dois argumentos inteiros'
            print '  o primeiro sendo o id minimo e o segundo o id maximo,'
            print '  ou chame sem argumentos para usar os valores padrao.'
            #(TODO: gestao decente de erros.)
            raise

    print '# id  : nome'
    print '#-----------'
    
    for x in range(xmin,xmax+1):
        p = obter_votacao_porid(x)
        txt = str(p)
        if not txt == 'None':
            print '%d: %s' %(x,txt)
