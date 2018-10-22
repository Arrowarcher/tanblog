# Register your models here.
from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'text', 'post', 'email', 'url', 'created_time']
