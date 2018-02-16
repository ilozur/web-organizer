from django import forms


class AddNoteForm(forms.Form):
    title = forms.CharField(label='Enter title', max_length=200)
    data = forms.CharField(label='Enter description', max_length=400, widget=forms.Textarea)
