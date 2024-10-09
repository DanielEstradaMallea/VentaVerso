from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm
from django.db.models import Q
from django.contrib import messages


@login_required
def lista_clientes(request):
    busqueda = request.GET.get("buscarcliente")

    # función para obtener todos los clientes
    clientes = Cliente.objects.filter(usuario=request.user)


    # filtras los clientes según los criterios
    if busqueda:
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellidos__icontains=busqueda) |
            Q(correo__icontains=busqueda)
        ).distinct()

    clientes = clientes.order_by('apellidos')

    # Devuelves la respuesta renderizada con los clientes
    return render(request, "templatesClientes/clientes.html", {'clientes': clientes})


@login_required
def agregar_cliente(request):

    if request.method == 'POST':
        form = ClienteForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return lista_clientes(request)
    else:
        form = ClienteForm(user=request.user)
        titulo = "Agregar Cliente"


    return render(request, 'templatesClientes/agregarcliente.html', {'form': form,'titulo':titulo})


@login_required
def actualizar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    titulo = "Modificar Cliente"
    
    if request.method == 'POST':
        form = ClienteForm(user=request.user, data=request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return lista_clientes(request)
    else:
        form = ClienteForm(user=request.user, instance=cliente)

    data = {'form': form,'titulo':titulo}
    return render(request, 'templatesClientes/agregarcliente.html', data)



@login_required
def eliminar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
     # Agrega un mensaje de confirmación
    messages.success(request, f'Se ha eliminado a {cliente.nombre} {cliente.apellidos}.')
    return redirect('/clientes')
