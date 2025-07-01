# core/forms.py
from django import forms
from .models import BPIN, Contrato, Documento

class BPINForm(forms.ModelForm):
    class Meta:
        model = BPIN
        fields = ['numero_bpin', 'nombre_proyecto', 'vigencia', 'presupuesto']
        widgets = {
            'numero_bpin': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'vigencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'presupuesto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['numero_contrato', 'objeto_contrato', 'fecha_suscripcion', 'valor_contrato', 'bpin']
        widgets = {
            'numero_contrato': forms.TextInput(attrs={'class': 'form-control'}),
            'objeto_contrato': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fecha_suscripcion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_contrato': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bpin': forms.Select(attrs={'class': 'form-select'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nombre_archivo', 'archivo', 'tipo_documento', 'bpin', 'contrato', 'descripcion']
        widgets = {
            'nombre_archivo': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'bpin': forms.Select(attrs={'class': 'form-select'}),
            'contrato': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }