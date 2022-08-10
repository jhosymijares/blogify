from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

""""
Accounts Routes
"""
urlpatterns = [
    path('', views.account_init, name = 'Init'),
    path('login/', views.account_login, name = 'Login'),
    path('logout/', LogoutView.as_view(), name = 'Logout'),
    path('signup/', views.account_signup, name = 'Signup'),
    path('profile/', login_required(views.account_profile), name = 'Profile'),
    path('change/password', login_required(views.UpdatePassword.as_view()), name="AccountChangePass")
]
