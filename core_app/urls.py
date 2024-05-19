from django.urls import path
from core_app import views

urlpatterns = [
    path('inventory-home', views.Home.as_view(), name='inventory-home'),
    path('search-warehouse/', views.search_warehouse, name = 'search-warehouse'),
    path('update_password', views.ChangePassword.as_view(), name='update_password'),
    path('send-forget-password-email', views.SendForgetPasswordEmail.as_view(), name='send-forget-password-email'),
    path('reset-password/<str:token>', views.ResetForgetPassword.as_view(), name='reset-password'),


]
