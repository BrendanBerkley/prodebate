from django import forms

class SupportCounterPointForm(forms.Form):
    position = forms.CharField(label="What's your point?", max_length=255)
    elaboration = forms.CharField(
        label='Tell me more.', 
        widget=forms.Textarea,
        required=False
    )