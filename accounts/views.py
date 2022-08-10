from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from blogs.models import Image

"""
    Accounts Views
"""
def set_user_context(request, context):
    context["is_authenticated"] = request.user.is_authenticated
    if hasattr(request.user, 'first_name') and request.user.first_name!="":
        context["greeting"] = request.user.first_name
    else:
        context["greeting"] = request.user
    context["profile"] = Profile.objects.filter(user__username=request.user.username).first()

def account_init(request):
    if(request.user.is_authenticated):
        return redirect('profile/')
    else:
        return redirect('login/')

def account_login(request):
    if(request.user.is_authenticated):
        return redirect('/')   
    login_template = loader.get_template("login.html")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            auth = authenticate(username=username,
                                password=password)
            
            if auth is not None:
                login(request, auth)
                print(auth.is_superuser)
                next = request.GET.get("next", None)
                if next is not None:
                    print(next)
                    return redirect(next)
                else:
                    return redirect("/")            
            else:
                return HttpResponse(login_template.render({
                    "message":"Error, datos incorrectos"
                }))
                
        else:
            return HttpResponse(login_template.render({
                "message":"Error, datos incorrectos"
            })) 

    return HttpResponse(login_template.render({        
        "form": AuthenticationForm()
    }))

def account_profile(request):
    context = {}
    set_user_context(request, context)
    profile_template = loader.get_template("profile.html")
    user = User.objects.get(pk=request.user.id)  
    context["user"] = user
            
    if request.method == 'POST':
        if request.POST.get("first_name") is not None:            
            user.first_name=request.POST.get("first_name") 
        if request.POST.get("last_name") is not None:  
            user.last_name=request.POST.get("last_name") 
        if request.POST.get("email") is not None:  
            user.email=request.POST.get("email")         

        if request.POST.get("image") is not None or request.POST.get("description") is not None or request.POST.get("url_site") is not None:
            if Profile.objects.filter(pk = request.user.id).exists() is False:
               Profile(user = user, description = "", url_site="").save()              
            profile = Profile.objects.get(pk = request.user.id)

            if request.POST.get("image") is not None and request.POST.get("image")!= "":                         
                profile.image = Image(id = request.POST.get("image"))  
                profile.save() 
                profile = Profile.objects.get(pk = request.user.id)

            if request.POST.get("description") is not None:    
                profile.description=request.POST.get("description") 

            if request.POST.get("url_site") is not None:  
                profile.url_site=request.POST.get("url_site")           

            context["profile"] = profile
            profile.save()
        user.save()        
        
        context["message"]="Tu perfil ha sido actualizado"
    
    context["images"]=Image.objects.all()

    return HttpResponse(profile_template.render(context))
class UpdatePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = '/accounts/profile/'
    template_name = 'resetpass.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        set_user_context(self.request,context)        
        return context    

def account_signup(request):
    signup_template = loader.get_template("signup.html")    
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            new_user = User.objects.create_user(username,"automatic@email.com",password)

            new_user.first_name=request.POST.get('first_name')
            new_user.last_name=request.POST.get('last_name')
            new_user.email=request.POST.get('email')
            new_user.save()
           
            return HttpResponse(signup_template.render({
                "mensaje": f"Registro exitoso usuario: {username}"
            }))
        else:
            return HttpResponse(signup_template.render({
                "mensaje": "Error por favor valide los datos ingresados",
                "form": UserCreationForm()
            }))
    return HttpResponse(signup_template.render({
        "form": UserCreationForm()
    }))