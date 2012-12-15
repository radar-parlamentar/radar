# coding=utf8

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


from __future__ import unicode_literals
from django.test import TestCase
import models

class ModelsTest(TestCase):

    def test_partido(self):
       pt = models.Partido.from_nome('PT')
       self.assertEquals(pt.numero, 13)
       psdb = models.Partido.from_numero(45)
       self.assertEquals(psdb.nome, 'PSDB')
 
