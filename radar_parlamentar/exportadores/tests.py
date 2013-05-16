"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from __future__ import unicode_literals
from django.test import TestCase
from django.core import serializers
import exportar
import os
from modelagem import models


MODULE_DIR = os.path.abspath(os.path.dirname(__file__))


class exportarTest (TestCase):
    def test_create_file_partido(self):
    	filepath = os.path.join(MODULE_DIR, 'dados/voto.xml')
    	self.assertTrue(os.path.isfile(filepath))
		




        


