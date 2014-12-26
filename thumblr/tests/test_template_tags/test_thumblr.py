from django import template
from django.template import Token, TOKEN_TEXT
from django.test import TestCase
from mock import MagicMock, patch
from thumblr.templatetags.thumblr_tags import thumblr_tag_parser, ThumblrNode
from thumblr.tests.base import BaseThumblrTestCase


class TestThumblrTagParser(TestCase):

    def test_basic_usage(self):
        token = Token(TOKEN_TEXT, "thumblr 'nike_boots.jpg' size='normal' content_type_name='image' main=False")
        node = thumblr_tag_parser(None, token)

        self.assertIsInstance(node, ThumblrNode)
        self.assertEqual(node.file_name, u'nike_boots.jpg')
        self.assertEqual(node.main, False)
        self.assertEqual(node.size, u'normal')


class TestThumblrNode(BaseThumblrTestCase):

    def test_basic_usage(self):
        token = Token(TOKEN_TEXT, "thumblr 'boots.jpg' size='original' content_type_name='image'")
        node = thumblr_tag_parser(MagicMock(), token)
        url = node.render(MagicMock())

        self.assertIn(u"unisport.dk", url)

    def test_in_template(self):
        t = template.Template(u"""
            {% load thumblr_tags %}
            {% thumblr 'boots.jpg' size='original' content_type_name='image' %}
        """)
        res = t.render(template.Context())
        print(res)
        self.assertIn(u"unisport.dk", res)  # it MUST be cdn url, not s3
        self.assertNotIn(u"boots.jpg", res)  # it MUST be hash, not file name