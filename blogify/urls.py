from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

#Blogify Routes
urlpatterns = [    
    path('admin/', admin.site.urls),
    path('', views.Init, name = 'Init'),
    path('blogify/', views.Home, name = 'Home'),
    path('accounts/', include('accounts.urls'), name = 'Accounts'),
    path('blogify/chat/', include('messenger.urls'), name = 'Chat'),
    path('blogify/images/', login_required(views.Images), name = "Images"),
    path(r'blogify/image/delete/(?P<pk>\d+)$', login_required(views.ImageDelete.as_view()), name= 'ImageDelete'),
    path('blogify/acerca-de-mi', views.AboutMeListView.as_view(), name = "AboutMe"),    
    path(r'blogify/page/detail-acerca-de-mi/(?P<pk>\d+)$', login_required(views.AboutMeDetail.as_view()), name = 'AboutMeDetail'),
    path(r'blogify/page/crear-acerca-de-mi/', login_required(views.AboutMeCreate.as_view()), name = 'AboutMeCreate'),
    path(r'blogify/page/actualizar-acerca-de-mi/(?P<pk>\d+)$', login_required(views.AboutMeUpdate.as_view()), name= 'AboutMeUpdate'),
    path(r'blogify/page/eliminar-acerca-de-mi/(?P<pk>\d+)$', login_required(views.AboutMeDelete.as_view()), name= 'AboutMeDelete'),
    path('blogify/blogs', views.BlogListView.as_view(), name = "Blogs"),
    path(r'blogify/blog/(?P<pk>\d+)$', login_required(views.BlogDetail.as_view()), name = 'BlogDetail'),
    path(r'blogify/blog/create/', login_required(views.BlogCreate.as_view()), name = 'BlogCreate'),
    path(r'blogify/blog/update/(?P<pk>\d+)$', login_required(views.BlogUpdate.as_view()), name= 'BlogUpdate'),
    path(r'blogify/blog/delete/(?P<pk>\d+)$', login_required(views.BlogDelete.as_view()), name= 'BlogDelete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
