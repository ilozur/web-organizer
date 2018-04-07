from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class AddNoteForm(forms.Form):
    note_title = forms.CharField(max_length=19, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Заметочка'}))
    note_data = RichTextUploadingFormField(widget=CKEditorUploadingWidget)
    note_data_part = forms.CharField(max_length=128, widget=forms.HiddenInput())


class EditNoteForm(forms.Form):
    note_title_edit = forms.CharField(max_length=19, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                   'placeholder': 'Заметочка'}))
    note_data_edit = RichTextUploadingFormField(widget=CKEditorUploadingWidget())
    note_id = forms.IntegerField(widget=forms.HiddenInput())
    note_data_part_edit = forms.CharField(max_length=128, widget=forms.HiddenInput())


class SearchForm(forms.Form):
    result = forms.CharField(label='Что вы ищете?', max_length=70)
