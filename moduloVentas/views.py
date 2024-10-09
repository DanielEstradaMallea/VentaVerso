# En moduloVentas/views.py
from django.shortcuts import render, get_object_or_404
from .models import Sale
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum, Count, Value
from django.db.models.functions import TruncDay
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required


@login_required
def all_sales(request):
    # Obtén todas las ventas procesadas
    sales = Sale.objects.filter(user=request.user)

    sales = sales.order_by('-created_at')
    return render(request, 'templatesVentas/all_sales.html', {'sales': sales})


@login_required
def ver_venta(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    context = {'sale': sale}
    return render(request, 'templatesVentas/sales_details.html', context)


@login_required
def sales_report(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        if not start_date_str or not end_date_str:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
        else:
            start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'))
            end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d')) + timedelta(days=1)

        sales = Sale.objects.filter(user=request.user, created_at__range=[start_date, end_date])

        total_sales = sales.aggregate(total_sales=Coalesce(
            Sum('total_price'), Value(0)))['total_sales']

        daily_sales = sales.annotate(date=TruncDate('created_at')).values(
            'date').annotate(total_sales=Sum('total_price')).order_by('date')

        dates = [sale['date'].strftime('%Y-%m-%d') for sale in daily_sales]
        totals = [sale['total_sales'] for sale in daily_sales]

        context = {'dates': dates, 'totals': totals, 'total_sales': total_sales}
        return render(request, 'templatesVentas/sales_report.html', context)

    return render(request, 'templatesVentas/sales_report.html')