# coding=utf8
# Copyright (C) 2012, Eduardo Hideo
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

from django.db import (connections, DEFAULT_DB_ALIAS)
from django.core.management import call_command


def flush_db(cls):
    if getattr(cls, 'multi_db', False):
        databases = connections
    else:
        databases = [DEFAULT_DB_ALIAS]
    for db_name in databases:
        call_command('flush', verbosity=0, interactive=False, database=db_name)
