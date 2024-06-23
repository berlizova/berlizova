from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Prod, ProdCategory, Contacts, Staff, News
from .forms import AddToCartForm
from account.forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import CreateView
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
    form = AddToCartForm()
    return render(request, 'shop/product_detail.html', {'product': product, 'form': form})


@require_POST
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Prod, pk=pk)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart = request.session.get('cart', {})
        if str(pk) in cart:
            cart[str(pk)] += quantity
        else:
            cart[str(pk)] = quantity
        request.session['cart'] = cart
        messages.success(request, f'{product.name} добавлен в корзину.')
    return redirect('shop:product_detail', pk=pk)


@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0
    for pk, quantity in cart.items():
        product = get_object_or_404(Prod, pk=pk)
        products.append({'product': product, 'quantity': quantity, 'total_price': product.price * quantity})
        total_price += product.price * quantity
    return render(request, 'shop/cart.html', {'products': products, 'total_price': total_price})


@login_required
def checkout(request):
    # Обработка оплаты
    request.session['cart'] = {}
    messages.success(request, 'Оплата успешно выполнена.')
    return redirect('shop:view_cart')


def category_detail(request, pk):
    category = get_object_or_404(ProdCategory, pk=pk)
    products = category.prods.filter(is_visible=True)
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products,
    })


def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'shop/news_detail.html', {'news_item': news_item})


def staff_detail(request, pk):
    staff_member = get_object_or_404(Staff, pk=pk)
    return render(request, 'shop/staff_detail.html', {'staff_member': staff_member})


def all_news_view(request):
    news = News.objects.all()
    return render(request, 'shop/all_news.html', {'news': news})


def all_staff_view(request):
    staff = Staff.objects.all()
    return render(request, 'shop/all_staff.html', {'staff': staff})


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
