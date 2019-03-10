from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForms(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=30, min_length=4, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    first_name = forms.CharField(label='昵称', max_length=30, min_length=2, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'昵称不能为空'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱地址'}))
    password = forms.CharField(label='密码',  min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输一次密码'}))
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if User.objects.filter(first_name=first_name).exists():
            raise forms.ValidationError('昵称已存在')
        return first_name
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email
    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

class Change_first_name(forms.Form):
    first_name = forms.CharField(label='请输入新的昵称', max_length=30, min_length=2, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'昵称不能为空'}))
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if first_name == '':
            raise ValidationError('新的昵称不能为空')
        return first_name
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(Change_first_name , self).__init__(*args, **kwargs)
    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data


class Change_pwd(forms.Form):
    old_password = forms.CharField(label='旧密码',  min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入旧密码'}))
    new_password = forms.CharField(label='新密码',  min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入一遍新密码'}))
    new_password_again = forms.CharField(label='再输一遍新密码',  min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再输入一遍新密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(Change_pwd , self).__init__(*args, **kwargs)
    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data
    def clean_password_again(self):
        new_password = self.cleaned_data['password']
        new_password_again = self.cleaned_data['password_again']
        if new_password != new_password_again:
            raise forms.ValidationError('两次输入的新密码不一致')
        return new_password_again