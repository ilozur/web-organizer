from django import forms


class ChangeUserDataForm(forms.Form):
    """
        @!brief Form that handles user's data while changing process
    """
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Enter new e-mail'}))
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Enter new name'}))
    surname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Enter new surname'}))


class ChangePasswordForm(forms.Form):
    """
            @brief Form that handles user's password while changing
    """
    old_password = forms.CharField(max_length=200,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Enter old password'}))
    new_password1 = forms.CharField(max_length=200,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(max_length=200,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Enter new password again'}))


class RecoverPasswordForm(forms.Form):
    """
            !@brief Form that handles user's password while recovering
    """
    password1 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Enter new password'}))
    password2 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Enter new password again'}))


class RecoverPasswordUserData(forms.Form):
    """!
            @brief Form that handles user's data while recovering
    """
    recover_email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Enter your e-mail'}))
    recover_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Enter your name'}))
