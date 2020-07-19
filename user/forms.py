from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
    password=forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))

    def clean(self):
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']
        user=authenticate(username=username, password=password)
        if user is not None:
            self.cleaned_data['user']=user
        else:
            raise forms.ValidationError('用户名或密码错误')
        return self.cleaned_data

class RegisterForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=30,min_length=3,
                                        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
    nickname=forms.CharField(label='昵称',max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入昵称'}))
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))
    password=forms.CharField(label='密码',max_length=30,min_length=6,
                                        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
    password_again=forms.CharField(label='请再输入一次密码',max_length=30,min_length=6,
                                        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再输入一次密码'}))
    
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已存在')
        return username

    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已存在')
        return email

    def clean_password(self):
        password=self.data['password']
        if password.isalpha() or password.isdigit():
            raise forms.ValidationError('密码中必须包括数字和字母')
        return password
    

    def clean_password_again(self):
        password=self.data['password']
        password_again=self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('密码不一致')
        return password_again

class ChangeNicknameForm(forms.Form):
    new_nickname=forms.CharField(label='昵称',max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入昵称'}))

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user=kwargs.pop('user')
        super().__init__(*args, **kwargs)
    
    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

class BindEmailForm(forms.Form):
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱地址'}))
    verification_code=forms.CharField(label='验证码',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入验证码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user']=self.request.user
        else:
            raise forms.ValidationError('用户未登录')

        verificatin_code=self.request.session.get('bind_email_code','')
        user_code=self.cleaned_data['verification_code']
        if not(verificatin_code!='' and verificatin_code==user_code):
            raise forms.ValidationError('验证码错误')

        return self.cleaned_data
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被绑定')
        return email

