# -*- coding: utf8 -*-

from django.test import TestCase
from radar_parlamentar.templatetags.versao_radar import versao_radar
import re
from blog import DictionaryBlogGenerator
from views import *
from django.core.urlresolvers import reverse


class BlogTest(TestCase):

    def test_create_dict_blog(self):
        dict_blog = DictionaryBlogGenerator.create_dict_blog()
        blog_title = dict_blog.feed.title
        self.assertEquals(blog_title,'PoliGNU - Grupo de Estudos de Software Livre da Poli-USP - Radar Parlamentar')

    def test_generate_blog_news(self):
        url = reverse("blog")
        request = self.client.get(url)
        first_blog_news = "Elasticsearch no Radar Parlamentar: filtrando votações por palavras-chaves"
        self.assertContains(request, first_blog_news, status_code = 200)


class VersaoRadarTest(TestCase):

    def setUp(self):
        self.versao_radar = versao_radar()

    def test_versao_radar(self):

        pattern = r'^Versão: <a href="https://github\.com/radar-parlamentar/'
        pattern += 'radar/commit/[a-z0-9]{40}".*>[a-z0-9]{7}</a> de '
        pattern += '\d{2}/\d{2}/\d{4}$'

        result = re.match(pattern, self.versao_radar)

        self.assertIsNotNone(result)
