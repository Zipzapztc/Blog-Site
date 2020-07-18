from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from .forms import LoginForm,RegisterForm
from .models import Profile


def log_in(request):
    if request.method=='POST':
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user=login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form=LoginForm()
    context={}
    context['login_form']=login_form
    return render(request,'login.html',context)

def log_in_for_modal(request):
    login_form=LoginForm(request.POST)
    data={}
    if login_form.is_valid():
        user=login_form.cleaned_data['user']
        login(request, user)
        data['status']='SUCCESS'   
    else:
        data['status']='FAIL'
    return JsonResponse(data)

def register(request):
    if request.method=='POST':
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            username=register_form.cleaned_data['username']
            email=register_form.cleaned_data['email']
            password=register_form.cleaned_data['password']
            new_user=User.objects.create_user(username,email,password)
            new_user.save()

            user=authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        register_form=RegisterForm()
    context={}
    context['register_form']=register_form
    return render(request,'register.html',context)

def log_out(request):
    logout(request)
    return redirect(request.GET.get('from',reverse('home')))

def user_info(request):
    user=request.user
    context={}
    context['profile']=Profile.objects.get(user=user)
    return render(request,'user_info.html',context)

