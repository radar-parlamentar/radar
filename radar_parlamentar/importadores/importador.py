# -*- coding: utf-8 -*-
def main(lista_casas_legislativas):

    for casa_legislativa in lista_casas_legislativas:

        if casa_legislativa == 'conv':
            from importadores import conv as importador_convencao

            importador_convencao.main()

        elif casa_legislativa == 'cmsp':
            from importadores import cmsp as importador_cmsp

            importador_cmsp.main()

        elif casa_legislativa == 'sen':
            from importadores import sen as importador_senado

            importador_senado.main()

        elif casa_legislativa == 'cdep':
            from importadores import cdep as importador_camara

            importador_camara.main()

        else:
            print "Casa %s não encontrada" % casa_legislativa
