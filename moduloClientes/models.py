from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=35)
    direccion = models.CharField(max_length=40)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre
