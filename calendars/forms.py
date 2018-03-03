from django import forms
from ckeditor.widgets import CKEditorWidget


class AddingEventForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()
    title = forms.CharField(max_length=256)
    description = forms.CharField(widget=CKEditorWidget())
    is_public = forms.BooleanField(required=False)
    should_notify_days = forms.IntegerField()
    should_notify_hours = forms.IntegerField()
    should_notify_minutes = forms.IntegerField()
