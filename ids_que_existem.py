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

"""Módulo ids_que_existem -- Faz requisições para os Web Services da câmara, afim de determinar quais são as proposições que existem. Para fazer isso, a idéia é requisitar as proposições por id, tentando todos os ids de 0 até um número máximo (por exemplo 600000), e ver quais retornam proposições válidas. Isso é um pouco demorado mas só precisa ser rodado uma vez sempre que se desejar uma lista atualizada das proposições.

O método cria_txt(file_name,xmin,xmax) escreve no arquivo file_name uma linha para cada id válido, no formato exemplificado abaixo:
513512: MPV 540/2011
Ou seja, o id seguido do nome da proposição.
Se o argumento file_name for igual a 'stdout', a saída é simplesmente mandada para stdout, e não para um arquivo.

O método parse_txt(file_name) lê o arquivo (por exemplo 'resultados/ids_que_existem.txt') e retorna uma lista de dicionários com chaves \in {id, tipo, num, ano} , representando as proposições encontradas.

Contém script como envelope para cria_txt(), que pode ser chamado com o primeiro argumento sendo xmin e o segundo xmax para escrever a saída em stdout, ou com um terceiro argumento contendo o nome do arquivo no qual escrever.
"""

from model import Proposicao
import urllib2
import xml.etree.ElementTree as etree
import io
import camaraws
import sys
import re

def parse_txt(file_name):
    """Parse de arquivo criado por ids_que_existem.cria_txt(filename) (por exemplo resultados/ids_que_existem.txt)
    Retorna:
    Uma lista com a identificação das proposições encontradas no txt
    Cada posição da lista é um dicionário com chaves \in {id, tipo, num, ano}
    As chaves e valores desses dicionários são strings
    """
#    file_name = 'resultados/ids_que_existem.txt'  # arquivo contem proposições. Não necessariamente todas foram votadas.
    prop_file = open(file_name, 'r')
    # ex: "485262: MPV 501/2010"
    regexp = '^([0-9]*?): ([A-Z]*?) ([0-9]*?)/([0-9]{4})'
    proposicoes = []
    for line in prop_file:
        res = re.search(regexp, line)
        if res:
            proposicoes.append({'id':res.group(1), 'tipo':res.group(2), 'num':res.group(3), 'ano':res.group(4)})
    return proposicoes

def cria_txt(file_name,xmin,xmax):

    if file_name == 'stdout':
        print '# Procurando ids entre %d e %d.' % (xmin,xmax)
        print '# id  : nome'
        print '#-----------'
        
        for x in range(xmin,xmax+1):
            p = camaraws.obter_nomeProp_porid(x)
            txt = str(p)
            if not txt == 'None':
                print '%d: %s' %(x,txt)
    else:
        f = open(file_name,'w')
        linha = '# Procurando ids entre %d e %d.\n' % (xmin,xmax)
        f.write(linha)
        f.write('# id  : nome\n')
        f.write('#-----------\n')
        for x in range(xmin,xmax+1):
            p = camaraws.obter_nomeProp_porid(x)
            txt = str(p)
            if not txt == 'None':
                linha = '%d: %s\n' %(x,txt)
                f.write(linha)
        f.close()

if __name__ == "__main__":
    
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
            raise SyntaxError("ERRO de input: use dois argumentos inteiros, o primeiro sendo o id minimo e o segundo o id maximo, ou chame sem argumentos para usar os valores padrao.'")
    if (len(sys.argv)>=4):
        nome_arquivo_saida = sys.argv[3]
        print '# Resultado sera escrito no arquivo de saida: %s' % nome_arquivo_saida
    else:
        nome_arquivo_saida = 'stdout'
    
    cria_txt(nome_arquivo_saida,xmin,xmax)
