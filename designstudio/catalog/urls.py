from django.urls import path
from . import views
from .forms import RegisterForm

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/', views.register, name='register'),
]
