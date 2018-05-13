from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class AddTodoForm(forms.Form):
    todo_title = forms.CharField(label='Enter title', max_length=1000,
                                 widget=forms.TextInput(attrs={'form': 'add_todo_form', 'class': 'form-control', 'placeholder': 'Название'}))
    todo_text = forms.CharField(label='Enter description', max_length=1000,
                                widget=forms.Textarea(attrs={'form': 'add_todo_form', 'class': 'form-control', 'placeholder': 'Текст'}))
    todo_time = forms.TimeField(widget=forms.TimeInput(attrs={'form': 'add_todo_form', 'class': 'form-control', 'type': 'time'}))
    todo_deadline = forms.DateField(widget=forms.DateInput(attrs={'form': 'add_todo_form', 'class': 'form-control', 'type': 'date'}))
    todo_priority = forms.IntegerField(widget=forms.HiddenInput())


class EditTodoForm(forms.Form):
    todo_edit_title = forms.CharField(label='Enter title', max_length=1000,
                                      widget=forms.TextInput(attrs={'form': 'edit_todo_form', 'class': 'form-control', 'placeholder': 'Напоминалочка'}))
    todo_edit_text = forms.CharField(label='Enter description', max_length=1000,
                                     widget=forms.Textarea(attrs={'form': 'edit_todo_form', 'class': 'form-control', 'placeholder': 'Текст'}))
    todo_edit_time = forms.TimeField(widget=forms.TimeInput(attrs={'form': 'edit_todo_form', 'class': 'form-control', 'type': 'time'}))
    todo_edit_deadline = forms.DateField(widget=forms.DateInput(attrs={'form': 'edit_todo_form', 'class': 'form-control', 'type': 'date'}))
    todo_edit_priority = forms.IntegerField(widget=forms.HiddenInput())
    todo_id = forms.IntegerField(widget=forms.HiddenInput())


class SearchForm(forms.Form):
    result = forms.CharField(max_length=70)
