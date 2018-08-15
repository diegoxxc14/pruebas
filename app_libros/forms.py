from django import forms
from app_libros.models import Book, Periodo_Rol
from app_prestamo.models import Persona
from django_select2 import forms as ds2

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'codigo',
            'titulo',
            'resumen',
            'imprenta',
            'nro_pag',
            'fecha_pub',
            'autor',
            'persona',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código del libro'}),
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'resumen': forms.TextInput(attrs={'class':'form-control'}),
            'imprenta': forms.TextInput(attrs={'class':'form-control'}),
            'nro_pag': forms.NumberInput(attrs={'class':'form-control'}),
            'fecha_pub': forms.SelectDateWidget(attrs={'class':'form-control'}),
            'autor': forms.SelectMultiple(attrs={'class':'form-control'}),
            'persona': ds2.Select2Widget(attrs={'class':'form-control','data-placeholder':'Seleccione'}),
        }

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo_Rol
        fields = '__all__'
