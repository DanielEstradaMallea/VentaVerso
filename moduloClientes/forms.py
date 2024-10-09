from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'direccion', 'telefono', 'correo']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        }
    def __init__(self, user, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(ClienteForm, self).save(commit=False)
        instance.usuario = self.user

        if commit:
            instance.save()

        return instance

