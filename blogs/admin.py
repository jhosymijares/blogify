from django.contrib import admin
from blogs.models import Blog
from blogs.models import Page
from blogs.models import Image

# Blogify admin
admin.site.register(Blog)
admin.site.register(Page)
admin.site.register(Image)