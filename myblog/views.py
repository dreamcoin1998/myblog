from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForms, RegForm, Change_first_name, Change_pwd
from django.contrib.auth.models import User
from extra_apps.lib.models import Article
from general.views import count_Blog, blog_dates


def home(request):
    context = {}
    blog_dates(context)
    article = Article.objects.filter(is_deleted=False)
    count_Blog(context)
    context['article_count'] = article.count()
    return render(request, 'home.html', context)

def login(request):
    context = {}
    if request.method == 'POST':
        login_form = LoginForms(request.POST)
        if login_form.is_valid(): #  调用is_valid()方法来执行绑定表单的数据验证工作，并返回一个表示数据是否合法的布尔值
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForms()

    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            first_name = reg_form.cleaned_data['first_name']
            user = User.objects.create_user(username, email, password) # 创建用户
            user.first_name = first_name
            user.save()
            #登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
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

def change_first_name(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = Change_first_name(request.POST, user=request.user)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            user = request.user
            user.first_name = first_name
            user.save()
            return redirect(redirect_to)
    else:
        form = Change_first_name()

    context = {}
    context['tip_text1'] = '请修改您的昵称'
    context['tip_text2'] = '你可以任意修改您的昵称，除非它已经存在'
    context['page_title'] = '高俊斌的个人网站|昵称修改'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '提交修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = Change_pwd(request.POST, user=request.user)
        if form.is_valid():
            username = request.user.username
            old_password = form.cleaned_data['old_password']
            auth_user = auth.authenticate(username=username, password=old_password)
            if auth_user is not None:
                newpassword = form.cleaned_data['new_password']
                user = request.user
                user.set_password(newpassword)
                user.save()
                auth.login(request, user)
                return redirect(redirect_to)
    else:
        form = Change_pwd()

    context = {}
    context['tip_text1'] = '请修改您的密码'
    context['tip_text2'] = '请记好您的新密码'
    context['page_title'] = '高俊斌的个人网站|密码修改'
    context['form_title'] = '修改密码'
    context['submit_text'] = '确定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)
