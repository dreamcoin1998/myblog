from django.db import models
from django.contrib.auth.admin import User
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from django.db.models.fields import exceptions
from DjangoUeditor.models import UEditorField

class test():
    @property
    def read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_number
        except exceptions.ObjectDoesNotExist:
            return 0

class Type_all(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name
    class Meta:
        verbose_name = '文章类型'
        verbose_name_plural = verbose_name

class Article(models.Model, test):
    title = models.CharField(max_length=50, verbose_name="标题")
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    text = UEditorField(blank=False, verbose_name="正文")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    blog_type = models.ForeignKey(Type_all, on_delete=models.DO_NOTHING, verbose_name="文章类型")
    class Meta:
        ordering = ['-pub_time']
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
