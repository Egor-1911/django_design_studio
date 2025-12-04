from django.urls import path
from . import views
from .views import DesignRequestDeleteView
from .forms import RegistrationForm

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/registration/', views.registration, name='registration'),
    path('design-request/', views.design_request_view, name='design_request'),
    path('requests/', views.RequestsCreatedByUserListView.as_view(), name='my-requests'),
    path('request/<int:pk>/delete/', DesignRequestDeleteView.as_view(), name='request-delete'),
]


