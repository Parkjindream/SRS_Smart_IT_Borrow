from django.urls import path
from . import views

urlpatterns = [
    path('api/create/', views.create_booking, name='create_booking'),
    path('api/status/<str:booking_ref>/', views.check_booking_status, name='check_status'),
    path('api/admin/pickup/', views.admin_scan_pickup, name='admin_pickup'),
    path('api/admin/return/', views.admin_scan_return, name='admin_return'),
]