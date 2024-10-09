from django.shortcuts import render, redirect
from .models import Empleado
from .forms import EmpleadoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

@login_required
def buscar_empleado(request):
    busqueda = request.GET.get('busqueda')
    empleados = Empleado.objects.filter(Q(nombre__icontains=busqueda) |
                                        Q(apellidos__icontains=busqueda))
    resultados = [{'id': e.id, 'nombre': e.nombre,
                   'apellidos': e.apellidos} for e in empleados]
    if resultados:
        request.session['empleado_id'] = resultados[0]['id']
    return JsonResponse(resultados, safe=False)


@login_required
def lista_empleados(request):
    busqueda = request.GET.get("buscarempleado")
    if busqueda:
        empleados = Empleado.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellidos__icontains=busqueda)
        ).distinct()
    else:
        empleados = Empleado.objects.filter(usuario=request.user)
    return render(request, "templatesEmpleados/Empleados.html", {'empleados': empleados})


@login_required
def agregar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return lista_empleados(request)
    else:
        form = EmpleadoForm(user=request.user)
        titulo = "Agregar Empleado"

    return render(request, "templatesEmpleados/agregarempleado.html", {'form': form,'titulo':titulo})


@login_required
def eliminar_empleado(request, id):
    empleado = Empleado.objects.get(id=id)
    nombre_empleado = f'{empleado.nombre} {empleado.apellidos}'
    empleado.delete()

    # Agrega un mensaje de confirmación
    messages.success(request, f'Se ha eliminado a {nombre_empleado}.')
    return redirect('/empleados')


@login_required
def actualizar_empleado(request, id):
    cliente = Empleado.objects.get(id=id)
    titulo = "Modificar Empleado"

    if request.method == 'POST':
        form = EmpleadoForm(user=request.user,
                            data=request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return lista_empleados(request)
    else:
        form = EmpleadoForm(user=request.user, instance=cliente)

    data = {'form': form,'titulo':titulo}
    
    return render(request, 'templatesEmpleados/agregarempleado.html', data)
