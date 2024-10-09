from django.urls import path
from .views import home, tpv, exit, register


urlpatterns = [
    path('', home, name='home'),
    path('cuerpoVenta/', tpv, name='cuerpoventa'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
]
