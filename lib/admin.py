from django.contrib import admin
from .models import Article, Type_all
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'pub_time', 'update_time', 'blog_type', 'read_num', 'is_deleted')
    ordering = ('id',)

class Type_allAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    ordering = ('id',)
'''
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_number', 'article')
    ordering = ('id',)
'''
admin.site.register(Article, ArticleAdmin)
admin.site.register(Type_all)
#admin.site.register(ReadNum)