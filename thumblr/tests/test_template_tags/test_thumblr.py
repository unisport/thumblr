from django import template
from django.core.files import File
from django.template import Token, TOKEN_TEXT
from django.test import TestCase
from mock import MagicMock
import os
from thumblr import usecases
from thumblr.dto import ImageMetadata
from thumblr.models import ImageSize
from thumblr.templatetags.thumblr_tags import thumblr_tag_parser, ThumblrNode


class TestThumblrTagParser(TestCase):

    def test_basic_usage(self):
        token = Token(TOKEN_TEXT, "thumblr 'nike_boots.jpg' size='normal' main=False")
        node = thumblr_tag_parser(None, token)

        self.assertIsInstance(node, ThumblrNode)
        self.assertEqual(node.file_name, u'nike_boots.jpg')
        self.assertEqual(node.main, False)
        self.assertEqual(node.size, u'normal')


class TestThumblrNode(TestCase):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "boots.jpg"
        )
        self.site_id = 1
        self.content_type_id = 1
        self.object_id = 1

        original_size = ImageSize(name=ImageSize.ORIGINAL)
        original_size.save()

        self.image_metadata = ImageMetadata(
            file_name='boots.jpg',
            site_id=1,
            size_slug=ImageSize.ORIGINAL,
            content_type_id=1,
            object_id=1,
        )

        with open(self.image_file_path) as f:
            usecases.add_image(
                File(f),
                self.image_metadata
            )

    def test_basic_usage(self):
        token = Token(TOKEN_TEXT, "thumblr 'boots.jpg' size='original'")
        node = thumblr_tag_parser(MagicMock(), token)
        url = node.render(MagicMock())

        self.assertIn(u"unisport.dk", url)

    def test_in_template(self):
        t = template.Template(u"""
            {% load thumblr_tags %}
            {% thumblr 'boots.jpg' size='original' %}
        """)
        res = t.render(template.Context())
        print(res)
        self.assertIn(u"unisport.dk", res)  # it MUST be cdn url, not s3
        self.assertNotIn(u"boots.jpg", res)  # it MUST be hash, not file name