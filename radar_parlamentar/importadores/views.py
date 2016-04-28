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

from __future__ import unicode_literals
import logging
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from celery import importar_assincronamente

logger = logging.getLogger("radar")


@staff_member_required
def importar(request, nome_curto_casa_legislativa):
    logger.info("Invocando importador de %s assincronamente" %
                nome_curto_casa_legislativa)
    importar_assincronamente.delay(nome_curto_casa_legislativa)
    return HttpResponse("OK, invocando importador de %s assincronamente" %
                        nome_curto_casa_legislativa)
