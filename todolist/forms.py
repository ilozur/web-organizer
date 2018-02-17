from django import forms


class AddTodoForm(forms.Form):
    title = forms.CharField(label='Enter title', max_length=200, error_messages={'required': "Enter todo's title"})
    text = forms.CharField(label='Enter description', max_length=400,
                           error_messages={'required': "Enter todo's description"})
    priority = forms.CharField(label='Enter priority', max_length=200)
    deadline = forms.CharField(max_length=128, default="deadline")  # планируется интеграция с календарем
