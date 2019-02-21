from django.contrib import admin
from .models import ReadNum
# Register your models here.
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_number', 'content_object')
    ordering = ('id',)

admin.site.register(ReadNum)