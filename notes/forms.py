from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class AddNoteForm(forms.Form):
    note_title = forms.CharField(max_length=19, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Заметочка'}))
    note_data = RichTextUploadingFormField(widget=CKEditorUploadingWidget)


class EditNoteForm(forms.Form):
    note_title_edit = forms.CharField(max_length=19, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                   'placeholder': 'Заметочка'}))
    note_data_edit = RichTextUploadingFormField(widget=CKEditorUploadingWidget())
    note_id = forms.IntegerField(widget=forms.HiddenInput())


class SearchForm(forms.Form):
    result = forms.CharField(label='What are you looking for?', max_length=70)
