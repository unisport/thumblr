from django import forms


class AddImageForm(forms.Form):
    image = forms.FileField()
    site = forms.URLField()
    content_type = forms.CharField()
    object_id = forms.IntegerField()


