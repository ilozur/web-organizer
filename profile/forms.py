from django import forms


class ChangeUserDataForm(forms.Form):
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Enter new e-mail'}))
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Enter new name'}))
    surname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Enter new surname'}))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=200,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Enter old password'}))
    new_password1 = forms.CharField(max_length=200,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(max_length=200,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Enter new password again'}))
