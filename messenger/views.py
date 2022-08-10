from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from messenger.models import Chat
from django.db.models import Q
from accounts.models import Profile

"""
    Messenger´s Views
"""
def set_user_context(request, context):
    context["is_authenticated"] = request.user.is_authenticated
    context["greeting"] = request.user
    if hasattr(request.user, 'first_name') and request.user.first_name!="":
        context["greeting"] = request.user.first_name        
    context["profile"] = Profile.objects.filter(user__username=request.user.username).first()

def set_header_menu_comtext(context,option):        
    context["is_show"] = option  

def chat_init(request):
    context = {}
    set_user_context(request,context)
    set_header_menu_comtext(context, False)
    users = []    
    context["users"] = User.objects.all().exclude(username=request.user.username)
    for user in User.objects.all().exclude(username=request.user.username):       
        users.append({
            "username":user.username,
            "full_name": f"{user.first_name}  {user.last_name}",
            "profile":Profile.objects.filter(user__username=user.username).first()
        })   
    context["users"]=users
    chat_template = loader.get_template("chat.html")
    context["firstime"]=True
    return HttpResponse(chat_template.render(context))

def chat_with_user(request, username):
    context={}
    set_user_context(request,context)
    set_header_menu_comtext(context, False)      
    context["user"] = request.user
    
    chats = Chat.objects.filter(
        Q(sender=request.user.username) & Q(receiver=username)
      | Q(sender=username) & Q(receiver=request.user.username)
    )    
    user_avatar = Profile.objects.filter(user__username=request.user.username).first()
    receiver_avatar = Profile.objects.filter(user__username=username).first()
    for chat in chats:
        if chat.sender == request.user.username:     
            chat.avatar = user_avatar            
        else:
            chat.avatar = receiver_avatar         

    context["chats"] = chats
    receiver=[]
    for user in User.objects.all().filter(username=username):       
        receiver.append({
            "username":user.username,
            "full_name": f"{user.first_name} {user.last_name}",
            "profile":Profile.objects.filter(user__username=user.username).first()
        }) 
    context["receiver"]=receiver[0]

    usuario=[] 
    for user in User.objects.all().exclude(username=request.user.username):       
        usuario.append({
            "username":user.username,
            "full_name": f"{user.first_name} {user.last_name}",
            "profile":Profile.objects.filter(user__username=user.username).first()
        }) 
             
    context["users"]=usuario

    if request.method == 'POST':
        if request.POST.get("text") is not None:  
            Chat(sender = request.user,receiver=username,text=request.POST.get("text"),status="Enviado").save() 

    if request.GET.get("param") is not None:       
        chat_template = loader.get_template("just_chat.html")
        context["firstime"]=False
        return HttpResponse(chat_template.render(context))

    context["firstime"] = False
    chat_template = loader.get_template("chat.html")
    return HttpResponse(chat_template.render(context))
