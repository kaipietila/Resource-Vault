from django import forms


class ResourceForm(forms.Form):
    image = forms.ImageField()
    user = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    description = forms.CharField(widget=forms.TextInput)
    tags = forms.CharField()
