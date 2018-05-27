from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class SaveNoteForm(forms.Form):
    note_title = forms.CharField(max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                                               'placeholder': 'Название'}))
    note_data = RichTextUploadingFormField(widget=CKEditorUploadingWidget())


class EditNoteForm(forms.Form):
    note_title_edit = forms.CharField(max_length=19, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Название'}))
    note_data_edit = RichTextUploadingFormField(widget=CKEditorUploadingWidget())
