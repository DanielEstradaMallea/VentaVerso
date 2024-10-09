# En moduloVentas/models.py
from django.db import models
from moduloArticulos.models import Product
from moduloEmpleado.models import Empleado
from django.contrib.auth.models import User


class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empleado = models.ForeignKey(
        Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product, through='SaleItem')
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    recibo_numero = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        # Si la venta es nueva
        if not self.pk:
            # Obtén la última venta del usuario
            last_sale = Sale.objects.filter(
                user=self.user).order_by('-recibo_numero').first()

            # Si el usuario ya tiene ventas, incrementa el número de recibo, de lo contrario, comienza en 1
            self.recibo_numero = last_sale.recibo_numero + 1 if last_sale else 1

        super().save(*args, **kwargs)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()
    subtotal = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calcular y actualizar el subtotal antes de guardar
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)
