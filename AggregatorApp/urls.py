from django.urls import path, include
from . import views
from .views import (SignIn, NewsTable, NewsListView, NewsDetail)

app_name = 'AggregatorApp'
urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('profile/', views.update_profile, name='profile'),

    path('process-news/', views.news_processing, name='process-news'),
    path('news-list/', NewsListView.as_view(), name='news-test'),
    path('news-table-1/', NewsTable.as_view(), name='news-table-1'),
    path('news-table-2/', views.news_list_table, name='news-table-2'),
    path('news-detail/<int:year>/<int:month>/<int:day>/<news_id>/<pk>', NewsDetail.as_view(), name='news-detail'),
    path('test-table-2/tag/<slug:tag_slug>/', views.news_list_table, name='news_list_by_tag'),

    path('category/world/', views.category_world_news, name='category-world'),
    path('category/sports/', views.category_sports, name='category-sports'),
    path('category/business/', views.category_business, name='category-business'),
    path('category/science-technology/', views.category_science_technology, name='category-science-technology'),
    path('category/entertainment/', views.category_entertainment, name='category-entertainment'),
    path('category/culture/', views.category_culture, name='category-culture'),
    path('category/opinion/', views.category_opinion, name='category-opinion'),
    path('category/politics/', views.category_politics, name='category-politics'),
    path('category/environment/', views.category_environment, name='category-environment'),
    path('category/other/', views.category_other, name='category-other'),
]
