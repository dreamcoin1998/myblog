from .models import Comment
import xadmin
# Register your models here.
class CommentAdmin:
    list_display = ('content_object', 'text', 'comment_time', 'user')
    search_fields = ('text', 'comment_time', 'user')
    list_filter = ('comment_time', 'user')

xadmin.site.register(Comment, CommentAdmin)
