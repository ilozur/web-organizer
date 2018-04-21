from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class AddingEventForm(forms.Form):
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
