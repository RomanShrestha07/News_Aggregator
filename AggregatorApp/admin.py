from django.contrib import admin
from .models import BlockedSources, RawNews, Profile, News, SavedNews

admin.site.register(Profile)
admin.site.register(SavedNews)
admin.site.register(BlockedSources)


@admin.register(RawNews)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'source', 'date_time', 'tags')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_id', 'headline', 'source', 'author', 'date_time')
