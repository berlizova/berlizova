from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import CreateView
from .forms import RegisterForm

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

class MyLoginView(LoginView):
    template_name = 'log.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/')

def logout_view(request):
    logout(request)
    return redirect('shop:shop')
