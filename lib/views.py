from django.shortcuts import render, get_object_or_404
from .models import Article, Type_all
from django.core.paginator import Paginator
from django.db.models.aggregates import Count
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from comment.models import Comment

# Create your views here.
def index(request):
    article_all_list = Article.objects.filter(is_deleted = False)
    paginator = Paginator(article_all_list, 5)
    page_num = request.GET.get('page', 1) #获取页码参数
    page_of_articles = paginator.get_page(page_num)
    dates = Article.objects.datetimes('pub_time', 'month', order='DESC')
    currentr_page_num = page_of_articles.number  # 获取当前页码
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + list(
        range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages)))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    '''
    博客分类计数
    '''
    type_list = Type_all.objects.annotate(num_article=Count('article')).filter(num_article__gt=0)

    context = {}
    context['dates'] = dates
    context['type_num'] = type_list
    context['page_number'] = page_num
    context['page_of_articles'] = page_of_articles
    context['page_range'] = page_range
    context['article_count'] = Article.objects.all().count()
    context['article_dates'] = dates
    return render(request, 'lib/index.html', context)

def detail(request, id):
    article = Article.objects.get(id = id)
    article_content_type = ContentType.objects.get_for_model(article)
    comments = Comment.objects.filter(content_type=article_content_type, object_id=article.pk)

    if not request.COOKIES.get('article_%s_read' % id):
        ct = ContentType.objects.get_for_model(Article)
        if ReadNum.objects.filter(content_type=ct, object_id=article.pk):
            readnum = ReadNum.objects.get(content_type=ct, object_id=article.pk)
        else:
            readnum = ReadNum(content_type=ct, object_id=article.pk)
        readnum.read_number += 1
        readnum.save()

    context = {}
    context['comments'] = comments
    context['previous_article'] = Article.objects.filter(pub_time__gt=article.pub_time).last()
    context['next_article'] = Article.objects.filter(pub_time__lt=article.pub_time).first()
    context['article'] = article
    response = render(request, 'lib/detail.html', context)
    response.set_cookie('article_%s_read' % id, 'true')
    return response

def blogs_with_type(request, blog_type_id):
    context = {}
    type_list = Type_all.objects.annotate(num_article=Count('article')).filter(num_article__gt=0)
    blog_type = get_object_or_404(Type_all, pk = blog_type_id)
    articles = Article.objects.filter(blog_type=blog_type)
    dates = Article.objects.datetimes('pub_time', 'month', order='DESC')
    paginator = Paginator(articles, 5)
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

    context['type_num'] = type_list
    context['article_dates'] = dates
    context['page_range'] = page_range
    context['page_of_articles'] = page_of_articles
    context['blog_type'] = blog_type
    context['blog_types'] = Type_all.objects.all()
    return render(request, 'lib/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    context = {}
    articles = Article.objects.filter(pub_time__year=year, pub_time__month=month)
    paginator = Paginator(articles, 5)
    page_num = request.GET.get('page', 1)  # 获取页码参数
    page_of_articles = paginator.get_page(page_num)
    currentr_page_num = page_of_articles.number #获取当前页码
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context['blog_with_date'] = '%s年%s月' % (year, month)
    context['page_range'] = page_range
    context['page_of_articles'] = page_of_articles
    context['blog_types'] = Type_all.objects.all()
    context['article_dates'] = Article.objects.datetimes('pub_time', 'month', order='DESC')
    return render(request, 'lib/blogs_with_date.html', context)