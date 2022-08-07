"""blogify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
# To Logout session user
from django.contrib.auth.views import LogoutView

#Accounts Routes
urlpatterns = [
    path('', views.account_init, name = 'Init'),
    path('login/', views.account_login, name = 'Login'),
    path('logout/', LogoutView.as_view(), name = 'Logout'),
    path('signup/', views.account_signup, name = 'Signup'),
    path('profile/', views.account_profile, name = 'Profile'),
    path('change/password', views.UpdatePassword.as_view(), name="AccountChangePass")
]
