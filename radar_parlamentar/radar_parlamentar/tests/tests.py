# -*- coding: utf8 -*-

from django.test import TestCase
from radar_parlamentar.templatetags.versao_radar import versao_radar
import re
from radar_parlamentar.radar_parlamentar.blog import DictionaryBlogGenerator

class VersaoRadarTest(TestCase):

    def setUp(self):
        self.versao_radar = versao_radar()

    def test_versao_radar(self):

        pattern = r'^Versão: <a href="https://github\.com/radar-parlamentar/'
        pattern += 'radar/commit/[a-z0-9]{40}".*>[a-z0-9]{7}</a> de '
        pattern += '\d{2}/\d{2}/\d{4}$'

        result = re.match(pattern, self.versao_radar)

        self.assertIsNotNone(result)
