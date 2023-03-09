from django.shortcuts import render
from django import forms
from django.utils import timezone

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

# 通过form模式 把数据展示回去前端


def login(request):
    ''''
    
    '''
    login_time = timezone.now() # 获取服务器当前时间
    request.session['last_login'] = login_time # 记录登录时间

    return render(request, 'login/login.html')