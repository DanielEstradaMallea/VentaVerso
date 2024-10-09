from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    categoria = models.CharField(max_length=30)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='articulos/', null=True, blank=True, help_text='Imagen del articulo')

    def __str__(self) -> str:
        return self.name




