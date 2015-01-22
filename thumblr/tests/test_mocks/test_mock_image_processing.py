from django.test.testcases import TestCase
from mock import MagicMock
from thumblr.image_processing.basic_operations import thumbnail, overlay
from thumblr.tests.mocks import thumblr_pil_mock


class TestMockingImageProcessing(TestCase):

    def test_thumbnail(self):
        with self.assertRaises(AssertionError):
            thumbnail(MagicMock(), MagicMock())

        with thumblr_pil_mock():
            thumbnail(MagicMock(), MagicMock())

        with self.assertRaises(AssertionError):
            thumbnail(MagicMock(), MagicMock())

    def test_overlay(self):
        with self.assertRaises(AssertionError):
            overlay(MagicMock(), MagicMock(), MagicMock(), MagicMock())

        with thumblr_pil_mock():
            overlay(MagicMock(), MagicMock(), MagicMock(), MagicMock())

        with self.assertRaises(AssertionError):
            overlay(MagicMock(), MagicMock(), MagicMock(), MagicMock())
