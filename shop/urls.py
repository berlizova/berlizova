from django.urls import path
from .views import (
    shop_view,
    product_detail,
    news_detail,
    staff_detail,
    add_to_cart,
    category_detail,
    all_news_view,
    all_staff_view
)

urlpatterns = [
    path('', shop_view, name='shop'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('staff/<int:pk>/', staff_detail, name='staff_detail'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    path('all_news/', all_news_view, name='all_news'),
    path('all_staff/', all_staff_view, name='all_staff'),
]
