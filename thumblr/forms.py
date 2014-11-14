from django import forms


class AddImageForm(forms.Form):
    image = forms.FileField()
    site_id = forms.IntegerField()
    content_type = forms.CharField()
    object_id = forms.IntegerField()


