from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.views.decorators.http import require_POST
from account.forms import RegisterForm
from .models import ProdCategory, Prod, Contacts, Staff, News
from django.contrib import messages
from django.contrib.auth.models import User

def shop_view(request):
    categories = ProdCategory.objects.filter(is_visible=True)
    categories_with_limited_products = []
    for category in categories:
        limited_products = category.prods.filter(is_visible=True)[:3]
        categories_with_limited_products.append((category, limited_products))

    staff = Staff.objects.filter(is_visible=True)[:3]
    all_staff = Staff.objects.filter(is_visible=True)
    contacts = Contacts.objects.all()
    news = News.objects.all()[:3]
    all_news = News.objects.all()
    return render(request, 'shop/shop.html', {
        'categories_with_limited_products': categories_with_limited_products,
        'staff': staff,
        'all_staff': all_staff,
        'contacts': contacts,
        'news': news,
        'all_news': all_news,
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

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.')
        return self.render_to_response(self.get_context_data(form=form))

class MyLoginView(LoginView):
    template_name = 'log.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(self.request, 'Пользователь не существует. Пожалуйста, зарегистрируйтесь.')
            return redirect('account:register')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', '/')

def logout_view(request):
    logout(request)
    return redirect('shop:shop')

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
    return redirect('shop:product_detail', pk=pk)

def category_detail(request, pk):
    category = get_object_or_404(ProdCategory, pk=pk)
    products = category.prods.filter(is_visible=True)
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products,
    })

def all_news_view(request):
    news = News.objects.all()
    return render(request, 'shop/all_news.html', {'news': news})

def all_staff_view(request):
    staff = Staff.objects.all()
    return render(request, 'shop/all_staff.html', {'staff': staff})
