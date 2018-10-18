import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.
from django.http import HttpResponse

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 渲染文章内容为markdown
    post.body = markdown.markdown(post.body, extensions=['markdown.extensions.extra',
                                                         'markdown.extensions.codehilite',
                                                         'markdown.extensions.toc',
                                                         ])
    # Markdown 语法的拓展:
    # extra 本身包含很多拓展
    # codehilite 是语法高亮拓展
    # toc 则允许我们自动生成目录
    return render(request, 'blog/detail.html', context={'post': post})