from django import template
from django.contrib.contenttypes.models import ContentType
from django.forms import HiddenInput
from django.template.base import TemplateSyntaxError
from thumblr.services.url import get_image_instance_url

from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.forms import ImageSizeForm
from thumblr.models import ImageSize, Image
from thumblr.usecases import get_image_url
from thumblr.views import SizeTable
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


register.tag("thumblr", thumblr_tag_parser)


class ThumblrNode(template.Node):
    def __init__(self, file_name, size=None, site_id=None, content_type_name=None, main=True):
        self.file_name = file_name
        self.size = size
        self.site_id = site_id
        self.content_type_name = content_type_name
        self.main = main

        self._url = None

    @property
    def url(self):
        if self._url is None:
            image_spec = ImageMetadata(
                file_name=self.file_name,
                size_slug=self.size,
                site_id=self.site_id,
                content_type_id=ContentType.objects.values('id').get(name=self.content_type_name)['id']
            )
            self._url = get_image_url(image_spec, ImageUrlSpec.CDN_URL)

        return self._url

    def render(self, context):
        return self.url


class ImagesNode(template.Node):
    def __init__(self, var_name='images', size='original',
                 site_id=None,
                 content_type_id=None,
                 content_type_name=None,
                 object_id=None):
        self.var_name = var_name
        self.size = size
        self.site_id = site_id
        self.content_type_id = content_type_id
        self.content_type_name = content_type_name
        self.object_id = object_id

    def render(self, context):
        images = Image.objects.filter(
            site_id=self.site_id if self.site_id else context.get('site_id'),
            content_type__name=self.content_type_name if self.content_type_name else context.get(
                'content_type_name'),
            object_id=self.object_id if self.object_id else context.get('object_id'),
            size__name=self.size)
        """
        render updates context of the template and adds new variable with var_name that contains images
        """
        urls = list(get_image_instance_url(i, ImageUrlSpec.CDN_URL) for i in images)
        context[self.var_name] = urls


@register.tag("thumblr_imgs")
def thumblr_imgs(parser, token):
    '''
    Could be used with or without
    {% thumblr_imgs large as images %}
    '''
    try:
        split_content = token.split_contents()
        tag_name, kwargs_unparsed, _as, var_name = split_content[0], split_content[1:-2], split_content[-2], \
                                                   split_content[-1]
        kwargs = parse_kwargs(kwargs_unparsed)
        if _as != 'as':
            raise TemplateSyntaxError(
                "'as' wasn't found. Thumblr_imgs should be in the next format {% thumblr_imgs <size> as <var_name> %}")
    except:
        raise TemplateSyntaxError("thumblr_imgs should be in the next format {% thumblr_imgs <size> as <var_name> %}")
    else:
        return ImagesNode(var_name, **kwargs)


class SizeAddingNode(template.Node):
    def __init__(self, content_type_name=None):
        self.content_type_name = content_type_name
        if content_type_name:
            try:
                self.content_type_id = ContentType.objects.values('id').get(name=content_type_name)['id']
            except ContentType.DoesNotExist:
                raise ContentType.DoesNotExist('Content Type from template tag with name "{}" '
                                               'does not exist'.format(content_type_name))
        else:
            self.content_type_id = None

    def render(self, context):
        context['form'] = ImageSizeForm(initial={'content_type': self.content_type_id})
        context['form'].fields['content_type'].widget = HiddenInput()
        context['sizes'] = ImageSize.objects.all()
        context['model'] = self.content_type_name
        t = template.loader.get_template('thumblr/sizes.html')
        if self.content_type_id:
            context['sizes'] = SizeTable(ImageSize.objects.filter(content_type__id=self.content_type_id))
        else:
            context['sizes'] = SizeTable(ImageSize.objects.all())
        return t.render(context)


@register.tag("thumblr_add_sizes")
def thumblr_size_adding(parser, token):
    """
    Tag that returns a form for adding new size with a list of existing sizes for given content type
    {% thumblr_add_sizes content_type_name='Tile' %}
    """
    try:
        split_content = token.split_contents()
        if len(split_content) <= 1:
            return SizeAddingNode()
        tag_name, content_type_name_unparsed = split_content[0], split_content[-1]
        key, content_type_name = content_type_name_unparsed.split('=')
        if key != 'content_type_name':
            raise TemplateSyntaxError(
                "content_type_name coudn't be found in template tag. Check the syntax (Example: "
                "thumblr_add_sizes content_type_name='Tile')")
    except IndexError:
        raise TemplateSyntaxError("Only two arguments should be passes "
                                  "(Example: thumblr_add_sizes content_type_name='Tile')")

    return SizeAddingNode(content_type_name.replace('"', '').replace("'", ''))



