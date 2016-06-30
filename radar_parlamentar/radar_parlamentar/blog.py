import feedparser

class DictionaryBlogGenerator:

	@staticmethod
	def create_dict_blog():
		# FIX-ME: url hard coded
		polignu_blog_url = "http://polignu.org/taxonomy/term/173/feed"
		dict_generated = feedparser.parse(polignu_blog_url)
		return dict_generated

