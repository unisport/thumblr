from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.template.context import Context
from django_tables2 import tables
from thumblr.models import ImageSize
from forms import ImageSizeForm


class SizeTable(tables.Table):
    """
    This class customizes the view of table. Can be used for adding columns
    """
    class Meta:
        model = ImageSize


def imagesizes(request):
    context = Context()
    context['form'] = ImageSizeForm()
    if request.method == 'POST':
        form = ImageSizeForm(request.POST, request.FILES)
        if form.is_valid():
            imagesize = ImageSize()
            imagesize.name = form.data['name']
            imagesize.width = form.data['width']
            imagesize.height = form.data['height']
            imagesize.content_type = ContentType.objects.get(pk=int(form.data['content_type']))
            imagesize.save()
            messages.info(request, 'Size was successfully added')
        else:
            messages.error(request, form.errors)
    return redirect(request.META['HTTP_REFERER'])

