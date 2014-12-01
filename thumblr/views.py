from django.contrib import messages
from django.shortcuts import render
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
    context['sizes'] = SizeTable(ImageSize.objects.all())
    if request.method == 'POST':
        form = ImageSizeForm(request.POST, request.FILES)
        if form.is_valid():
            imagesize = ImageSize()
            imagesize.name = form.data['name']
            imagesize.width = form.data['width']
            imagesize.height = form.data['height']
            imagesize.save()
            messages.info(request, 'Size was successfully added')
        else:
            messages.error(request, "Please check the form values. Form is not valid.")
    return render(request, "thumblr/sizes.html", context)

