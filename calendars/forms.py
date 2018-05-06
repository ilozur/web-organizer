from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class AddingEventForm(forms.Form):
    """!
        @brief Form that handles user's event for writing to DB
    """
    ##@brief Contain date why event will hapen.
    date = forms.DateField(widget=forms.DateInput(attrs={'form': 'add_event_form', 'type': 'date'}))

    ##@brief Contain time why event will happen.
    time = forms.TimeField(widget=forms.TimeInput(attrs={'form': 'add_event_form', 'type': 'time'}))

    ##@brief Contain title(string).
    title = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Мероприятиеюшка',
                                                                          'type': 'name'}))

    ##@brief Contain description(string).
    description = RichTextUploadingFormField(widget=CKEditorUploadingWidget())

    ##@brief  Bool variable about publicity of event.
    is_public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                                                     'form': 'add_event_form',
                                                                                     'type': 'checkbox'}))

    ##@brief Contain date why notification will be send.
    should_notify_days = forms.IntegerField(min_value=0, max_value=30, required=False)

    ##@brief Contain hour why notification will be send.
    should_notify_hours = forms.IntegerField(min_value=0, max_value=23, required=False)

    ##@brief Contain minute why notification will be send.
    should_notify_minutes = forms.IntegerField(min_value=0, max_value=59, required=False)

    ##@brief Contain information about place where event will happen.
    place = forms.CharField(max_length=255, required=None)
