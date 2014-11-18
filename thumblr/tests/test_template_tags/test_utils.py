from django.test import TestCase
from thumblr.templatetags.utils import parse_kwargs, remove_quotes


class TestRemoveQuotes(TestCase):

    def test_basic(self):
        self.assertEqual(
            remove_quotes(u'"asdasd""'),
            u'asdasd"',
        )

        self.assertEqual(
            remove_quotes(u'"Pavlo"'),
            u'Pavlo',
        )

        self.assertEqual(
            remove_quotes(u'\'"Pavlo'),
            u'"Pavlo',
        )


class TestParseKwargs(TestCase):

    def test_basic(self):
        self.assertEqual(
            parse_kwargs(
                [u"size='original'", u"main=True"]
            ),
            { u"size": u'original', u"main": True },
        )

        self.assertEqual(
            parse_kwargs(
                [u"size=original", u"main='True'"]
            ),
            { u"size": u'original', u"main": True },
        )

