from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem
from moduloVentas.models import Sale, SaleItem
from moduloEmpleado.models import Empleado
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.contrib import messages
# Create your views here.


@login_required
def index(request):

    products = Product.objects.filter(usuario=request.user)

    products = products.order_by('name')

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)

    context = {"products": products, "cart": cart, 'en_cuerpoventa': True}
    return render(request, "templatesVentas/cuerpoventa.html", context)


@login_required
def guardar_empleado(request):
    if request.method == 'POST':
        empleado_id = request.POST.get('empleadoId')
        # Guardar el ID del empleado en la sesión
        request.session['empleadoId'] = empleado_id
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required
def cart(request):

    cart = None
    cartitems = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cartitems = cart.cartitems.all()

    context = {"cart": cart, "items": cartitems}
    return render(request, "templatesVentas/cart.html", context)


@login_required
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()

        num_of_item = cart.num_of_items

    return JsonResponse(num_of_item, safe=False)


@login_required
def clear_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, completed=False)
        cart.cartitems.all().delete()
        messages.success(request, 'El carrito se ha vaciado correctamente.')

    return redirect('cuerpoventa')


@login_required
@transaction.atomic
def process_sale(request):
    if request.method == 'POST':
        empleado_id = request.session.get('empleadoId')
        empleado = None
        if empleado_id:
            try:
                empleado = Empleado.objects.get(id=empleado_id)
            except Empleado.DoesNotExist:
                pass

        cart = Cart.objects.get(user=request.user, completed=False)
        cart.empleado = empleado
        cart.save()

        sale = Sale.objects.create(
            user=request.user, total_price=cart.total_price, empleado=empleado)

        for cart_item in cart.cartitems.all():
            SaleItem.objects.create(
                sale=sale,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price
            )

            # Actualizar el stock del producto
            product = cart_item.product
            quantity_sold = cart_item.quantity

            product.stock -= quantity_sold
            product.save()

        # Marcar el carrito como completado
        cart.completed = True
        cart.save()

        return render(request, 'templatesVentas/venta_procesada.html', {'sale': sale})

    return redirect('cuerpoventa')


@login_required
def edit_cart_item(request, item_id, new_quantity):
    cart_item = CartItem.objects.get(id=item_id)

    if cart_item.cart.user == request.user:
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()

            # Actualizar el precio total del carrito y el subtotal del artículo
            cart = Cart.objects.get(user=request.user, completed=False)
            total_price = cart.total_price
            subtotal = cart_item.price  # Usa el método price para obtener el subtotal

            # Devolver también la cantidad actualizada
            return JsonResponse({'success': True, 'total_price': total_price, 'subtotal': subtotal, 'quantity': cart_item.quantity})
        else:
            # Si la nueva cantidad es cero, elimina el artículo del carrito
            cart_item.delete()

            # Actualizar el precio total del carrito
            cart = Cart.objects.get(user=request.user, completed=False)
            total_price = cart.total_price
            return JsonResponse({'success': True, 'total_price': total_price, 'quantity': 0})

    return JsonResponse({'success': False})


@login_required
def delete_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)

    if cart_item.cart.user == request.user:
        cart_item.delete()

        # Actualizar el precio total del carrito
        cart = Cart.objects.get(user=request.user, completed=False)
        total_price = cart.total_price
        return JsonResponse({'success': True, 'total_price': total_price})

    return JsonResponse({'success': False})
