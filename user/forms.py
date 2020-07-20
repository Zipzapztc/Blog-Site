from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username_or_email=forms.CharField(label='用户名或邮箱',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名或邮箱'}))
    password=forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))

    def clean(self):
        username_or_email=self.cleaned_data['username_or_email']
        password=self.cleaned_data['password']
        user=authenticate(username=username_or_email, password=password)
        if user is not None:
            self.cleaned_data['user']=user
        else:
            if User.objects.filter(email=username_or_email).exists():
                username=User.objects.get(email=username_or_email)
                user=authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user']=user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码错误')
        return self.cleaned_data
        
class RegisterForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=30,min_length=3,
                                        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
    nickname=forms.CharField(label='昵称',max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入昵称'}))
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))
    password=forms.CharField(label='密码',max_length=30,min_length=6,
                                        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
    password_again=forms.CharField(label='再次输入密码',max_length=30,min_length=6,
                                        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再输入一次密码'}))
    verification_code=forms.CharField(label='验证码',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'点击“发送验证码”在邮箱获取验证码'}))
    
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

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
    
    def clean_verification_code(self):
        verification_code=self.request.session.get('register_code','')
        user_code=self.cleaned_data['verification_code']
        if not(verification_code!='' and verification_code==user_code):
            raise forms.ValidationError('验证码错误')
        return verification_code

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
    verification_code=forms.CharField(label='验证码',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'点击“发送验证码”在邮箱获取验证码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user']=self.request.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被绑定')
        return email
    
    def clean_verification_code(self):
        verification_code=self.request.session.get('bind_email_code','')
        user_code=self.cleaned_data['verification_code']
        if not(verification_code!='' and verification_code==user_code):
            raise forms.ValidationError('验证码错误')
        return verification_code

class ChangePasswordForm(forms.Form):
    old_password=forms.CharField(label='旧密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入旧密码'}))
    new_password=forms.CharField(label='新密码',max_length=30,min_length=6,
                                            widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新密码'}))
    new_password_again=forms.CharField(label='再次输入新密码',max_length=30,min_length=6,
                                            widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再输入一次新密码'}))

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user=kwargs.pop('user')
        super().__init__(*args, **kwargs)
    
    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用户未登录')
        
        new_password=self.cleaned_data['new_password']
        new_password_again=self.cleaned_data['new_password_again']
        if new_password!=new_password_again:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        old_password=self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码错误')
        return old_password

class ForgetPassword(forms.Form):
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入绑定的邮箱地址'}))
    verification_code=forms.CharField(label='验证码',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'点击“发送验证码”在邮箱获取验证码'}))
    new_password=forms.CharField(label='新密码',max_length=30,min_length=6,
                                            widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新密码'}))
    new_password_again=forms.CharField(label='再次输入新密码',max_length=30,min_length=6,
                                            widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再输入一次新密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        new_password=self.cleaned_data['new_password']
        new_password_again=self.cleaned_data['new_password_again']
        if new_password!=new_password_again:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data
        
    def clean_email(self):
        email=self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email
    
    def clean_verification_code(self):
        verification_code=self.request.session.get('forget_password_code','')
        user_code=self.cleaned_data['verification_code']
        if not(verification_code!='' and verification_code==user_code):
            raise forms.ValidationError('验证码错误')
        return verification_code