from django.shortcuts import render
from django.http import JsonResponse
from .utils import (
    daily_demand, predict_future, get_top_products,
    predict_product, get_stockout_alerts, FESTIVALS
)
import json

def index(request):
    days = int(request.GET.get('days', 30))

    # Overview chart data
    historical      = daily_demand['TotalQuantity'].iloc[-60:]
    hist_dates      = historical.index.strftime('%Y-%m-%d').tolist()
    hist_quantities = historical.values.tolist()

    future_dates, future_quantities = predict_future(days)

    total_predicted = sum(future_quantities)
    avg_daily       = round(total_predicted / days)
    peak_day_idx    = future_quantities.index(max(future_quantities))
    peak_day        = future_dates[peak_day_idx]
    peak_qty        = max(future_quantities)
    stockout_alert  = peak_qty > avg_daily * 2

    context = {
        'days'              : days,
        'hist_dates'        : json.dumps(hist_dates),
        'hist_quantities'   : json.dumps(hist_quantities),
        'future_dates'      : json.dumps(future_dates),
        'future_quantities' : json.dumps(future_quantities),
        'total_predicted'   : f"{total_predicted:,}",
        'avg_daily'         : f"{avg_daily:,}",
        'peak_day'          : peak_day,
        'peak_qty'          : f"{peak_qty:,}",
        'stockout_alert'    : stockout_alert,
        'festivals'         : json.dumps(FESTIVALS),
        'products'          : get_top_products(),
        'alerts'            : get_stockout_alerts(),
    }
    return render(request, 'dashboard/index.html', context)


def product_forecast(request):
    product = request.GET.get('product', '')
    days    = int(request.GET.get('days', 30))

    if not product:
        return JsonResponse({'error': 'No product selected'}, status=400)

    hist_dates, hist_qty, future_dates, future_qty = predict_product(product, days)

    return JsonResponse({
        'hist_dates'  : hist_dates,
        'hist_qty'    : hist_qty,
        'future_dates': future_dates,
        'future_qty'  : future_qty,
        'total'       : f"{sum(future_qty):,}",
        'avg'         : f"{round(sum(future_qty)/days):,}",
        'peak'        : f"{max(future_qty):,}",
    })