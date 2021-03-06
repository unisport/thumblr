from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template import Token, TOKEN_TEXT, Context
from django.test import TestCase, Client, RequestFactory
from mock import MagicMock
from thumblr import views

from thumblr.templatetags.thumblr_tags import SizeAddingNode, thumblr_size_adding


class TestSizeAddingTagParser(TestCase):
    def test_basic_usage(self):
        token = Token(TOKEN_TEXT, "thumblr_add_sizes content_type_name='image'")
        node = thumblr_size_adding(None, token)

        self.assertIsInstance(node, SizeAddingNode)
        self.assertEqual(node.content_type_name, u'image')


class TestSizeAddNode(TestCase):
    def setUp(self):
        self.content_type_id = 2
        self.context = {'content_type_name': self.content_type_id, }
        self.factory = RequestFactory()

    def test_rendered_template(self):
        _template = template.Template(u"""
            {% load thumblr_tags %}
            {% thumblr_add_sizes content_type_name='image' %}
        """)
        self.context['request'] = HttpRequest()
        result = _template.render(Context(self.context))
        self.assertIn('<input type="submit" value="Submit"/>', result, 'Submit button not in a form')
        self.assertIn('<form action="{}" method="post">'.format(reverse('thumblr:imagesizes')), result)
        self.assertIn('<label for="id_width">', result, "Width wasn't found in a form")
        self.assertIn('<label for="id_height">', result, "Height wasn't found in a form")


class TestAddSize(TestCase):
    urls = 'thumblr.tests.test_template_tags.urls'
    def setUp(self):
        self.client = Client()

    def test_size_adding_through_form(self):
        data = {
            "name": "test size",
            "width": 350,
            "height": 440,
            "content_type": ContentType.objects.get(name='image').id
        }
        self.client.post(reverse(views.imagesizes), data=data, HTTP_REFERER='http://unisport.dk')