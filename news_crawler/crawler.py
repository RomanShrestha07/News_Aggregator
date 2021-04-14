from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from news_crawler.spiders.ap_news_spider import ApNewsSpider2
from news_crawler.spiders.guardian_spider import GuardianSpider
from news_crawler.spiders.reuters_spider import ReutersSpider

process = CrawlerProcess(get_project_settings())

process.crawl(ApNewsSpider2)
process.crawl(GuardianSpider)
process.crawl(ReutersSpider)
process.start()
