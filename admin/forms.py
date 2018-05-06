from django import forms

from admin.models import *


class CForm (forms.Form):
    inputfld = forms.IntegerField(label='number')
    choicebox = forms.ChoiceField(choices=(('n', 'Notes'), ('e', 'Events'), ('t', 'Todos'), ('u', 'Users')))

    class Meta:
        model = Creating


class ucform(forms.Form):
    logfld = forms.CharField ( max_length=40 )
    passfld = forms.CharField ( max_length=40 )
    langfld = forms.CharField ( max_length=3 )

    class Meta:
        model = CreateUsr
