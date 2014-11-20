from django import template
from django.template.base import TemplateSyntaxError
from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.models import ImageFile, Image
from thumblr.services.image_file_service import get_image_file_url
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


class ImagesNode(template.Node):
    def __init__(self, size='original', var_name='images'):
        self.size = size
        self.var_name = var_name

    def render(self, context):
        """
        render updates context of the template and adds new variable with var_name that contains images
        """
        images = ImageFile.objects.filter(image__site_id=context['site_id'],
                                                          image__content_type_id=context['content_type_id'],
                                                          image__object_id=context['object_id'],
                                                          size__name=self.size)
        urls = list(get_image_file_url(i, ImageUrlSpec.CDN_URL) for i in images)
        context[self.var_name] = urls


def thumblr_imgs(parser, token):
    '''{% thumblr_imgs large as images %}'''
    try:
        tag_name, size, _as, var_name = token.split_contents()
        if _as != 'as':
            raise TemplateSyntaxError("'as' wasn't found. Thumblr_imgs should be in the next format {% thumblr_imgs <size> as <var_name> %}")
    except:
        raise TemplateSyntaxError("thumblr_imgs should be in the next format {% thumblr_imgs <size> as <var_name> %}")
    else:
        return ImagesNode(size, var_name)


register.tag("thumblr", thumblr_tag_parser)
register.tag("thumblr_imgs", thumblr_imgs)