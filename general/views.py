
'''
此文件为项目通用工具
'''
from django.contrib.auth.models import User
from lib.models import Article, Type_all
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from comment.models import Comment

def paginator(request, article_all_list, context): #  分页器，(request, 要分页的博客列表, 字典)
    paginator = Paginator(article_all_list, 5)
    page_num = request.GET.get('page', 1)  # 获取页码参数
    page_of_articles = paginator.get_page(page_num)
    currentr_page_num = page_of_articles.number  # 获取当前页码
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + list(
        range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context['page_number'] = page_num
    context['page_of_articles'] = page_of_articles
    context['page_range'] = page_range
    return context

def count_Blog(context):  #  分类器及计数器，博客分类计数
    article_list = []
    for type in Type_all.objects.all():
        blogs_count = type.article_set.filter(is_deleted=False).count() #  先筛选出未被标志删除的对象，再计数
        type.num_article = blogs_count
        article_list.append(type)
    article_list2 =[]
    for type in article_list:
        if type.num_article != 0:
            article_list2.append(type)
    context['article_list'] = article_list2
    return context

def get_Comment(context, article): #  获取评论列表
    article_content_type = ContentType.objects.get_for_model(article)
    comments = Comment.objects.filter(content_type=article_content_type, object_id=article.pk)  # 获取文章的评论列表
    context['comments'] = comments
    return context

def get_Readnum(request, article): #  阅读数计数器
    if not request.COOKIES.get('article_%s_read' % article.id):
        ct = ContentType.objects.get_for_model(Article)
        if ReadNum.objects.filter(content_type=ct, object_id=article.pk):
            readnum = ReadNum.objects.get(content_type=ct, object_id=article.pk)
        else:
            readnum = ReadNum(content_type=ct, object_id=article.pk)
        readnum.read_number += 1
        readnum.save()

def blog_dates(context): #  博客时间归档计数器
    dates = Article.objects.dates('pub_time', 'month', order="DESC") #  按月排序
    dates_dict = {}
    for n in dates:
        blog_count = Article.objects.filter(is_deleted=False).filter(pub_time__year=n.year,
                                            pub_time__month=n.month).count()
        dates_dict[n] = blog_count
    context['article_dates'] = dates_dict
    return context