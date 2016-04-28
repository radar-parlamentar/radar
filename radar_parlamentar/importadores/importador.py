# -*- coding: utf-8 -*-
from importadores import importador_elasticsearch
import logging

logger = logging.getLogger("radar")


def main(lista_casas_legislativas):

    for casa_legislativa in lista_casas_legislativas:

        if casa_legislativa == 'conv':
            from importadores import conv as importador_convencao
            importador_convencao.main()
            importador_elasticsearch.main()

        elif casa_legislativa == 'cmsp':
            from importadores import cmsp as importador_cmsp
            importador_cmsp.main()
            importador_elasticsearch.main()

        elif casa_legislativa == 'sen':
            from importadores import sen as importador_senado
            importador_senado.main()
            importador_elasticsearch.main()

        elif casa_legislativa == 'cdep':
            from importadores import cdep as importador_camara
            importador_camara.main()
            importador_elasticsearch.main()

        else:
            logger.info("Casa %s não encontrada" % casa_legislativa)
