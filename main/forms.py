from django import forms


class AuthForm(forms.Form):
    username = forms.CharField(label='Email or username', error_messages={'required': "Enter email or user name"})
    password = forms.CharField(label='Password', widget=forms.PasswordInput(),
                               error_messages={'required': "Enter password"})
