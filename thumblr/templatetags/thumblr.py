from django import template
from .utils import parse_kwargs


register = template.Library()


def thubmlr_tag_parser(parser, token):
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

    def render(self, context):
        pass
