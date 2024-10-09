from django import forms
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellidos', 'direccion', 'telefono', 'correo','rol','pin']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'rol':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rol'}),
            'pin':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Pin de acceso'})
        }
    
    def __init__(self, user, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(EmpleadoForm, self).save(commit=False)
        instance.usuario = self.user

        if commit:
            instance.save()

        return instance
