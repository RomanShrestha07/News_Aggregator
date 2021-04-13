import scrapy
from ..items import ApNewsItem, ApNewsItem2, GuardianItem, NewsItem


class ApNewsSpider(scrapy.Spider):
    name = "ap_news_spider"
    start_urls = ['https://apnews.com/hub/ap-top-news']

    def parse(self, response):
        selector1 = 'div.FeedCard'

        for news_title in response.css(selector1):
            selector2 = 'h1::text'
            selector3 = 'span::text'
            selector4 = 'span.Timestamp::attr(title)'
            selector5 = 'a::attr(href)'

            item = ApNewsItem()

            item['headline'] = news_title.css(selector2).get()
            item['author'] = news_title.css(selector3).extract_first()
            item['date_time'] = news_title.css(selector4).get()
            item['url'] = news_title.css(selector5).get()

            yield item


class ApNewsSpider2(scrapy.Spider):
    name = "ap_news_spider_2"
    start_urls = ['https://apnews.com/hub/ap-top-news']

    def parse(self, response):
        selector1 = 'div.FeedCard'
        n = 0

        for href in response.css(selector1):
            selector2 = 'a::attr(href)'
            n = n + 1
            url = response.urljoin(href.css(selector2).get())
            yield scrapy.Request(url, meta={'counter': n}, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        selector3 = 'div.Content'
        counter = response.request.meta['counter']

        for news in response.css(selector3):
            selector4 = 'h1::text'
            selector5 = 'span::text'
            selector6 = 'span.Timestamp::attr(title)'
            selector7 = 'p::text'
            selector8 = '//meta[@name="keywords"]/@content'
            selector9 = '//meta[@property="article:section"]/@content'
            selector10 = '//meta[@property="og:image"]/@content'
            selector11 = '//meta[@property="og:description"]/@content'

            # item = ApNewsItem2()
            item = NewsItem()

            # item['news_id'] = 'AP-News-' + str(counter)

            item['headline'] = news.css(selector4).get()
            item['source'] = 'AP News'

            author = news.css(selector5).extract_first()

            if author.startswith('By') or author.startswith('BY'):
                temp = author[3:]
                item['author'] = temp
            else:
                item['author'] = 'AP News'

            item['date_time'] = news.css(selector6).get()

            con = news.css(selector7).getall()
            # item['content'] = ' '.join(con)
            item['content'] = con
            item['url'] = response.request.url

            y = news.xpath(selector8).get()
            x = y.split(",")
            item['tags'] = x

            item['section'] = news.xpath(selector9).get()
            item['image'] = news.xpath(selector10).get()
            item['description'] = news.xpath(selector11).get()

            yield item
