from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('checkotp/', views.CheckOtpView.as_view(), name='check-otp'),
    path('add-address/', views.AddAddressView.as_view(), name='add-address'),
    path('delete-address/<int:pk>/', views.DeleteAddressView.as_view(), name='delete-address'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
]