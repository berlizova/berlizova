from django.urls import path
from .views import shop_view, product_detail, news_detail, staff_detail, add_to_cart

urlpatterns = [
    path('', shop_view, name='shop'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('staff/<int:pk>/', staff_detail, name='staff_detail'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
]
