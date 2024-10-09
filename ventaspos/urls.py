"""
URL configuration for ventaspos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from moduloArticulos import views as articulos
from moduloCarrito import views
from moduloEmpleado import views as empleados
from moduloVentas import views as ventas
from moduloClientes import views as clientes


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('moduloCuentas.urls')),
    path('cuerpoventa/', views.index, name='cuerpoventa'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("cart/", views.cart, name="cart"),
   
    path('edit_cart_item/<int:item_id>/<int:new_quantity>/', views.edit_cart_item, name='edit_cart_item'),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),

    path("add_to_cart", views.add_to_cart, name="add"),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('articulos/', articulos.lista_articulos, name='articulos'),
    path('agregararticulo/', articulos.agregar_articulo,name='agregar_articulo'),
    path('eliminararticulo/<int:id>',
         articulos.eliminar_articulo, name='eliminar_articulo'),
    path('actualizararticulo/<int:id>',
         articulos.actualizar_articulo, name='actualizar_articulo'),
    
    path('empleados/', empleados.lista_empleados, name='empleados'),
    path('agregarempleado/', empleados.agregar_empleado, name='agregar_empleado'),
    path('eliminarempleado/<int:id>',
         empleados.eliminar_empleado, name='eliminar_empleado'),
    path('actualizarempleado/<int:id>',
         empleados.actualizar_empleado, name='actualizar_empleado'),
    path('procesar_venta/', views.process_sale, name='process_sale'),
    path('all_sales/', ventas.all_sales, name='all_sales'),
    path('buscar_empleado/', empleados.buscar_empleado, name='buscar_empleado'),
    path('asociar_empleado/', views.guardar_empleado, name='guardar_empleado'),
    path('ver_venta/<int:sale_id>/', ventas.ver_venta, name='ver_venta'),
    path('reporte_ventas/', ventas.sales_report, name='sales_report'),
     path('clientes/', clientes.lista_clientes, name='clientes'),
    path('agregarcliente/', clientes.agregar_cliente, name='agregar_cliente'),
    path('eliminarcliente/<int:id>',
         clientes.eliminar_cliente, name='eliminar_cliente'),
    path('actualizarcliente/<int:id>',
         clientes.actualizar_cliente, name='actualizar_cliente'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


