import scrapy
from ..items import ApNewsItem, ApNewsItem2, GuardianItem, NewsItem
from scrapy.spiders import XMLFeedSpider, SitemapSpider
from scrapy import Spider


class NYTimesSpider(XMLFeedSpider, Spider):
    name = "nytimes_spider"
    start_urls = ['https://www.nytimes.com/sitemaps/new/news.xml.gz']
    namespaces = [
        ('news', 'https://www.nytimes.com/sitemaps/new/news.xml.gz'),
        ('xmlns', "http://www.sitemaps.org/schemas/sitemap/0.9"),
    ]
    itertag = 'url'

    def parse_node(self, response, node):
        item = NewsItem()
        pub_date = node.xpath("//*[local-name()='publication_date']/text()").get()

        if "2021-03-25" in pub_date or "2021-03-26" in pub_date:
            item['headline'] = node.xpath("//*[local-name()='title']/text()").get()
            item['source'] = 'The New York Times'

            item['date_time'] = pub_date

            url = node.xpath("//*[local-name()='loc']/text()").get()
            item['url'] = url
            item['tags'] = node.xpath("//*[local-name()='keywords']/text()").get()

            yield item
