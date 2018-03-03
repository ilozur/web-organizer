from django import forms

class ShowTodoForm(forms.Form):
    data = forms.CharField(label='What are you want?')

