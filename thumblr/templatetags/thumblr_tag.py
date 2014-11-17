from django import template
from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.usecases import get_image_url
from .utils import parse_kwargs


register = template.Library()


def thumblr_tag_parser(parser, token):
    try:
        splited = token.split_contents()
        tag_name, file_name, params = splited[0], splited[1], splited[2:]
    except ValueError:
        raise template.TemplateSyntaxError(u"%r tag requires at least file name and size" % token.contents.split()[0])

    kwargs = parse_kwargs(params)
    return ThumblrNode(file_name[1:-1], **kwargs)


class ThumblrNode(template.Node):

    def __init__(self, file_name, size=None, site_id=None, main=True):
        self.file_name = file_name
        self.size = size
        self.site_id = site_id
        self.main = main

        self._url = None

    @property
    def url(self):
        if self._url is None:
            image_spec = ImageMetadata(
                file_name=self.file_name,
                size_slug=self.size,
                site_id=self.site_id,
            )
            self._url = get_image_url(image_spec, ImageUrlSpec.CDN_URL)

        return self._url

    def render(self, context):
        return self.url
