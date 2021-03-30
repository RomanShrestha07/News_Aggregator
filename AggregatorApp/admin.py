from django.contrib import admin
from .models import AddedSources, BlockedSources, RawNews, Profile, News

admin.site.register(Profile)
admin.site.register(AddedSources)
admin.site.register(BlockedSources)


@admin.register(RawNews)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'source', 'date_time', 'tags')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_id', 'headline', 'source', 'author', 'date_time')
