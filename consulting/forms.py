from django import forms
from django.forms import ModelForm
from consulting.models import ConsultingRequest


class ConsultingRequestForm(ModelForm):
    request = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea i-textarea-5'}))

    class Meta:
        model = ConsultingRequest
        exclude = ()


