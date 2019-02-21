from django.urls import path
from . import views
app_name = 'lib'
urlpatterns = [
    path('blog/', views.index, name='index'),
    path('detail/<int:id>', views.detail, name='article_detail'),
    path('index/<int:blog_type_id>', views.blogs_with_type, name='blog_with_type'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name="blogs_with_date"),
]