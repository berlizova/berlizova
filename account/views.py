from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import RegisterForm


# View for handling user registration
class RegisterView(CreateView):
    template_name = "register.html"  # Template to be used for registration
    form_class = RegisterForm  # Form class for registration
    success_url = "/"  # URL to redirect to upon successful registration

    def form_valid(self, form):
        """
        This method is called when the form is valid.
        It authenticates and logs in the user after registration.
        """
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)  # Log the user in
        messages.success(
            self.request, "Registration successful. You are now logged in."
        )
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """
        This method is called when the form is invalid.
        It adds an error message and re-renders the form with the provided data.
        """
        messages.error(
            self.request, "An error occurred during registration. Please try again."
        )
        return self.render_to_response(self.get_context_data(form=form))


# Custom login view for handling user login
class MyLoginView(LoginView):
    template_name = "login.html"  # Template to be used for login

    def form_valid(self, form):
        """
        This method is called when the login form is valid.
        It checks if the user exists and proceeds with the login process.
        """
        username = form.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(self.request, "User does not exist. Please register")
            return redirect("register")
        return super().form_valid(form)

    def get_success_url(self):
        """
        Returns the URL to redirect to after login.
        If 'next' is provided in the GET parameters, it will redirect to that URL.
        Otherwise, it redirects to the homepage.
        """
        return self.request.GET.get("next", "/")


# View for handling user logout
def logout_view(request):
    logout(request)  # Log the user out
    return redirect("shop:shop")  # Redirect to the shop homepage
