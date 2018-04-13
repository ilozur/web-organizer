from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class AddTodoForm(forms.Form):
    title = forms.CharField(label='Enter title', max_length=1000, error_messages={'required': "Enter todo's title"})
    text = forms.CharField(label='Enter description', max_length=1000,
                           error_messages={'required': "Enter todo's description"})
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # планируется интеграция с календарем


class EditTodoForm(forms.Form):
    todo_title_edit = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Напоминание'}))
    todo_text_edit = RichTextUploadingFormField(widget=CKEditorUploadingWidget())
    todo_id = forms.IntegerField(widget=forms.HiddenInput())
    edit_priority = forms.CharField(max_length=200, widget=forms.TextInput())
    edit_deadline = forms.CharField(max_length=128, widget=forms.TextInput())  # планируется интеграция с календарем


class SearchForm(forms.Form):
    result = forms.CharField(label='What are you looking for?', max_length=70)
