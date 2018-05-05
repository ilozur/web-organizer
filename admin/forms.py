from django import forms
from admin.models import Creating


class cform(forms.ModelForm):
    inputfld = forms.IntegerField(max_length=3, label='number')
    checkbox = forms.BooleanField()
    btnsubmit = forms.CharField(max_length=2)

    class Meta:
        model = Creating
