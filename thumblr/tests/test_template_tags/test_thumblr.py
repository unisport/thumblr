from django.template import Token, TOKEN_TEXT
from django.test import TestCase
from thumblr.templatetags.thumblr import thubmlr_tag_parser, ThumblrNode


class TestThumblrTagParser(TestCase):

    def test_basic_usage(self):
        token = Token(TOKEN_TEXT, "thumblr 'nike_boots.jpg' size='normal' main=False")
        node = thubmlr_tag_parser(None, token)

        self.assertIsInstance(node, ThumblrNode)
        self.assertEqual(node.file_name, u'nike_boots.jpg')
        self.assertEqual(node.main, False)
        self.assertEqual(node.size, u'normal')