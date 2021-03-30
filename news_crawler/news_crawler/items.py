# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from AggregatorApp.models import RawNews


class ApNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    headline = scrapy.Field()
    author = scrapy.Field()
    date_time = scrapy.Field()
    url = scrapy.Field()


class ApNewsItem2(scrapy.Item):
    _id = scrapy.Field()
    headline = scrapy.Field()
    source = scrapy.Field()
    author = scrapy.Field()
    date_time = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()


class NewsItem(DjangoItem):
    django_model = RawNews


class GuardianItem(scrapy.Item):
    headline = scrapy.Field()
    author = scrapy.Field()
    date_time = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
