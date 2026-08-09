from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'latitude', 'longitude', 'risk_level', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. Stagnant water near market',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Describe the breeding spot — location details, water type, surroundings...',
            }),
            'latitude': forms.NumberInput(attrs={
                'step': 'any',
                'class': 'form-control',
                'id': 'id_latitude',
                'readonly': True,
                'placeholder': 'Click on the map to set location',
            }),
            'longitude': forms.NumberInput(attrs={
                'step': 'any',
                'class': 'form-control',
                'id': 'id_longitude',
                'readonly': True,
                'placeholder': 'Click on the map to set location',
            }),
            'risk_level': forms.Select(attrs={
                'class': 'form-select form-select-lg',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
