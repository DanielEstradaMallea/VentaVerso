from django import forms
from .models import Product as Articulo


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['name', 'categoria', 'price', 'stock','imagen']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoria'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock'}),
            'imagen': forms.ClearableFileInput(attrs={'accept': 'image/*', 'directory': 'articulos'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(ArticuloForm, self).save(commit=False)
        instance.usuario = self.user

        if commit:
            instance.save()

        return instance
