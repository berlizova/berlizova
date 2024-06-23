from django.shortcuts import render
from .models import ProdCategory, Prod, Contacts, Staff, News


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
