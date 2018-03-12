from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class AddNoteForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Заметочка'}))
    data = RichTextUploadingFormField(widget=CKEditorUploadingWidget)


class ShowNoteForm(forms.Form):
    title_show = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'placeholder': 'Заметочка'}))
    data_show = forms.CharField(widget=CKEditorWidget())


class SearchForm(forms.Form):
    result = forms.CharField(label='What are you looking for?', max_length=70)
