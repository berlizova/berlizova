from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import AddToCartForm
from .models import Prod, ProdCategory, Contacts, Staff, News


def shop_view(request):
    """
    Displays the shop homepage with categories, staff, contacts, and news.
    """
    categories = ProdCategory.objects.filter(
        is_visible=True
    )  # Fetch visible product categories
    categories_with_limited_products = []
    for category in categories:
        limited_products = category.prods.filter(is_visible=True)[
            :3
        ]  # Limit to 3 products per category
        categories_with_limited_products.append((category, limited_products))

    staff = Staff.objects.filter(is_visible=True)[:3]  # Fetch visible staff members
    all_staff = Staff.objects.filter(is_visible=True)  # Fetch all visible staff members
    contacts = Contacts.objects.all()  # Fetch contact information
    news = News.objects.all()[:3]  # Fetch latest 3 news items
    all_news = News.objects.all()  # Fetch all news items

    # Render the shop view with the fetched data
    return render(
        request,
        "shop/shop.html",
        {
            "categories_with_limited_products": categories_with_limited_products,
            "staff": staff,
            "all_staff": all_staff,
            "contacts": contacts,
            "news": news,
            "all_news": all_news,
        },
    )


def product_detail(request, pk):
    """
    Displays the detail view of a specific product.
    """
    product = get_object_or_404(Prod, pk=pk)  # Fetch the product by its primary key
    form = AddToCartForm()  # Initialize the form to add the product to the cart
    return render(
        request, "shop/product_detail.html", {"product": product, "form": form}
    )


@require_POST
@login_required(login_url="account:login")
def add_to_cart(request, pk):
    """
    Adds a product to the cart. Requires the user to be logged in.
    """
    product = get_object_or_404(Prod, pk=pk)  # Fetch the product by its primary key
    form = AddToCartForm(request.POST)  # Process the form with POST data
    if form.is_valid():
        quantity = form.cleaned_data["quantity"]
        cart = request.session.get("cart", {})
        if str(pk) in cart:
            cart[
                str(pk)
            ] += quantity  # Update quantity if product is already in the cart
        else:
            cart[str(pk)] = quantity  # Add new product to the cart
        request.session["cart"] = cart
        messages.success(request, f"{product.name} Added to cart.")
    return redirect("shop:product_detail", pk=pk)  # Redirect to product detail page


@login_required(login_url="account:login")
def view_cart(request):
    """
    Displays the cart contents. Requires the user to be logged in.
    """
    cart = request.session.get("cart", {})
    products = []
    total_price = 0
    for pk, quantity in cart.items():
        product = get_object_or_404(Prod, pk=pk)  # Fetch each product in the cart
        products.append(
            {
                "product": product,
                "quantity": quantity,
                "total_price": product.price * quantity,
            }
        )
        total_price += product.price * quantity  # Calculate total price
    return render(
        request, "shop/cart.html", {"products": products, "total_price": total_price}
    )


@login_required(login_url="account:login")
def checkout(request):
    """
    Handles the checkout process. Requires the user to be logged in.
    """
    # Clear the cart after successful payment
    request.session["cart"] = {}
    messages.success(request, "Payment completed successfully.")
    return redirect("shop:view_cart")  # Redirect to the cart view


def category_detail(request, pk):
    """
    Displays the products under a specific category.
    """
    category = get_object_or_404(
        ProdCategory, pk=pk
    )  # Fetch the category by its primary key
    products = category.prods.filter(
        is_visible=True
    )  # Fetch visible products in the category
    return render(
        request,
        "shop/category_detail.html",
        {
            "category": category,
            "products": products,
        },
    )


def news_detail(request, pk):
    """
    Displays the detail view of a specific news item.
    """
    news_item = get_object_or_404(News, pk=pk)  # Fetch the news item by its primary key
    return render(request, "shop/news_detail.html", {"news_item": news_item})


def staff_detail(request, pk):
    """
    Displays the detail view of a specific staff member.
    """
    staff_member = get_object_or_404(
        Staff, pk=pk
    )  # Fetch the staff member by their primary key
    return render(request, "shop/staff_detail.html", {"staff_member": staff_member})


def all_news_view(request):
    """
    Displays a list of all news items.
    """
    news = News.objects.all()  # Fetch all news items
    return render(request, "shop/all_news.html", {"news": news})


def all_staff_view(request):
    """
    Displays a list of all staff members.
    """
    staff = Staff.objects.all()  # Fetch all staff members
    return render(request, "shop/all_staff.html", {"staff": staff})
