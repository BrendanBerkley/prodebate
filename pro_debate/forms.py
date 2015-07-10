from django import forms

class SupportCounterPointForm(forms.Form):
    position = forms.CharField(
        label="What's your point?", 
        max_length=255,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    elaboration = forms.CharField(
        label='Tell me more.', 
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'rows': '',
            'cols': ''
        }),
        required=False
    )
    tree_relation = forms.CharField(
        widget=forms.HiddenInput(), 
        max_length=1
    )
    child_of = forms.CharField(
        widget=forms.HiddenInput(), 
        required=False
    )
    grandchild_of = forms.CharField(
        widget=forms.HiddenInput(), 
        required=False
    )

class SubmitManifestationForm(forms.Form):
    url = forms.URLField(
        max_length=400,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label="URL"
    )
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label="Article Title"
    )
    notes = forms.CharField(
        label='Relevant quote', 
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'rows': '',
            'cols': ''
        })
    )
    manifests = forms.CharField(widget=forms.HiddenInput())

