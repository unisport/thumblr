from django import forms


class AddImageForm(forms.Form):
    image = forms.FileField()
    website_url = forms.URLField()
    content_type = forms.CharField()
    object_id = forms.IntegerField()


