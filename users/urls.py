from django.urls import path

from . import views
from .views import SendOTPView, VerifyOTPView, UserProfileView, UserListView

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('send-otp/', views.SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('dashboard/', views.DashboardView.as_view(), name='profile'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('list/', UserListView.as_view(), name='user-list'),
]

