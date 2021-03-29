from django.contrib import admin
from .models import AddedSources, BlockedSources, News, Profile

admin.site.register(Profile)
admin.site.register(AddedSources)
admin.site.register(BlockedSources)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'source', 'date_time', 'tags')
