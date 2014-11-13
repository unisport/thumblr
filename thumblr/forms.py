from django import forms
from thumblr.models import ImageType


class AddImageForm(forms.Form):
    image = forms.FileField()
    image_type = forms.ChoiceField(choices=(
        (ImageType.ORIGINAL, ImageType.ORIGINAL),
        (ImageType.THUMBNAIL, ImageType.THUMBNAIL),
        (ImageType.SMALL, ImageType.SMALL),
        (ImageType.MEDIUM, ImageType.MEDIUM),
    ))
