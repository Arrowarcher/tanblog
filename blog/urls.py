from django.urls import path, re_path
from . import views


app_name = 'blog'   # 告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间。
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # 文章页
    re_path(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    # 归档
    re_path(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    # path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('search/', views.search, name='search'),
]