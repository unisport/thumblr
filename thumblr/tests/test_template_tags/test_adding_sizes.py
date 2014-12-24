from django import template
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template import Token, TOKEN_TEXT, Context
from django.test import TestCase, Client, RequestFactory
from mock import MagicMock

from thumblr.templatetags.thumblr_tags import SizeAddingNode, thumblr_size_adding


class TestSizeAddingTagParser(TestCase):
    def test_basic_usage(self):
        token = Token(TOKEN_TEXT, "thumblr_add_sizes content_type_id=2")
        node = thumblr_size_adding(None, token)

        self.assertIsInstance(node, SizeAddingNode)
        self.assertEqual(node.content_type_id, u'2')


class TestSizeAddNode(TestCase):
    def setUp(self):
        self.content_type_id = 2
        self.context = {'content_type_id': self.content_type_id, }
        self.factory = RequestFactory()

    def test_rendered_template(self):
        _template = template.Template(u"""
            {% load thumblr_tags %}
            {% thumblr_add_sizes content_type_id=2 %}
        """)
        self.context['request'] = HttpRequest()
        result = _template.render(Context(self.context))
        self.assertIn('<input type="submit" value="Submit"/>', result, 'Submit button not in a form')
        self.assertIn('<form action="{}" method="post">'.format(reverse('thumblr:imagesizes')), result)
        self.assertIn('<label for="id_width">', result, "Width wasn't found in a form")
        self.assertIn('<label for="id_height">', result, "Height wasn't found in a form")
