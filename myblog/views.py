from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForms, RegForm
from django.contrib.auth.models import User

def home(request):
    context = {}
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForms()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password) # 创建用户
            user.save()
            #登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

            '''
            user = User()
            user.username = username
            user.set_password(password) # 不能直接写user.password = password,因为django对密码的保护机制
            user.email = email
            user.save()
            '''
    else:
        reg_form = RegForm()
    context = {}
    context['regform'] = reg_form
    return render(request, 'register.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):

    context = {}
    return render(request, 'user_info.html', context)