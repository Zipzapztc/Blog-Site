import string
import random
import time
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from django.core.mail import send_mail
from .forms import LoginForm,RegisterForm,ChangeNicknameForm,BindEmailForm,ChangePasswordForm,ForgetPassword
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
        register_form=RegisterForm(request.POST,request=request)
        if register_form.is_valid():
            username=register_form.cleaned_data['username']
            nickname=register_form.cleaned_data['nickname']
            email=register_form.cleaned_data['email']
            password=register_form.cleaned_data['password']
            new_user=User.objects.create_user(username,email,password)
            new_user.save()
            new_profile=Profile(user=new_user,nickname=nickname)
            new_profile.save()
            del request.session['register_code']

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
    context={}
    return render(request,'user_info.html',context)

def change_nickname(request):
    redirect_to=request.GET.get('from',reverse('home'))
    if request.method=='POST':
        form=ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            new_nickname=form.cleaned_data['new_nickname']
            profile=Profile.objects.get(user=request.user)
            profile.nickname=new_nickname
            profile.save()
            return redirect(redirect_to)
    else:
        form=ChangeNicknameForm()
    
    context={}
    context['profile_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['redirect_to'] = redirect_to
    return render(request,'form.html',context)

def bind_email(request):
    redirect_to=request.GET.get('from',reverse('home'))
    if request.method=='POST':
        form=BindEmailForm(request.POST,request=request)
        if form.is_valid():
            email=form.cleaned_data['email']
            request.user.email=email
            request.user.save()
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form=BindEmailForm()
    
    context={}
    context['profile_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['redirect_to'] = redirect_to
    return render(request,'bind_email.html',context)

def send_verification_code(request):
    email=request.GET.get('email','')
    send_code_for=request.GET.get('send_code_for','')
    data={}
    if email!='':
        verificatin_code=''.join(random.sample(string.ascii_letters+string.digits,4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'FAIL'
        else:
            request.session[send_code_for]=verificatin_code
            request.session['send_code_time'] = now

            send_mail(
                '绑定邮箱',
                '验证码为%s'% verificatin_code,
                '995811384@qq.com',
                [email],
                fail_silently=False,
            )
            data['status']='SUCCESS'
    else:
        data['status']='FAIL'
    return JsonResponse(data)

def change_password(request):
    redirect_to=request.GET.get('from',reverse('home'))
    user=request.user
    if request.method=='POST':
        form=ChangePasswordForm(request.POST,user=user)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            return redirect(redirect_to)
    else:
        form=ChangePasswordForm()
    
    context={}
    context['profile_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['redirect_to'] = redirect_to
    return render(request,'form.html',context)

def forget_password(request):
    redirect_to=reverse('login')
    if request.method=='POST':
        form=ForgetPassword(request.POST,request=request)
        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.get(email=email)
            new_password=form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            del request.session['forget_password_code']
            return redirect(redirect_to)
    else:
        form=ForgetPassword()
    
    context={}
    context['profile_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['redirect_to'] = redirect_to
    return render(request,'forget_password.html',context)