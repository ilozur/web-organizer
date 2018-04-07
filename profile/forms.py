from django import forms


class ChangeUserDataForm(forms.Form):
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Введите новый адрес эл.почты'}))
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Введите новое имя'}))
    surname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Введите новую фамилию'}))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=200,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Введите старый пароль'}))
    new_password1 = forms.CharField(max_length=200,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Введите новый пароль'}))
    new_password2 = forms.CharField(max_length=200,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Введите новый пароль еще раз'}))


class RecoverPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Введите новый пароль'}))
    password2 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Введите новый пароль еще раз'}))


class RecoverPasswordUserData(forms.Form):
    recover_email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Введите адрес эл.почты'}))
    recover_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Введите ваше имя'}))
