import scrapy
from ..items import ApNewsItem, ApNewsItem2, GuardianItem, NewsItem
from scrapy.spiders import XMLFeedSpider, SitemapSpider
from scrapy import Spider


class GuardianSpider(XMLFeedSpider, Spider):
    name = "guardian_spider"
    start_urls = ['https://www.theguardian.com/sitemaps/news.xml']
    namespaces = [
        ('news', 'https://www.theguardian.com/sitemaps/news.xml'),
        ('xmlns', "http://www.sitemaps.org/schemas/sitemap/0.9"),
    ]
    itertag = 'url'

    def parse_node(self, response, node):
        # self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.getall()))

        # item = GuardianItem()
        item = NewsItem()
        item['headline'] = node.xpath("//*[local-name()='title']/text()").get()
        item['source'] = 'The Guardian'
        item['date_time'] = node.xpath("//*[local-name()='publication_date']/text()").get()

        url = node.xpath("//*[local-name()='loc']/text()").get()
        item['url'] = url

        y = node.xpath("//*[local-name()='keywords']/text()").get()
        if y:
            x = y.split(",")
            item['tags'] = x
        else:
            item['tags'] = 'No tags'

        yield scrapy.Request(url, meta={'item': item}, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        old_item = response.request.meta['item']

        selector1 = '//a[@rel="author"]/text()'
        selector2 = 'p::text'
        selector3 = '//meta[@name="keywords"]/@content'

        author = response.xpath(selector1).get()

        if author == "" or author == 'None' or author == " ":
            old_item['author'] = "The Guardian"
        elif not author:
            old_item['author'] = "The Guardian"
        else:
            old_item['author'] = response.xpath(selector1).get()

        old_item['content'] = response.css(selector2).getall()

        yield old_item
