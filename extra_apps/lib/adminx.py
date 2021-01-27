from .models import Article, Type_all
import xadmin
# Register your models here.
class ArticleAdmin:
    list_display = ('id', 'title', 'author', 'pub_time', 'update_time', 'read_num', 'blog_type', 'is_deleted')
    search_fields = ('title', 'author', 'pub_time', 'update_time', 'blog_type', 'is_deleted')
    list_filter = ('title', 'author', 'pub_time', 'update_time', 'blog_type', 'is_deleted')
    ordering = ('id',)
    style_fields = {'text':'ueditor'}

class Type_allAdmin:
    list_display = ('id', 'type_name')
    search_fields = ('type_name')
    ordering = ('id',)
'''
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_number', 'article')
    ordering = ('id',)
'''
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Type_all, Type_allAdmin)
#admin.site.register(ReadNum)
