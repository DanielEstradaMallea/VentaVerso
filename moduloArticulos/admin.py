from django.contrib import admin
from .models import Product

class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['name', 'categoria', 'price', 'stock']
    list_editable = ['price']
    search_fields = ['name', 'categoria']


# Register your models here.

admin.site.register(Product,ArticuloAdmin)


