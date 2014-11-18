from django import forms


class AddImageForm(forms.Form):
    image = forms.FileField()
    site_id = forms.IntegerField()
    content_type = forms.IntegerField()
    object_id = forms.IntegerField()


