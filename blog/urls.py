from django.urls import path
from . import views


app_name = 'blog'   # 告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间。
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
]