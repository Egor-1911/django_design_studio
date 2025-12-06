from django.urls import path
from . import views
from .views import DesignRequestDeleteView
from .forms import RegistrationForm
from .views import AllDesignRequestsListView
from .views import update_request_status

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/registration/', views.registration, name='registration'),
    path('design-request/', views.design_request_view, name='design_request'),
    path('my-requests/', views.my_requests_view, name='my-requests'),
    path('request/<int:pk>/delete/', DesignRequestDeleteView.as_view(), name='request-delete'),
    path('admin/all-requests/', AllDesignRequestsListView.as_view(), name='all-requests'),
    path('request/<int:request_id>/update-status/', views.update_request_status, name='update-request-status'),
    path('admin/categories/', views.manage_categories, name='manage-categories'),
    path('admin/category/<int:category_id>/delete/', views.delete_category, name='delete-category'),


]


