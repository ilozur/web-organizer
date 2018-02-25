from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(label='Email or username', error_messages={'required': "Enter email or user name"})
    password = forms.CharField(label='Password', widget=forms.PasswordInput(),
                               error_messages={'required': "Enter password"})


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Enter your e-mail', max_length=200)
    username = forms.CharField(label='Enter username', max_length=200)
    name = forms.CharField(label='Enter your name', max_length=200)
    surname = forms.CharField(label='Enter your surname', max_length=200)
    password1 = forms.CharField(label='Enter password', max_length=200, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Enter password again', max_length=200, widget=forms.PasswordInput())
