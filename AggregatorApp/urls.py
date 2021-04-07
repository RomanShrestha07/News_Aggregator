from django.urls import path, include
from . import views
from .views import (SignIn, NewsTable, NewsListView, NewsDetail, SavedNewsListView)

app_name = 'AggregatorApp'
urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('sign-up/', views.signup, name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('profile/', views.update_profile, name='profile'),

    path('process-news/', views.news_processing, name='process-news'),
    path('news-list/', NewsListView.as_view(), name='news-test'),
    path('news-table-1/', NewsTable.as_view(), name='news-table-1'),
    path('news-table-2/', views.news_list_table, name='news-table-2'),
    path('news-detail/<int:year>/<int:month>/<int:day>/<news_id>/<pk>', NewsDetail.as_view(), name='news-detail'),
    path('test-table-2/tag/<slug:tag_slug>/', views.news_list_table, name='news_list_by_tag'),

    path('category/<str:section>/', views.category, name='category'),
    path('top-news/', views.category_top, name='category-top'),

    path('add-tag/<slug:tag_slug>/', views.add_tags, name='add-tag'),
    path('user-feed/', views.user_feed, name='user-feed'),
    path('add-news/<pk>',  views.save_news, name='save-news'),
    path('saved-news/', SavedNewsListView.as_view(), name='saved-news')
]
