from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product as Articulo
from .forms import ArticuloForm
from django.db.models import Q
from django.contrib import messages


@login_required
def listar():

    articulos = Articulo.objects.all()

    context = {'articulos': articulos}

    return context
# Lista articulos al template


@login_required
def lista_articulos(request):
    busqueda = request.GET.get("buscarlista")

    # Filtra los artículos del usuario actual
    articulos_usuario = Articulo.objects.filter(usuario=request.user)

    # Filtra los artículos según los criterios de búsqueda
    if busqueda:
        articulos_usuario = articulos_usuario.filter(
            Q(name=busqueda)).distinct()

    articulos_usuario = articulos_usuario.order_by('name')
    # Devuelve la respuesta renderizada con los artículos del usuario
    return render(request, "templatesArticulos/articulos.html", {'articulos': articulos_usuario})


# Peticion para agregar articulos a la DB
@login_required
def agregar_articulo(request):

    if request.method == 'POST':
        form = ArticuloForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            # Redirige a la vista lista_articulos
            return lista_articulos(request)
    else:
        form = ArticuloForm(user=request.user)
        titulo = "Agregar Articulo"

    return render(request, "templatesArticulos/agregararticulo.html", {'form': form, 'titulo': titulo})

# Peticion para eliminar un articulo a la DB
@login_required
def eliminar_articulo(request, id):
    articulo = Articulo.objects.get(id=id)
    articulo.delete()
    # Agrega un mensaje de confirmación
    messages.success(
        request, f'Se ha eliminado a {articulo.name} {articulo.categoria}.')
    return redirect('/articulos')

# Peticion para actualizar articulo de la BD
@login_required
def actualizar_articulo(request, id):
    cliente = Articulo.objects.get(id=id)
    titulo = "Modificar Articulo"

    if request.method == 'POST':
        form = ArticuloForm(user=request.user,
                            data=request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return lista_articulos(request)
    else:
        form = ArticuloForm(user=request.user, instance=cliente)

    data = {'form': form, 'titulo': titulo}
    return render(request, 'templatesArticulos/agregararticulo.html', data)
