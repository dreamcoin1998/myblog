from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Article, Type_all
from general.views import paginator, count_Blog, get_Comment, get_Readnum, blog_dates
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType

def index(request):
    context = {}
    article_all_list = Article.objects.filter(is_deleted=False) #  获取所有的博客对象
    blog_dates(context)
    paginator(request, article_all_list, context) #  调用博客内容分页函数
    count_Blog(context) #  博客分类计数
    return render(request, 'lib/index.html', context)

def detail(request, id):
    context = {}
    article = Article.objects.get(id = id)
    article_content_type = ContentType.objects.get_for_model(article)
    comments = Comment.objects.filter(content_type=article_content_type, object_id=article.pk)
    get_Comment(context, article) #  获得评论列表
    get_Readnum(request, article) #  获得阅读数
    context['previous_article'] = Article.objects.filter(is_deleted=False).filter(pub_time__gt=article.pub_time).last() #  获取上一片博客
    context['next_article'] = Article.objects.filter(is_deleted=False).filter(pub_time__lt=article.pub_time).first() #  获取下一片博客
    context['article'] = article
    context['comments'] = comments
    response = render(request, 'lib/detail.html', context)
    response.set_cookie('article_%s_read' % id, 'true')
    return response

def blogs_with_type(request, blog_type_id):
    context = {}
    blog_dates(context)
    count_Blog(context) #  获取博客分类计数
    blog_type = get_object_or_404(Type_all, pk = blog_type_id)
    articles = Article.objects.filter(blog_type=blog_type).filter(is_deleted=False)
    paginator(request, articles, context)
    context['blog_type'] = blog_type
    context['blog_types'] = Type_all.objects.all()
    return render(request, 'lib/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    context = {}
    blog_dates(context)
    count_Blog(context)
    articles = Article.objects.filter(pub_time__year=year, pub_time__month=month).filter(is_deleted=False) #  按年和月筛选
    paginator(request, articles, context)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    context['blog_types'] = Type_all.objects.all()
    return render(request, 'lib/blogs_with_date.html', context)


def search(request):
    context = {}
    blog_dates(context)
    try:
        wd = request.GET['wd']
        if not wd:
            return render(request, 'lib/index.html')
        blogs = Article.objects.filter(is_deleted=False).filter(title__contains=wd)
        paginator(request, blogs, context)
        context["wd"] = wd
        count_Blog(context)
    except Exception:
        raise Http404
    return render(request, 'lib/blog_search.html', context)
