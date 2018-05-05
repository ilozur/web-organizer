from django import forms
from admin.models import *


class cform(forms.ModelForm):
    inputfld = forms.IntegerField(label='number')
    checkbox = forms.BooleanField()
    key = forms.CharField(max_length=2)

    class Meta:
        model = Creating

class ucform(forms.ModelForm):
    logfld = forms.CharField ( max_length=40 )
    passfld = forms.CharField ( max_length=40 )
    langfld = forms.CharField ( max_length=3 )
    key = forms.CharField(max_length=2)
    class Meta:
        model = CreateUsr