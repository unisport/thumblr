import os

from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.template import Token, TOKEN_TEXT, Context
from django.test import TestCase
from mock import MagicMock

from thumblr import usecases
from thumblr.dto import ImageMetadata
from thumblr.models import ImageSize
from thumblr.templatetags.thumblr_tags import thumblr_imgs, ImagesNode


class TestThumblrImgsTagParser(TestCase):
    def test_basic_usage(self):
        token = Token(TOKEN_TEXT, "thumblr_imgs size='large' as images")
        node = thumblr_imgs(None, token)

        self.assertIsInstance(node, ImagesNode)
        self.assertEqual(node.var_name, u'images')
        self.assertEqual(node.size, u'large')


class TestThumblrImgsNode(TestCase):
    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "boots.jpg"
        )
        self.site_id = 1
        self.content_type_name = 'image'
        self.content_type_id = ContentType.objects.values('id').get(name=self.content_type_name)['id']

        self.object_id = 1
        self.context = Context({'object_id': self.object_id,
                                'content_type_name': self.content_type_name,
                                'site_id': self.site_id})

        original_size = ImageSize(name=ImageSize.ORIGINAL, content_type_id=self.content_type_id)
        original_size.save()

        self.image_metadata = ImageMetadata(
            file_name='boots.jpg',
            site_id=1,
            size_slug=ImageSize.ORIGINAL,
            content_type_id=self.content_type_id,
            object_id=1,
        )

        with open(self.image_file_path) as f:
            usecases.add_image(
                File(f),
                self.image_metadata
            )

    def test_basic_usage(self):
        token = Token(TOKEN_TEXT, "thumblr_imgs size='original' as images")
        node = thumblr_imgs(MagicMock(), token)
        context = self.context
        node.render(context)
        self.assertIn('images', context, 'Key images should be in context')
        self.assertGreater(len(context['images']), 0, "No images were returned")
        self.assertIn('4d6d69494a4f.jpg',
                      context['images'][0],
                      msg="Test image wasn't found in context tag")

    def test_in_template(self):
        t = template.Template(u"""
            {% load thumblr_tags %}
            {% thumblr_imgs size='original' as imgs %}
            {% for img_url in imgs %}
                {{ img_url }}
            {% endfor %}
        """)
        res = t.render(Context(self.context))
        print(res)
        self.assertIn(u"unisport.dk", res)  # it MUST be cdn url, not s3
        self.assertNotIn(u"boots.jpg", res)  # it MUST be hash, not file name

    def test_in_template_with_arguments(self):
        t = template.Template(u"""
            {%% load thumblr_tags %%}
            {%% thumblr_imgs size='original' site_id=%s content_type_name=%s object_id=%s as imgs %%}
            {%% for img_url in imgs %%}
                {{ img_url }}
            {%% endfor %%}
        """ % (self.site_id, self.content_type_name, self.object_id))
        res = t.render(Context())
        self.assertIn(u"unisport.dk", res)  # it MUST be cdn url, not s3
        self.assertNotIn(u"boots.jpg", res)  # it MUST be hash, not file name