import scrapy
from ..items import ApNewsItem, ApNewsItem2, GuardianItem, NewsItem
from scrapy.spiders import XMLFeedSpider, SitemapSpider
from scrapy import Spider


class BBCSpider(XMLFeedSpider, Spider):
    name = "bbc_spider"
    start_urls = ['https://www.bbc.co.uk/sitemaps/https-sitemap-uk-news-1.xml']
    namespaces = [
        ('news', 'https://www.bbc.co.uk/sitemaps/https-sitemap-uk-news-1.xml'),
        ('xmlns', "http://www.sitemaps.org/schemas/sitemap/0.9"),
    ]
    itertag = 'url'

    def parse_node(self, response, node):
        item = NewsItem()

        item['headline'] = node.xpath("//*[local-name()='title']/text()").get()
        item['source'] = 'BBC News'
        item['date_time'] = node.xpath("//*[local-name()='publication_date']/text()").get()

        url = node.xpath("//*[local-name()='loc']/text()").get()
        item['url'] = url

        yield scrapy.Request(url, meta={'item': item}, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        old_item = response.request.meta['item']

        selector1 = "//figure/div/span/span/img[@alt='Analysis']/@alt"
        selector2 = '//header/p/span/strong/text()'
        selector3 = 'p::text'
        selector4 = "//meta[@property='article:section']/@content"

        author1 = response.xpath(selector1).get()
        author2 = response.xpath(selector2).get()

        if author1:
            old_item['author'] = author1
        elif author2:
            old_item['author'] = author2
        else:
            old_item['author'] = "BBC News"

        con = response.css(selector3).getall()
        old_item['content'] = ' '.join(con)

        old_item['tags'] = response.xpath(selector4).get()

        yield old_item
