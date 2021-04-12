from django.contrib import admin
from .models import BlockedSources, RawNews, Profile, News, SavedNews, Comment

admin.site.register(Profile)
admin.site.register(SavedNews)
admin.site.register(BlockedSources)


@admin.register(RawNews)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'source', 'date_time', 'tags')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_id', 'headline', 'source', 'author', 'date_time')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'body')
