from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    shop_view,
    product_detail,
    news_detail,
    staff_detail,
    category_detail,
    all_news_view,
    all_staff_view,
    add_to_cart,
    view_cart,
    checkout,
)

app_name = 'shop'

urlpatterns = [
    path('', shop_view, name='shop'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('staff/<int:pk>/', staff_detail, name='staff_detail'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    path('all_news/', all_news_view, name='all_news'),
    path('all_staff/', all_staff_view, name='all_staff'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),

]