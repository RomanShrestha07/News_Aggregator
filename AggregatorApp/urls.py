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
    path('news-detail/<pk>', NewsDetail.as_view(), name='news-detail'),
    path('mango/', views.news_detail, name='mango'),
]
