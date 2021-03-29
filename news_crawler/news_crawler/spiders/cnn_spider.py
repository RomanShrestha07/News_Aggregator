import scrapy
from ..items import ApNewsItem, ApNewsItem2, GuardianItem, NewsItem
from scrapy.spiders import XMLFeedSpider, SitemapSpider
from scrapy import Spider


class CNNSpider(XMLFeedSpider, Spider):
    name = "cnn_spider"
    start_urls = ['https://edition.cnn.com/sitemaps/cnn/news.xml']
    namespaces = [
        ('news', 'https://edition.cnn.com/sitemaps/cnn/news.xml'),
        ('xmlns', "http://www.sitemaps.org/schemas/sitemap/0.9"),
    ]
    itertag = 'url'

    def parse_node(self, response, node):
        item = NewsItem()

        item['headline'] = node.xpath("//*[local-name()='title']/text()").get()
        item['source'] = 'CNN'
        item['date_time'] = node.xpath("//*[local-name()='publication_date']/text()").get()

        url = node.xpath("//*[local-name()='loc']/text()").get()
        item['url'] = url

        yield scrapy.Request(url, meta={'item': item}, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        old_item = response.request.meta['item']

        selector1 = '//meta[@name="author"]/@content'
        selector2 = 'div.zn-body__paragraph::text'
        selector3 = '//meta[@name="section"]/@content'
        selector4 = 'p.zn-body__paragraph::text'

        author = response.xpath(selector1).get()

        if author == "" or author == 'None' or author == " ":
            old_item['author'] = "CNN"
        elif not author:
            old_item['author'] = "CNN"
        else:
            old_item['author'] = response.xpath(selector1).get()

        c = response.css(selector4).get()
        con = response.css(selector2).getall()
        old_item['content'] = c + ' '.join(con)

        old_item['tags'] = response.xpath(selector3).get()

        yield old_item
