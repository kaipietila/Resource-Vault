from django.forms import forms


class ResourceForm(forms.Form):
    file = forms.FileField()
    contributor_id = forms.IntegerField()
    description = forms.Textfield()
    tags = forms.Charfield()
