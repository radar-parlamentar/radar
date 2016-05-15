# -*- coding: utf-8 -*-

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

"""# Celery/Django HOW-TO:
#http://celery.readthedocs.org/en/latest/django/first-steps-with-django.html"""

from __future__ import unicode_literals
from __future__ import absolute_import
from celery import Celery
import os
from django.conf import settings
import logging
from importadores import importador

logger = logging.getLogger("radar")

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')

celery_app = Celery('radar')
"#celery_app = Celery('views', broker='amqp://guest@localhost//')"

# Using a string here means the worker will not have to
# pickle the object when using Windows.
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@celery_app.task(bind=True)
def importar_assincronamente(self, nome_curto_casa_legislativa):
    importador.main([nome_curto_casa_legislativa])
    logger.info("Importação de %s completa" % nome_curto_casa_legislativa)
