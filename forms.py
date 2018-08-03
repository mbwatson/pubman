from django import forms
from pubman.models import Publication

class PublicationAddForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('doi',)
        labels = {'doi' : 'DOI'}

class PublicationConfirmForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('doi', 'title', 'citation',)
