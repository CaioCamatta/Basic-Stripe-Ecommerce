from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_cart_item, name='add_cart_item'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>', views.item_remove, name='item_remove'),
    path('delete/<int:product_id>', views.item_full_delete, name='item_full_delete')
]
