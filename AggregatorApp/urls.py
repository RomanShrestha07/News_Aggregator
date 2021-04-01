from django.urls import path, include
from . import views
from .views import (SignIn, TestTable, NewsListView, NewsDetail)

app_name = 'AggregatorApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('profile/', views.update_profile, name='profile'),
    path('test-table/', TestTable.as_view(), name='test-table'),
    path('news-test/', NewsListView.as_view(), name='news-test'),
    path('news-detail/<int:year>/<int:month>/<int:day>/<news_id>/<pk>', NewsDetail.as_view(), name='news-detail'),
    path('mango/', views.news_processing, name='mango'),
    path('test-table-2/', views.news_list, name='news_list'),
    path('test-table-2/tag/<slug:tag_slug>/', views.news_list, name='news_list_by_tag'),
]
