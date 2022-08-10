from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

#Messenger´s Routes
urlpatterns = [
    path('', login_required(views.chat_init), name = 'ChatInit'),
    path('with/<str:username>/',login_required(views.chat_with_user), name = 'ChatWithUser')
]
