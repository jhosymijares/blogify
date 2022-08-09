from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from blogs.models import Blog
from blogs.models import Page
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime
from accounts.models import Profile
from blogs.models import Image
from blogs.models import ImageForm
from django.db.models import ProtectedError

"""
    Blogify Views
"""
def blogify_init(request):
    return redirect('/blogify')

def set_user_context(request, context):
    context["is_authenticated"] = request.user.is_authenticated
    if hasattr(request.user, 'first_name') and request.user.first_name != "":
        context["greeting"] = request.user.first_name
    else:
        context["greeting"] = request.user

def set_header_menu_comtext(context, option):
    context["is_page"] = option
    context["is_blog"] = option
    context["is_img"] = option
    context["is_profile"] = option  
    
def blogify_home(request):
    context = {}
    set_user_context(request, context)
    home_template = loader.get_template("home.html")    
    profiles = Profile.objects.filter(pk=request.user.id)
    if profiles.exists() is True and profiles.first().description != "":
        context["description"] = profiles.first().description
    context["blogs"] = Blog.objects.all().order_by('-creation', '-id')
    context["pages"] = Page.objects.all().order_by('-id').values()   
    set_header_menu_comtext(context,True)
    return HttpResponse(home_template.render(context))    

def image_upload_view(request):
    context = {}
    image_template = loader.get_template("image.html")  
    set_user_context(request, context)    
    context["imageList"] = Image.objects.filter().order_by('-creation')    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            context["form"] = form
            context["img_obj"] = img_obj
            return HttpResponse(image_template.render(context))
    else:
        form = ImageForm()
    context["form"]=form    
    return HttpResponse(image_template.render(context))   

class ImageDelete(DeleteView):
    model = Image
    template_name =   "image_delete.html"
    success_url = "../../images" 

    def delete(self, request, *args, **kwargs):
        context = {}
        self.object = self.get_object()
        img = Image.objects.filter(image = self.object.image)                
        blog = Blog.objects.filter(image = img.first().id)
        profile = Profile.objects.filter(image = img.first().id)
        page = Page.objects.filter(image = img.first().id)
        context["linked_blog"] = None
        context["linked_page"] = None
        context["linked_profile"] = None        
        context["image"] = img.first()
        if len(blog) > 0:
            context["linked_blog"] = blog  
        elif len(page)>0:
            context["linked_page"] = page
        elif len(profile) > 0:
            context["linked_profile"] = profile          
        else:
            self.object.delete()        
            success_url = self.get_success_url()
            return redirect(success_url)
        template = loader.get_template("image_delete.html")
        return HttpResponse(template.render(context))

class PageListView(ListView):
    model = Page
    template_name = "pages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        context['pages'] = Page.objects.filter().order_by('-id')
        set_header_menu_comtext(context, True)    
        context['is_page'] = False
        return context

class PageDetail(DetailView):
    model = Page
    template_name = "page_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        set_header_menu_comtext(context,False)  
        return context

class PageCreate(CreateView):
    model = Page
    template_name = "page_create.html"
    success_url = "../../pages"
    fields = ["title","content"]
    def form_valid(self, form):
        if self.request.POST.get("image") is not None and self.request.POST.get("image")!= "":
            form.instance.image = Image(id=self.request.POST.get("image"))       
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        set_header_menu_comtext(context,False)
        context["images"]=Image.objects.all()
        return context

class PageUpdate(UpdateView):
    model = Page
    template_name  = "page_update.html"
    success_url = "../../pages"
    fields = ["title","content"]

    def form_valid(self, form):
        if self.request.POST.get("image") is not None and self.request.POST.get("image")!= "":
            form.instance.image = Image(id=self.request.POST.get("image"))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        set_header_menu_comtext(context,False)
        context["images"]=Image.objects.all()
        return context

class PageDelete(DeleteView):
    model = Page
    template_name = "page_delete.html"
    success_url = "../../pages" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        set_header_menu_comtext(context,False) 
        return context

class BlogListView(ListView):
    model = Blog
    template_name = "blogs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        context['blogs'] = Blog.objects.filter().order_by('-creation', '-id')
        set_header_menu_comtext(context,True) 
        context['is_blog'] = False        
        return context

class BlogDetail(DetailView):
    model = Blog
    template_name = "blog_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        set_header_menu_comtext(context,False) 
        return context

class BlogCreate(CreateView):
    model = Blog
    template_name = "blog_create.html"
    success_url = "../../blogs"
    fields = ["title","body","image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.subtitle =form.instance.body[0:400]
        if self.request.POST.get("image") is not None and self.request.POST.get("image")!= "":
            form.instance.image = Image(id=self.request.POST.get("image"))
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        set_header_menu_comtext(context,False) 
        context["images"]=Image.objects.all()
        return context

class BlogUpdate(UpdateView):
    model = Blog
    template_name = "blog_update.html"
    success_url = "../../blogs"
    fields = ["title","body"]
    def form_valid(self, form):
        form.instance.subtitle =form.instance.body[0:400]
        if self.request.POST.get("image") is not None and self.request.POST.get("image")!= "":
            form.instance.image = Image(id=self.request.POST.get("image"))
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        set_header_menu_comtext(context,False) 
        context["images"]=Image.objects.all()
        return context

class BlogDelete(DeleteView):
    model = Blog
    template_name = "blog_delete.html"
    success_url = "../../blogs"    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)
        set_header_menu_comtext(context,False)
        return context