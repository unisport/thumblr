from django import forms
from thumblr.models import ImageSize


class AddImageForm(forms.Form):
    image = forms.FileField()
    site_id = forms.IntegerField()
    content_type = forms.IntegerField()
    object_id = forms.IntegerField()


class ImageSizeForm(forms.ModelForm):
    class Meta:
        model = ImageSize
