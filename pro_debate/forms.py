from django import forms
from taggit.forms import TagField
from .models import Position, Elaboration

class PositionForm(forms.Form):
    position = forms.CharField(
        label="Position Statement", 
        max_length=255,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    tags = TagField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=True
    )


class ElaborationForm(forms.Form):
    elaboration = forms.CharField(
        label='Edit elaboration', 
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'rows': '15',
            'cols': ''
        }),
        required=False
    )
    # tree_relation = forms.ChoiceField( 
    #     widget=forms.Select(attrs={'class':'form-control'}),
    #     label='Relation to Parent', 
    #     choices=Elaboration.TREE_RELATION_CHOICES,
    # )
    # child_of = forms.ModelChoiceField(
    #     queryset=Position.objects.all(),
    #     widget=forms.Select(attrs={'class':'form-control'}),
    #     required=False,
    # )

    # def clean(self):
    #     cleaned_data = super(ElaborationForm, self).clean()
    #     tree_relation = cleaned_data.get('tree_relation')
    #     child_of = cleaned_data.get('child_of')

    #     if (child_of == None and not tree_relation == "G"):
    #         raise forms.ValidationError(
    #             "If removing the 'Child of' link, set 'Relation to Parent' "
    #             "to general."
    #         )
    #     if (child_of and tree_relation == "G"):
    #         raise forms.ValidationError(
    #             "If setting a 'Child of' link, set 'Relation to Parent' to "
    #             "be a support or counter point."
    #         )


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
    tags = TagField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=True
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
    position_parent = forms.CharField(
        widget=forms.HiddenInput(), 
        required=False
    )
    position_grandparent = forms.CharField(
        widget=forms.HiddenInput(), 
        required=False
    )

