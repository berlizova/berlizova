from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import RegisterForm
from django.contrib import messages


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'An error occurred during registration. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))


class MyLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(self.request, 'User does not exist. Please register')
            return redirect('account:register')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', '/')


def logout_view(request):
    logout(request)
    return redirect('shop:shop')
