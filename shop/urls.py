from django.urls import path

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

# Set the application namespace
app_name = "shop"

# Define the URL patterns for the 'shop' application
urlpatterns = [
    path("", shop_view, name="shop"),  # Home page displaying the shop view
    path(
        "product/<int:pk>/", product_detail, name="product_detail"
    ),  # Product detail page
    path("news/<int:pk>/", news_detail, name="news_detail"),  # News detail page
    path("staff/<int:pk>/", staff_detail, name="staff_detail"),  # Staff detail page
    path(
        "category/<int:pk>/", category_detail, name="category_detail"
    ),  # Category detail page
    path("all_news/", all_news_view, name="all_news"),  # Page listing all news items
    path(
        "all_staff/", all_staff_view, name="all_staff"
    ),  # Page listing all staff members
    path(
        "add_to_cart/<int:pk>/", add_to_cart, name="add_to_cart"
    ),  # Add a product to the cart
    path("cart/", view_cart, name="view_cart"),  # View the contents of the cart
    path(
        "checkout/", checkout, name="checkout"
    ),  # Checkout page for completing purchases
]
