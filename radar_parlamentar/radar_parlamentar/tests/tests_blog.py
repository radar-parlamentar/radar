
from django.test import TestCase
from radar_parlamentar.blog import DictionaryBlogGenerator

class BlogTest(TestCase):

    def test_create_dict_blog(self):
        dict_blog = DictionaryBlogGenerator.create_dict_blog()
        blog_title = dict_blog.feed.title
        self.assertEquals(blog_title,'PoliGNU - Grupo de Estudos de Software Livre da Poli-USP - Radar Parlamentar')

