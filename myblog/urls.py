"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
import xadmin


urlpatterns = [
    path('', include('lib.urls')),
    path('xadmin/', xadmin.site.urls),
    path('', views.home, name='home'),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_info/', views.user_info, name='user_info'),
    path('comment/', include('comment.urls')),
    path('change_first_name/', views.change_first_name, name='change_first_name'),
    path('change_pwd/', views.change_password, name='change_pwd'),
]

urlpatterns += static(settings.STATIC_URL + "uepload", document_root = settings.STATIC_URL + "uepload")
