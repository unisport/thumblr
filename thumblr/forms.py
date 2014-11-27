from django import forms
from thumblr.models import ImageSize


class ImageSizeForm(forms.ModelForm):
    class Meta:
        model = ImageSize
