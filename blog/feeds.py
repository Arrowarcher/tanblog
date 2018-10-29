from django.contrib.syndication.views import Feed

from .models import Post


class AllPostsRssFeed(Feed):
    title = 'Django 博客教程演示项目'
    link = '/'
    description = 'Django 博客教程演示项目测试文章'

    def items(self):            # 需要显示的内容条目
        return Post.objects.all()

    def items_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body