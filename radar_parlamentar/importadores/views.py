# coding=utf8

# Copyright (C) 2014, Leonardo Leite
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

import threading
import logging
from importadores import importador
from django.http import HttpResponse

logger = logging.getLogger("radar")

def importar(request, nome_curto_casa_legislativa):
    logger.info("Invocando importador de %s assincronamente" % nome_curto_casa_legislativa)
    task = ImportadorAync(nome_curto_casa_legislativa)
    task.start()
    return HttpResponse('OK')

class ImportadorAync(threading.Thread):
    
    def __init__(self, nome_curto_casa_legislativa):
        threading.Thread.__init__(self)
        self.nome_curto_casa_legislativa = nome_curto_casa_legislativa
        
    def run(self):
        importador.main([self.nome_curto_casa_legislativa])
        logger.info("Tarefa assíncrona de importação completa")
        
        