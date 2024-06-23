from django.urls import path
from .views import RegisterView, MyLoginView, logout_view

app_name = 'account'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
