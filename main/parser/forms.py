from django import forms
from .models import Preference, NewsKeyWord



class NewsKeyWordForm(forms.ModelForm):

    class Meta:
        model = NewsKeyWord
        fields = '__all__'
        widgets = {
            'keyword': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PreferenceForm(forms.ModelForm):

    class Meta:
        model = Preference
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'default_value': forms.TextInput(attrs={'class': 'form-control'}),
        }