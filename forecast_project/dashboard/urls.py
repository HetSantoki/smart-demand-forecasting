from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/product-forecast/', views.product_forecast, name='product_forecast'),
]   