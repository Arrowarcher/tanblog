import markdown
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from comments.forms import CommentForm
from .models import Post, Category
# Create your views here.
from django.http import HttpResponse


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []               # 当前页左边连续的页码号，初始值为空
        right = []              # 当前页右边连续的页码号，初始值为空
        left_has_more = False   # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False           # 标示是否需要显示最后一页的页码号。
        last = False

        page_number = page.number   # 获得用户当前请求的页码号
        total_pages = paginator.num_pages   # 获得分页后的总页数
        page_range = paginator.page_range   # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]

        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:
                          (page_number - 1) if (page_number - 1) > 0 else 0]
        right = page_range[page_number:page_number + 2]

        if right:
            if right[-1] < total_pages:
                last = True
            if right[-1] < total_pages - 1:
                right_has_more = True
        if left:
            if left[0] > 1:
                first = True
            if left[0] > 2:
                left_has_more = True

        data = {'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last, }

        return data

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 包含评论
        context = super(PostDetailView,self).get_context_data(**kwargs)   # 先调用父类方法生成context
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(IndexView):
    def get_queryset(self):     #默认获取指定模型的全部列表数据,需复写
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
