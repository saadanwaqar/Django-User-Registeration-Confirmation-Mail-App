from django.contrib import auth
from . models import Profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# email setting imports
import uuid
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def index(request):
    return render(request,'blog/index.html')


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        email = request.POST.get('email') 
        pass1 = request.POST.get('pass1') 
        pass2 = request.POST.get('pass2') 
        cust = User.objects.filter(email=email)
        cust1 = User.objects.filter(username=username)
        if pass1 != pass2:
            messages.error(request,'Passwords doesnot Match ')
            return redirect('index') 
        if cust and cust1 :
            messages.error(request,'E-Mail already exists')
            return redirect('index') 
        myuser = User.objects.create(username=username,email=email)
        myuser.set_password(pass1)
        myuser.save()
        # email setting code
        auth_token = str(uuid.uuid4()) 
        profile_obj = Profile.objects.create(user=myuser, auth_token= auth_token )
        profile_obj.save()
        send_mail_reg(email,auth_token)
        messages.success(request,'Your account has been created sucessfully. To Login Check your mail box and confirm mail')    
        return redirect('index')
    else:
        return HttpResponse("404 Not Found")

      


def handleLogin(request):
    if request.method=='POST': 
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(username=username,password=pass1)
        
        if user is not None:
            profile = Profile.objects.filter(user=user).first()
            if not profile.is_verified :
                messages.success(request,'Check Your E-Mail and Verify your mail')
                return redirect('index')

            
            login(request,user)
            messages.success(request,'You Login sucessfully')
            return redirect('index')
        else:  
            messages.error(request,'Invalid Crediants')
            return redirect('index')
            
    else:
        return HttpResponse("404 Not Found")           




def handleLogout(request):
    logout(request)
    messages.success(request,'You Logout succesfully ')
    return redirect('index')


    # E-Mail Setup

def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,"Your account already has been verified")
            return redirect('index')
        else:    
            profile_obj.is_verified = True   
            messages.success(request,'Your Mail is verified, Now you can Login')  
            profile_obj.save()
            return redirect('index')
    else:
        return HttpResponse("<h1>404 Page Not Found</h1>")   
             
def send_mail_reg(email, token ):
    
    subject = "Your accounts need to be verified"
    message = f"Hi paste the link to verify your account http://127.0.0.1:8000/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list  = [email]
    send_mail( subject,message,email_from,recipient_list)