from django import forms


class ResourceForm(forms.Form):
    image = forms.ImageField()
    contributor_id = forms.IntegerField()
    description = forms.CharField(widget=forms.TextInput)
    tags = forms.CharField()
