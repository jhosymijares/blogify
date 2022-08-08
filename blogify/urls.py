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
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

#Blogify Routes
urlpatterns = [    
    path('admin/', admin.site.urls),
    path('', views.blogify_init, name = 'BlogifyInit'),
    path('blogify/', views.blogify_home, name = 'BlogifyHome'),
    path('accounts/', include('accounts.urls'), name = 'Accounts'),
    path('blogify/messenger/', include('messenger.urls'), name = 'Messenger'),

    path('blogify/images/', login_required(views.image_upload_view), name = "BlogifyImages"),
    path(r'blogify/image/delete/(?P<pk>\d+)$', login_required(views.ImageDelete.as_view()), name= 'BlogifyImageDelete'),

    path('blogify/pages', views.PageListView.as_view(), name = "BlogifyPageList"),
    path(r'blogify/page/(?P<pk>\d+)$', login_required(views.PageDetail.as_view()), name = 'BlogifyPageDetail'),
    path(r'blogify/page/create/', login_required(views.PageCreate.as_view()), name = 'BlogifyPageCreate'),
    path(r'blogify/page/update/(?P<pk>\d+)$', login_required(views.PageUpdate.as_view()), name= 'BlogifyPageUpdate'),
    path(r'blogify/page/delete/(?P<pk>\d+)$', login_required(views.PageDelete.as_view()), name= 'BlogifyPageDelete'),
    
    path('blogify/blogs', views.BlogListView.as_view(), name = "BlogifyBlogsList"),
    path(r'blogify/blog/(?P<pk>\d+)$', login_required(views.BlogDetail.as_view()), name = 'BlogifyBlogsDetail'),
    path(r'blogify/blog/create/', login_required(views.BlogCreate.as_view()), name = 'BlogifyBlogCreate'),
    path(r'blogify/blog/update/(?P<pk>\d+)$', login_required(views.BlogUpdate.as_view()), name= 'BlogifyBlogUpdate'),
    path(r'blogify/blog/delete/(?P<pk>\d+)$', login_required(views.BlogDelete.as_view()), name= 'BlogifyBlogDelete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
