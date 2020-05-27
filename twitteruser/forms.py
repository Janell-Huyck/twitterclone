from django import forms


class TwitterUserForm(forms.Form):
    username = forms.CharField(max_length=50)
    display_name = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)
