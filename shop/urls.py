from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.allProducts, name='allProducts'),
    path('<slug:c_slug>/', views.allProducts, name='products_by_category'),
    path('<slug:c_slug>/<slug:p_slug>', views.productDetails, name='product_detail')
]
