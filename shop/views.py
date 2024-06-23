from django.shortcuts import render, get_object_or_404, redirect
from .models import ProdCategory, Prod, Contacts, Staff, News
from django.views.decorators.http import require_POST

def shop_view(request):
    categories = ProdCategory.objects.filter(is_visible=True)
    products = Prod.objects.filter(is_visible=True)
    staff = Staff.objects.filter(is_visible=True)
    contacts = Contacts.objects.all()
    news = News.objects.all()
    return render(request, 'shop/shop.html', {
        'categories': categories,
        'products': products,
        'staff': staff,
        'contacts': contacts,
        'news': news,
    })

def product_detail(request, pk):
    product = get_object_or_404(Prod, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'shop/news_detail.html', {'news_item': news_item})

def staff_detail(request, pk):
    staff_member = get_object_or_404(Staff, pk=pk)
    return render(request, 'shop/staff_detail.html', {'staff_member': staff_member})

@require_POST
def add_to_cart(request, pk):
    product = get_object_or_404(Prod, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    if pk in cart:
        cart[pk] += quantity
    else:
        cart[pk] = quantity
    request.session['cart'] = cart
    return redirect('shop')
