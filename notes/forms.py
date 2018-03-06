from django import forms
from ckeditor.widgets import CKEditorWidget


class AddNoteForm(forms.Form):
    title = forms.CharField(label='Enter title', max_length=200)
    data = forms.CharField(widget=CKEditorWidget())


class ShowNoteForm(forms.Form):
    data = forms.CharField(widget=CKEditorWidget())


class SearchForm(forms.Form):
    result = forms.CharField(label='What are you looking for?', max_length=70)
