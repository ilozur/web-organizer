from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class AddTodoForm(forms.Form):
    title = forms.CharField(label='Enter title', max_length=1000,
                            widget=forms.TextInput(attrs={'form': 'add_todo_form', 'class': 'form-control', 'placeholder': 'Название'}))
    text = forms.CharField(label='Enter description', max_length=1000,
                           widget=forms.Textarea(attrs={'form': 'add_todo_form', 'class': 'form-control', 'placeholder': 'Текст'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'form': 'add_todo_form', 'class': 'form-control', 'type': 'time'}))
    deadline = forms.DateField(widget=forms.DateInput(attrs={'form': 'add_todo_form', 'class': 'form-control', 'type': 'date'}))


class EditTodoForm(forms.Form):
    todo_title_edit = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Напоминание'}))
    todo_text_edit = RichTextUploadingFormField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                                             'placeholder': 'Текст'}))
    edit_priority = forms.CharField(max_length=200, widget=forms.TextInput())
    edit_deadline = forms.DateField(widget=forms.DateInput())


class SearchForm(forms.Form):
    result = forms.CharField(label='What are you looking for?', max_length=70)
