# parking/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/login/', views.api_post_login, name='api_login'),
    path('api/dashboard_stats/', views.api_get_dashboard_stats, name='api_dashboard_stats'),
    path('api/recent_transactions/', views.api_get_recent_transactions, name='api_recent_transactions'),
    path('api/all_transactions/', views.api_get_all_transactions, name='api_all_transactions'),
    path('api/expiry_notifications/', views.api_get_expiry_notifications, name='api_expiry_notifications'),
    path('api/slots_data/', views.api_get_slots_data, name='api_slots_data'),
    path('api/create_pass/', views.api_post_create_pass, name='api_create_pass'),
    path('api/vehicle_entry/', views.api_post_vehicle_entry, name='api_vehicle_entry'),
    path('api/vehicle_exit/', views.api_post_vehicle_exit, name='api_vehicle_exit'),
    path('api/all_passes/', views.api_get_all_passes, name='api_all_passes'),
]
