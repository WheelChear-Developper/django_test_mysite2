from django import forms

class UserCreateForm(forms.Form):
    file = forms.Field(required=False, widget=forms.FileInput)
