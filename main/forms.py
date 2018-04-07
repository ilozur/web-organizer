from django import forms


class SignInForm(forms.Form):
    username_sign_in = forms.CharField(label='Эл.почта или имя пользователя', max_length=200,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Введите эл.почту или имя пользователя'}))
    password = forms.CharField(label='Пароль', max_length=200,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Введите пароль'}))


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Эл.почта', max_length=200,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Введите адрес эл.почты'}))
    username = forms.CharField(label='Имя пользователя', max_length=200,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Введите имя пользователя'}))
    name = forms.CharField(label='Имя', max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Введите ваше имя'}))
    surname = forms.CharField(label='Фамилия', max_length=200,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Ввеждите вашу фамилию'}))
    password1 = forms.CharField(label='Пароль', max_length=200,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Пароль еще раз', max_length=200,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Ввелиие пароль еще раз'}))
