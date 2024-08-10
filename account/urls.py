from django.urls import path

from .views import RegisterView, MyLoginView, logout_view

# Setting the namespace for the account app
app_name = "account"

# Defining URL patterns for the account app
urlpatterns = [
    # URL pattern for user registration, using the RegisterView class-based view
    path("register/", RegisterView.as_view(), name="register"),
    # URL pattern for user login, using the MyLoginView class-based view
    path("login/", MyLoginView.as_view(), name="login"),
    # URL pattern for user logout, using the logout_view function-based view
    path("logout/", logout_view, name="logout"),
]
