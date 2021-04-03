import scrapy
from ..items import ApNewsItem, ApNewsItem2, GuardianItem, NewsItem
from scrapy.spiders import XMLFeedSpider, SitemapSpider
from scrapy import Spider


class ReutersSpider(XMLFeedSpider, Spider):
    name = "reuters_spider"
    start_urls = ['https://www.reuters.com/sitemap_news_index1.xml']
    namespaces = [
        ('news', 'https://www.reuters.com/sitemap_news_index1.xml'),
        ('xmlns', "http://www.sitemaps.org/schemas/sitemap/0.9"),
    ]
    itertag = 'url'

    def parse_node(self, response, node):
        item = NewsItem()
        item['headline'] = node.xpath("//*[local-name()='title']/text()").get()
        item['source'] = 'Reuters'
        item['date_time'] = node.xpath("//*[local-name()='publication_date']/text()").get()

        url = node.xpath("//*[local-name()='loc']/text()").get()
        item['url'] = url

        yield scrapy.Request(url, meta={'item': item}, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        old_item = response.request.meta['item']

        selector1 = '//meta[@name="author"]/@content'
        selector2 = '//div[@class="ArticleBodyWrapper"]/p/text()'
        selector3 = '//meta[@name="keywords"]/@content'
        selector4 = '//meta[@name="analyticsAttributes.topicChannel"]/@content'

        author = response.xpath(selector1).get()

        if author == "" or author == 'None' or author == " ":
            old_item['author'] = "Reuters"
        elif not author:
            old_item['author'] = "Reuters"
        else:
            old_item['author'] = author

        con = response.xpath(selector2).getall()
        # old_item['content'] = ' '.join(con)
        old_item['content'] = con

        y = response.xpath(selector3).get()
        if y:
            x = y.split(",")
            old_item['tags'] = x
        else:
            old_item['tags'] = 'No tags'

        old_item['section'] = response.xpath(selector4).get()

        yield old_item
