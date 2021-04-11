from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from .views import (SignIn, NewsDetail, SavedNewsDetail)

app_name = 'AggregatorApp'
urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('sign-up/', views.signup, name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('profile/', views.view_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update-profile'),

    path('process-news/', views.news_processing, name='process-news'),
    path('news-detail/<int:year>/<int:month>/<int:day>/<news_id>/<pk>', NewsDetail.as_view(), name='news-detail'),

    path('category/<str:section>/', views.category, name='category'),
    path('source/<str:source>/', views.news_by_source, name='news-by-source'),
    path('tag/<slug:tag_slug>/', views.news_by_tag, name='news_list_by_tag'),
    path('date/<str:date>/', views.news_by_date, name='news-by-date'),

    path('add-tag/<slug:tag_slug>/', views.add_tags, name='add-tag'),
    path('view-tags/', views.added_tags_list, name='added-tags-list'),
    path('remove-tag/<slug:tag_slug>/', views.remove_tags, name='remove-tag'),
    path('user-feed/', views.user_feed, name='user-feed'),

    path('add-news/<pk>', views.save_news, name='save-news'),
    path('saved-news/', views.saved_news_list_view, name='saved-news'),
    path('saved-news-detail/<int:id>/<int:year>/<int:month>/<int:day>/<pk>', login_required(SavedNewsDetail.as_view()),
         name='saved-news-detail'),
    path('saved-news-delete/<pk>', views.saved_news_delete, name='saved-news-delete'),
]
