
from django.test import TestCase
from radar_parlamentar.blog import DictionaryBlogGenerator

class BlogTest(TestCase):

    def test_create_dict_blog(self):
        dict_blog = DictionaryBlogGenerator.create_dict_blog()
        blog_title = dict_blog.feed.title
        self.assertEqual(blog_title, 'PoliGNU - Radar Parlamentar')

