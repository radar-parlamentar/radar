from __future__ import absolute_import, unicode_literals
from celery import shared_task
from importadores import importador
import logging

logger = logging.getLogger("radar")

@shared_task
def importar_assincronamente(nome_curto_casa_legislativa):
    importador.main([nome_curto_casa_legislativa])
    logger.info("Importação de %s completa" % nome_curto_casa_legislativa)
