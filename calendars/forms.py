from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class AddEventForm(forms.Form):
    """!
        @brief Form that handles user's event for writing to DB
    """
    date = forms.DateField(widget=forms.DateInput(attrs={'form': 'add_event_form', 'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'form': 'add_event_form', 'type': 'time'}))
    title = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Мероприятиеюшка',
                                                                          'type': 'name'}))
    description = RichTextUploadingFormField(widget=CKEditorUploadingWidget())
    is_public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                                                     'form': 'add_event_form',
                                                                                     'type': 'checkbox'}))
    should_notify_days = forms.IntegerField(min_value=0, max_value=30, required=False)
    should_notify_hours = forms.IntegerField(min_value=0, max_value=23, required=False)
    should_notify_minutes = forms.IntegerField(min_value=0, max_value=59, required=False)
    place = forms.CharField(max_length=255, required=None)


class EditEventForm(forms.Form):
    event_edit_description = RichTextUploadingFormField(widget=CKEditorUploadingWidget())
    event_edit_title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Событие'}))
    event_edit_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'form': 'edit_todo_form', 'class': 'form-control', 'type': 'time'}))
    event_edit_deadline = forms.DateField(
        widget=forms.DateInput(attrs={'form': 'edit_todo_form', 'class': 'form-control', 'type': 'date'}))
    event_id = forms.IntegerField(widget=forms.HiddenInput())
    is_public = forms.BooleanField()
